from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from ..models import ContentItem, TranscriptOptions, TranscriptResult
from .backends import (
    OpenAIAsrBackend,
    RetryableTranscriptError,
    TranscriptBackend,
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

    def _default_backends(self) -> list[TranscriptBackend]:
        backends: list[TranscriptBackend] = [
            YouTubeTranscriptApiBackend(),
            YtDlpSubtitleBackend(),
        ]
        if self.options.hosted_asr_enabled():
            backends.append(OpenAIAsrBackend())
        return backends

    def _is_transient_failure(self, result: TranscriptResult) -> bool:
        if result.status != "unavailable" or not result.error:
            return False
        error = result.error.lower()
        return any(marker in error for marker in TRANSIENT_FAILURE_MARKERS)

    def _pace_request(self, backend: TranscriptBackend, item: ContentItem) -> None:
        delay_seconds = max(0.0, self.options.request_delay_seconds)
        with self._request_lock:
            now = time.monotonic()
            scheduled_at = max(now, self._next_request_at)
            self._next_request_at = scheduled_at + delay_seconds
        sleep_for = scheduled_at - now
        if sleep_for > 0:
            logger.debug(
                "transcript.pacing backend=%s video_id=%s sleep_seconds=%.2f",
                backend.name,
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
    ) -> bool:
        if not error or not self._is_rate_limited_error(error):
            return False
        cooldown_seconds = max(
            15.0,
            max(1.0, self.options.request_delay_seconds) * (2 ** attempt),
        )
        with self._request_lock:
            now = time.monotonic()
            resume_at = now + cooldown_seconds
            self._next_request_at = max(self._next_request_at, resume_at)
        logger.warning(
            "transcript.cooldown backend=%s video_id=%s attempt=%s cooldown_seconds=%.2f error=%s",
            backend.name,
            item.id,
            attempt,
            cooldown_seconds,
            error,
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
                error = str(exc)
                cooled_down = self._extend_rate_limit_cooldown(backend, item, attempt=attempt, error=error)
                logger.warning(
                    "transcript.retry backend=%s video_id=%s attempt=%s error=%s",
                    backend.name,
                    item.id,
                    attempt,
                    error,
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
                if cooled_down:
                    continue
                backoff_seconds = backoff_base * (2 ** (attempt - 1))
                logger.info(
                    "transcript.backoff backend=%s video_id=%s attempt=%s sleep_seconds=%.2f",
                    backend.name,
                    item.id,
                    attempt,
                    backoff_seconds,
                )
                time.sleep(backoff_seconds)
            except TranscriptBackendError as exc:
                logger.warning(
                    "transcript.backend_error backend=%s video_id=%s error=%s",
                    backend.name,
                    item.id,
                    exc,
                )
                return (
                    TranscriptResult.unavailable(
                        source=backend.name,
                        language=self.options.language,
                        error=str(exc),
                        backend_fingerprint=backend.fingerprint(self.options),
                    ),
                    True,
                )

    def resolve_item(self, item: ContentItem) -> TranscriptResult:
        if not self.options.enabled:
            item.transcript = TranscriptResult.skipped("transcripts_disabled", language=self.options.language)
            return item.transcript

        errors: list[str] = []
        for backend in self.backends:
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

            result, cacheable = self._with_retry(backend, item)
            result.backend_fingerprint = fingerprint
            if cacheable:
                self.cache.save(item.id, result)
                logger.info(
                    "transcript.backend_result backend=%s video_id=%s status=%s source=%s",
                    backend.name,
                    item.id,
                    result.status,
                    result.source or backend.name,
                )
            else:
                logger.info(
                    "transcript.backend_result_uncached backend=%s video_id=%s status=%s source=%s",
                    backend.name,
                    item.id,
                    result.status,
                    result.source or backend.name,
                )
            if result.status == "available":
                item.transcript = result
                return result
            errors.append(f"{backend.name}: {result.error or result.status}")

        if not any(backend.name == "openai_asr" for backend in self.backends):
            if self.options.allow_hosted_asr is False:
                errors.append("openai_asr: disabled_by_flag")
            elif not self.options.openai_api_key:
                errors.append("openai_asr: missing_OPENAI_API_KEY")

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
