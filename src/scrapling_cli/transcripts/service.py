from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    def _default_backends(self) -> list[TranscriptBackend]:
        backends: list[TranscriptBackend] = [
            YouTubeTranscriptApiBackend(),
            YtDlpSubtitleBackend(),
        ]
        if self.options.hosted_asr_enabled():
            backends.append(OpenAIAsrBackend())
        return backends

    def _with_retry(self, backend: TranscriptBackend, item: ContentItem, *, attempts: int = 2) -> TranscriptResult:
        for attempt in range(1, attempts + 1):
            try:
                return backend.fetch(item, self.options)
            except RetryableTranscriptError as exc:
                logger.warning(
                    "transcript.retry backend=%s video_id=%s attempt=%s error=%s",
                    backend.name,
                    item.id,
                    attempt,
                    exc,
                )
                if attempt >= attempts:
                    return TranscriptResult.unavailable(
                        source=backend.name,
                        language=self.options.language,
                        error=str(exc),
                        backend_fingerprint=backend.fingerprint(self.options),
                    )
                time.sleep(1.5 * attempt)
            except TranscriptBackendError as exc:
                logger.warning(
                    "transcript.backend_error backend=%s video_id=%s error=%s",
                    backend.name,
                    item.id,
                    exc,
                )
                return TranscriptResult.unavailable(
                    source=backend.name,
                    language=self.options.language,
                    error=str(exc),
                    backend_fingerprint=backend.fingerprint(self.options),
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
                logger.info(
                    "transcript.cache_hit backend=%s video_id=%s status=%s",
                    backend.name,
                    item.id,
                    cached.status,
                )
                if cached.status == "available":
                    item.transcript = cached
                    return cached
                logger.info(
                    "transcript.cache_miss_retry backend=%s video_id=%s cached_status=%s",
                    backend.name,
                    item.id,
                    cached.status,
                )

            result = self._with_retry(backend, item)
            result.backend_fingerprint = fingerprint
            self.cache.save(item.id, result)
            logger.info(
                "transcript.backend_result backend=%s video_id=%s status=%s source=%s",
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
