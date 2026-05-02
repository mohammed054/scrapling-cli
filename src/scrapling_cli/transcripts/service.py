from __future__ import annotations

import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from ..models import ContentItem, TranscriptOptions, TranscriptResult
from .backends import (
    OpenAIAsrBackend,
    OpenRouterAsrBackend,
    RetryableTranscriptError,
    TranscriptBackend,
    TranscriptBackendConfigurationError,
    TranscriptBackendError,
    YouTubeTranscriptApiBackend,
    YtDlpSubtitleBackend,
)
from .cache import TranscriptCache

logger = logging.getLogger(__name__)

TRANSIENT_FAILURE_MARKERS = (
    "429",
    "too many requests",
    "rate limit",
    "requestblocked",
    "request blocked",
    "ipblocked",
    "ip blocked",
    "not a bot",
    "try again later",
    "temporarily unavailable",
    "timed out",
    "connection reset",
    "service unavailable",
)

CONFIGURATION_FAILURE_MARKERS = (
    "could not read youtube cookies",
    "could not copy chrome cookie database",
    "invalid cookies-from-browser",
    "export cookies.txt",
    "set ytdlp_cookies",
)

RATE_LIMIT_FAILURE_MARKERS = (
    "429",
    "too many requests",
    "rate limit",
    "requestblocked",
    "request blocked",
    "ipblocked",
    "ip blocked",
    "not a bot",
    "try again later",
)

RATE_LIMIT_SCOPE_BY_BACKEND = {
    "youtube_transcript_api": "youtube",
    "yt_dlp": "youtube",
    "openai_asr": "hosted_asr",
    "openrouter_asr": "hosted_asr",
}
PACE_SCOPES_BY_BACKEND = {
    "openai_asr": ("hosted_asr", "youtube_media"),
    "openrouter_asr": ("hosted_asr", "youtube_media"),
}
VISIBLE_SLEEP_THRESHOLD_SECONDS = 30.0
HOSTED_ASR_BACKENDS = frozenset({"openai_asr", "openrouter_asr"})
YOUTUBE_BACKENDS = frozenset({"youtube_transcript_api", "yt_dlp"})
ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def _compact_transcript_error(error: str) -> str:
    if not error:
        return ""
    error = ANSI_ESCAPE_RE.sub("", error)
    lowered = error.lower()
    if "youtube is blocking requests from your ip" in lowered:
        return "ip blocked: YouTube is blocking transcript requests from this IP"
    lines = [line.strip() for line in error.splitlines() if line.strip()]
    compact = lines[0] if lines else error.strip()
    return compact[:500]


class TranscriptService:
    def __init__(
        self,
        options: TranscriptOptions,
        *,
        backends: list[TranscriptBackend] | None = None,
        cache: TranscriptCache | None = None,
    ) -> None:
        self.options = options
        self.cache = cache or TranscriptCache(options.cache_dir)
        self.backends = backends or self._default_backends()
        self._request_lock = Lock()
        self._fetch_lock = Lock()
        self._next_request_at = 0.0
        self._scope_next_request_at: dict[str, float] = {}
        self._scope_rate_limit_streaks: dict[str, int] = {}
        self._disabled_backend_errors: dict[str, str] = {}

    def _default_backends(self) -> list[TranscriptBackend]:
        backends: list[TranscriptBackend] = [
            YouTubeTranscriptApiBackend(),
            YtDlpSubtitleBackend(),
        ]
        if self.options.hosted_asr_enabled() and self.options.openai_api_key:
            backends.append(OpenAIAsrBackend())
        if self.options.hosted_asr_enabled() and self.options.openrouter_api_key:
            backends.append(OpenRouterAsrBackend())
        return backends

    def _is_transient_failure(self, result: TranscriptResult) -> bool:
        if result.status != "unavailable" or not result.error:
            return False
        error = result.error.lower()
        if any(marker in error for marker in CONFIGURATION_FAILURE_MARKERS):
            return False
        return any(marker in error for marker in TRANSIENT_FAILURE_MARKERS)

    def is_retryable_failure(self, result: TranscriptResult) -> bool:
        return self._is_transient_failure(result)

    def _rate_limit_scope(self, backend: TranscriptBackend) -> str:
        return RATE_LIMIT_SCOPE_BY_BACKEND.get(backend.name, backend.name)

    def _pace_scopes(self, backend: TranscriptBackend) -> tuple[str, ...]:
        return PACE_SCOPES_BY_BACKEND.get(backend.name, (self._rate_limit_scope(backend),))

    def _clear_rate_limit_state(self, backend: TranscriptBackend) -> None:
        with self._request_lock:
            for scope in self._pace_scopes(backend):
                self._scope_rate_limit_streaks.pop(scope, None)

    def _rate_limit_streak(self, scope: str) -> int:
        with self._request_lock:
            return self._scope_rate_limit_streaks.get(scope, 0)

    def _should_skip_after_youtube_rate_limit(
        self,
        backend: TranscriptBackend,
        later_backends: list[TranscriptBackend],
    ) -> bool:
        return (
            backend.name in YOUTUBE_BACKENDS
            and self._rate_limit_streak("youtube") > 0
            and any(later.name in HOSTED_ASR_BACKENDS for later in later_backends)
        )

    def seconds_until_next_request(self) -> float:
        with self._request_lock:
            scheduled_at = max(
                [self._next_request_at, *self._scope_next_request_at.values()],
                default=0.0,
            )
        return max(0.0, scheduled_at - time.monotonic())

    def _pace_request(self, backend: TranscriptBackend, item: ContentItem) -> None:
        delay_seconds = max(0.0, self.options.request_delay_seconds)
        scopes = self._pace_scopes(backend)
        with self._request_lock:
            now = time.monotonic()
            scheduled_at = max(
                now,
                self._next_request_at,
                *(self._scope_next_request_at.get(scope, 0.0) for scope in scopes),
            )
            self._next_request_at = scheduled_at + delay_seconds
            for scope in scopes:
                self._scope_next_request_at[scope] = scheduled_at + delay_seconds
        sleep_for = scheduled_at - now
        if sleep_for > 0:
            log = logger.info if sleep_for >= VISIBLE_SLEEP_THRESHOLD_SECONDS else logger.debug
            log(
                "transcript.pacing backend=%s scope=%s video_id=%s sleep_seconds=%.2f",
                backend.name,
                "+".join(scopes),
                item.id,
                sleep_for,
            )
            time.sleep(sleep_for)

    def _is_rate_limited_error(self, error: str) -> bool:
        lowered = error.lower()
        return any(marker in lowered for marker in RATE_LIMIT_FAILURE_MARKERS)

    def _extend_rate_limit_cooldown(
        self,
        backend: TranscriptBackend,
        item: ContentItem,
        *,
        attempt: int,
        error: str,
        scope_override: str | None = None,
    ) -> bool:
        if not error or not self._is_rate_limited_error(error):
            return False
        scope = scope_override or self._rate_limit_scope(backend)
        with self._request_lock:
            now = time.monotonic()
            streak = self._scope_rate_limit_streaks.get(scope, 0) + 1
            self._scope_rate_limit_streaks[scope] = streak
            base_cooldown_seconds = max(1.0, self.options.rate_limit_cooldown_seconds)
            cooldown_cap_seconds = max(base_cooldown_seconds, self.options.rate_limit_cooldown_cap_seconds)
            cooldown_seconds = min(
                cooldown_cap_seconds,
                base_cooldown_seconds * (2 ** (streak - 1)),
            )
            resume_at = now + cooldown_seconds
            self._scope_next_request_at[scope] = max(self._scope_next_request_at.get(scope, 0.0), resume_at)
        logger.warning(
            "transcript.cooldown backend=%s scope=%s video_id=%s attempt=%s streak=%s cooldown_seconds=%.2f error=%s",
            backend.name,
            scope,
            item.id,
            attempt,
            streak,
            cooldown_seconds,
            _compact_transcript_error(error),
        )
        return True

    def _with_retry(self, backend: TranscriptBackend, item: ContentItem) -> tuple[TranscriptResult, bool]:
        attempts = max(1, self.options.retry_attempts)
        backoff_base = max(1.0, self.options.request_delay_seconds)
        for attempt in range(1, attempts + 1):
            try:
                with self._fetch_lock:
                    self._pace_request(backend, item)
                    return backend.fetch(item, self.options), True
            except RetryableTranscriptError as exc:
                raw_error = str(exc)
                error = _compact_transcript_error(raw_error)
                scope_override = getattr(exc, "rate_limit_scope", None)
                scope = scope_override or self._rate_limit_scope(backend)
                cooled_down = self._extend_rate_limit_cooldown(
                    backend,
                    item,
                    attempt=attempt,
                    error=raw_error,
                    scope_override=scope_override,
                )
                logger.warning(
                    "transcript.retry backend=%s scope=%s video_id=%s attempt=%s error=%s",
                    backend.name,
                    scope,
                    item.id,
                    attempt,
                    error,
                )
                if cooled_down:
                    return (
                        TranscriptResult.unavailable(
                            source=backend.name,
                            language=self.options.language,
                            error=error,
                            backend_fingerprint=backend.fingerprint(self.options),
                        ),
                        False,
                    )
                if attempt >= attempts:
                    return (
                        TranscriptResult.unavailable(
                            source=backend.name,
                            language=self.options.language,
                            error=error,
                            backend_fingerprint=backend.fingerprint(self.options),
                        ),
                        False,
                    )
                backoff_seconds = backoff_base * (2 ** (attempt - 1))
                logger.info(
                    "transcript.backoff backend=%s video_id=%s attempt=%s sleep_seconds=%.2f",
                    backend.name,
                    item.id,
                    attempt,
                    backoff_seconds,
                )
                time.sleep(backoff_seconds)
            except TranscriptBackendConfigurationError as exc:
                error = _compact_transcript_error(str(exc))
                self._disabled_backend_errors[backend.name] = error
                logger.error(
                    "transcript.backend_disabled backend=%s video_id=%s error=%s",
                    backend.name,
                    item.id,
                    error,
                )
                return (
                    TranscriptResult.unavailable(
                        source=backend.name,
                        language=self.options.language,
                        error=error,
                        backend_fingerprint=backend.fingerprint(self.options),
                    ),
                    False,
                )
            except TranscriptBackendError as exc:
                error = _compact_transcript_error(str(exc))
                logger.warning(
                    "transcript.backend_error backend=%s video_id=%s error=%s",
                    backend.name,
                    item.id,
                    error,
                )
                return (
                    TranscriptResult.unavailable(
                        source=backend.name,
                        language=self.options.language,
                        error=error,
                        backend_fingerprint=backend.fingerprint(self.options),
                    ),
                    True,
                )

    def resolve_item(self, item: ContentItem) -> TranscriptResult:
        if not self.options.enabled:
            item.transcript = TranscriptResult.skipped("transcripts_disabled", language=self.options.language)
            return item.transcript

        errors: list[str] = []
        for index, backend in enumerate(self.backends):
            fingerprint = backend.fingerprint(self.options)
            cached = self.cache.load(item.id, fingerprint)
            if cached:
                if self._is_transient_failure(cached):
                    logger.info(
                        "transcript.cache_skip_transient backend=%s video_id=%s error=%s",
                        backend.name,
                        item.id,
                        cached.error,
                    )
                else:
                    logger.info(
                        "transcript.cache_hit backend=%s video_id=%s status=%s",
                        backend.name,
                        item.id,
                        cached.status,
                    )
                    if cached.status == "available":
                        item.transcript = cached
                        return cached
                    errors.append(f"{backend.name}: {cached.error or cached.status}")
                    continue

            if self._should_skip_after_youtube_rate_limit(backend, self.backends[index + 1 :]):
                error = "skipped_after_youtube_rate_limit_hosted_asr_available"
                logger.info(
                    "transcript.backend_skip backend=%s video_id=%s reason=%s",
                    backend.name,
                    item.id,
                    error,
                )
                errors.append(f"{backend.name}: {error}")
                continue

            disabled_error = self._disabled_backend_errors.get(backend.name)
            if disabled_error:
                logger.info(
                    "transcript.backend_skip backend=%s video_id=%s reason=disabled error=%s",
                    backend.name,
                    item.id,
                    disabled_error,
                )
                errors.append(f"{backend.name}: {disabled_error}")
                continue

            result, cacheable = self._with_retry(backend, item)
            result.backend_fingerprint = fingerprint
            if cacheable:
                self.cache.save(item.id, result)
                logger.info(
                    "transcript.backend_result backend=%s video_id=%s status=%s source=%s error=%s",
                    backend.name,
                    item.id,
                    result.status,
                    result.source or backend.name,
                    result.error,
                )
            else:
                logger.info(
                    "transcript.backend_result_uncached backend=%s video_id=%s status=%s source=%s error=%s",
                    backend.name,
                    item.id,
                    result.status,
                    result.source or backend.name,
                    result.error,
                )
            if result.status == "available":
                self._clear_rate_limit_state(backend)
                item.transcript = result
                return result
            errors.append(f"{backend.name}: {result.error or result.status}")

        if not any(backend.name in {"openai_asr", "openrouter_asr"} for backend in self.backends):
            if self.options.allow_hosted_asr is False:
                errors.append("hosted_asr: disabled_by_flag")
            elif not self.options.openai_api_key and not self.options.openrouter_api_key:
                errors.append("hosted_asr: missing_OPENAI_API_KEY_or_OPENROUTER_API_KEY")

        item.transcript = TranscriptResult.unavailable(
            source="none",
            language=self.options.language,
            error="; ".join(errors) if errors else "no transcript backend succeeded",
            backend_fingerprint="final",
        )
        return item.transcript

    def resolve_many(self, items: list[ContentItem], progress_callback=None) -> list[ContentItem]:
        if not items:
            return items
        if not self.options.enabled:
            for index, item in enumerate(items, 1):
                self.resolve_item(item)
                if progress_callback:
                    progress_callback(index, len(items), item.title)
            return items

        if self.options.workers <= 1 or len(items) == 1:
            for index, item in enumerate(items, 1):
                self.resolve_item(item)
                if progress_callback:
                    progress_callback(index, len(items), item.title)
            return items

        completed = 0
        with ThreadPoolExecutor(max_workers=self.options.workers) as executor:
            future_map = {executor.submit(self.resolve_item, item): item for item in items}
            for future in as_completed(future_map):
                future.result()
                completed += 1
                item = future_map[future]
                if progress_callback:
                    progress_callback(completed, len(items), item.title)
        return items
