from __future__ import annotations

import io
import threading
import time
import urllib.request

import pytest

from scrapling_cli.models import ContentItem, TranscriptOptions, TranscriptResult
from scrapling_cli.transcripts.backends import (
    OpenAIAsrBackend,
    RetryableTranscriptError,
    TranscriptBackendError,
    YouTubeTranscriptApiBackend,
    YtDlpSubtitleBackend,
)
from scrapling_cli.transcripts.cache import TranscriptCache
from scrapling_cli.transcripts.service import TranscriptService


class FakeBackend:
    def __init__(self, name, result=None, error=None):
        self.name = name
        self._result = result
        self._error = error
        self.calls = 0

    def fingerprint(self, options):
        return f"{self.name}:{options.language}"

    def fetch(self, item, options):
        self.calls += 1
        if self._error:
            raise self._error
        return self._result


def test_service_uses_first_available_backend(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path)
    primary = FakeBackend(
        "youtube_transcript_api",
        TranscriptResult.available(source="youtube_transcript_api", text="manual", language="en", backend_fingerprint="a"),
    )
    secondary = FakeBackend(
        "yt_dlp",
        TranscriptResult.available(source="yt_dlp_auto_subtitle", text="auto", language="en", backend_fingerprint="b"),
    )
    service = TranscriptService(options, backends=[primary, secondary], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(item)
    assert result.text == "manual"
    assert primary.calls == 1
    assert secondary.calls == 0


def test_service_falls_back_after_retryable_error(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path, retry_attempts=2, request_delay_seconds=0)
    failing = FakeBackend("youtube_transcript_api", error=RetryableTranscriptError("blocked"))
    fallback = FakeBackend(
        "yt_dlp",
        TranscriptResult.available(source="yt_dlp_auto_subtitle", text="fallback", language="en", backend_fingerprint="b"),
    )
    service = TranscriptService(options, backends=[failing, fallback], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(item)
    assert result.text == "fallback"
    assert failing.calls == 2
    assert fallback.calls == 1


def test_retryable_failure_is_not_cached(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path, retry_attempts=2, request_delay_seconds=0)
    backend = FakeBackend("youtube_transcript_api", error=RetryableTranscriptError("429 Too Many Requests"))
    service = TranscriptService(options, backends=[backend], cache=TranscriptCache(tmp_path))

    first = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    second = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")

    service.resolve_item(first)
    service.resolve_item(second)

    assert backend.calls == 4


def test_transient_cached_failure_is_ignored(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path)
    backend = FakeBackend(
        "youtube_transcript_api",
        TranscriptResult.available(source="youtube_transcript_api", text="fresh", language="en", backend_fingerprint="a"),
    )
    cache = TranscriptCache(tmp_path)
    fingerprint = backend.fingerprint(options)
    cache.save(
        "vid",
        TranscriptResult.unavailable(
            source=backend.name,
            language="en",
            error="429 Too Many Requests",
            backend_fingerprint=fingerprint,
        ),
    )

    service = TranscriptService(options, backends=[backend], cache=cache)
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(item)

    assert result.status == "available"
    assert result.text == "fresh"
    assert backend.calls == 1


def test_service_uses_cache_for_second_call(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path)
    backend = FakeBackend(
        "youtube_transcript_api",
        TranscriptResult.available(source="youtube_transcript_api", text="cached", language="en", backend_fingerprint="a"),
    )
    service = TranscriptService(options, backends=[backend], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    service.resolve_item(item)
    second = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(second)
    assert result.cached is True
    assert backend.calls == 1


def test_service_reports_no_key_when_hosted_asr_unavailable(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path, allow_hosted_asr=None, openai_api_key="")
    backend = FakeBackend(
        "youtube_transcript_api",
        TranscriptResult.unavailable(source="youtube_transcript_api", error="disabled", language="en", backend_fingerprint="a"),
    )
    service = TranscriptService(options, backends=[backend], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(item)
    assert result.status == "unavailable"
    assert "missing_OPENAI_API_KEY" in result.error


class _FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


def test_ytdlp_backend_prefers_manual_subtitles(monkeypatch):
    backend = YtDlpSubtitleBackend()
    monkeypatch.setattr(
        backend,
        "_extract_info",
        lambda item, options: {
            "subtitles": {"en": [{"ext": "vtt", "url": "https://subs/manual"}]},
            "automatic_captions": {"en": [{"ext": "vtt", "url": "https://subs/auto"}]},
        },
    )
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda request, timeout=30: _FakeResponse(b"WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nManual\n"),
    )
    result = backend.fetch(ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid"), TranscriptOptions(enabled=True))
    assert result.source == "yt_dlp_manual_subtitle"
    assert result.text == "Manual"


def test_ytdlp_backend_uses_auto_subtitles_when_manual_missing(monkeypatch):
    backend = YtDlpSubtitleBackend()
    monkeypatch.setattr(
        backend,
        "_extract_info",
        lambda item, options: {
            "subtitles": {},
            "automatic_captions": {"en": [{"ext": "json3", "url": "https://subs/auto"}]},
        },
    )
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda request, timeout=30: _FakeResponse(b'{"events":[{"segs":[{"utf8":"Auto"}]}]}'),
    )
    result = backend.fetch(ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid"), TranscriptOptions(enabled=True))
    assert result.source == "yt_dlp_auto_subtitle"
    assert result.text == "Auto"


def test_ytdlp_backend_sends_browser_like_headers(monkeypatch):
    backend = YtDlpSubtitleBackend()
    captured = {}
    monkeypatch.setattr(
        backend,
        "_extract_info",
        lambda item, options: {
            "subtitles": {"en": [{"ext": "vtt", "url": "https://subs/manual"}]},
            "automatic_captions": {},
        },
    )

    def _capture_request(request, timeout=30):
        captured["headers"] = dict(request.header_items())
        return _FakeResponse(b"WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nManual\n")

    monkeypatch.setattr(urllib.request, "urlopen", _capture_request)

    backend.fetch(
        ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid"),
        TranscriptOptions(enabled=True, language="en-US"),
    )

    assert captured["headers"]["User-agent"].startswith("Mozilla/5.0")
    assert captured["headers"]["Accept-language"] == "en-US,en;q=0.9"


def test_openai_asr_backend_merges_chunks(monkeypatch, tmp_path):
    backend = OpenAIAsrBackend()

    class DummyFFmpeg:
        @staticmethod
        def get_ffmpeg_exe():
            return "ffmpeg"

    class DummyOpenAIClient:
        class audio:
            class transcriptions:
                @staticmethod
                def create(model, file, response_format):
                    class Response:
                        text = f"chunk:{Path(file.name).name}"

                    return Response()

        def __init__(self, api_key=None):
            self.api_key = api_key

    class DummyYDL:
        pass

    from pathlib import Path

    audio_path = tmp_path / "source.m4a"
    normalized_path = tmp_path / "normalized.mp3"
    chunk_a = tmp_path / "chunk_000.mp3"
    chunk_b = tmp_path / "chunk_001.mp3"
    for path in (audio_path, normalized_path, chunk_a, chunk_b):
        path.write_bytes(b"audio")

    monkeypatch.setattr(backend, "_require_dependencies", lambda: (DummyFFmpeg, DummyOpenAIClient, DummyYDL))
    monkeypatch.setattr(backend, "_download_audio", lambda item, workdir, YoutubeDL, options: audio_path)
    monkeypatch.setattr(backend, "_normalize_audio", lambda input_path, output_path, ffmpeg_exe: normalized_path.write_bytes(b"norm"))
    monkeypatch.setattr(backend, "_chunk_audio", lambda normalized_path, ffmpeg_exe: [chunk_a, chunk_b])

    result = backend.fetch(
        ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid"),
        TranscriptOptions(enabled=True, openai_api_key="test-key"),
    )
    assert result.status == "available"
    assert "chunk:chunk_000.mp3" in result.text
    assert "chunk:chunk_001.mp3" in result.text


@pytest.mark.live
def test_live_smoke_suite():
    pytest.skip("Set SCRAPLING_RUN_LIVE_SMOKE=1 and provide stable live URLs before running.")


# ---------------------------------------------------------------------------
# v1.x exception handling — non-retryable errors must not be retried
# ---------------------------------------------------------------------------

class _FakeCouldNotRetrieveTranscript(Exception):
    """Minimal stand-in for youtube_transcript_api.CouldNotRetrieveTranscript."""


class _FakePoTokenRequired(_FakeCouldNotRetrieveTranscript):
    """Minimal stand-in for youtube_transcript_api.PoTokenRequired."""


class _FakeIpBlocked(_FakeCouldNotRetrieveTranscript):
    """Minimal stand-in for youtube_transcript_api.IpBlocked."""


def test_non_retryable_error_not_retried_falls_through_to_next_backend(tmp_path, monkeypatch):
    """IpBlocked (CouldNotRetrieveTranscript subclass) must raise TranscriptBackendError,
    not RetryableTranscriptError, so the service tries yt-dlp without extra retries."""
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path)

    # Patch _load_transcript_api_exceptions to return our fake hierarchy
    import scrapling_cli.transcripts.backends as _backends_mod
    monkeypatch.setattr(
        _backends_mod,
        "_load_transcript_api_exceptions",
        lambda: (_FakeCouldNotRetrieveTranscript, _FakePoTokenRequired),
    )

    yta_backend = YouTubeTranscriptApiBackend()
    # Make _get_api() return an object whose .list() raises IpBlocked
    class _FakeApi:
        def list(self, video_id):
            raise _FakeIpBlocked("Your IP has been blocked")
    monkeypatch.setattr(yta_backend, "_get_api", lambda options: _FakeApi())

    fallback = FakeBackend(
        "yt_dlp",
        TranscriptResult.available(source="yt_dlp_auto_subtitle", text="fallback text", language="en", backend_fingerprint="b"),
    )

    service = TranscriptService(options, backends=[yta_backend, fallback], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(item)

    # Should have fallen through to yt-dlp and succeeded
    assert result.status == "available"
    assert result.text == "fallback text"
    # yt_dlp backend called exactly once (no extra retries on yta_backend's error)
    assert fallback.calls == 1


def test_non_retryable_error_raises_backend_error_not_retryable(monkeypatch):
    """YouTubeTranscriptApiBackend.fetch() must raise TranscriptBackendError
    (not RetryableTranscriptError) when api.list() raises CouldNotRetrieveTranscript."""
    import scrapling_cli.transcripts.backends as _backends_mod
    monkeypatch.setattr(
        _backends_mod,
        "_load_transcript_api_exceptions",
        lambda: (_FakeCouldNotRetrieveTranscript, _FakePoTokenRequired),
    )

    backend = YouTubeTranscriptApiBackend()
    class _FakeApi:
        def list(self, video_id):
            raise _FakeIpBlocked("blocked")
    monkeypatch.setattr(backend, "_get_api", lambda options: _FakeApi())

    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    options = TranscriptOptions(enabled=True)

    with pytest.raises(TranscriptBackendError) as exc_info:
        backend.fetch(item, options)

    assert not isinstance(exc_info.value, RetryableTranscriptError), (
        "IpBlocked must NOT become a RetryableTranscriptError"
    )


def test_po_token_required_is_non_retryable(monkeypatch):
    """PoTokenRequired must also map to TranscriptBackendError."""
    import scrapling_cli.transcripts.backends as _backends_mod
    monkeypatch.setattr(
        _backends_mod,
        "_load_transcript_api_exceptions",
        lambda: (_FakeCouldNotRetrieveTranscript, _FakePoTokenRequired),
    )

    backend = YouTubeTranscriptApiBackend()
    class _FakeApi:
        def list(self, video_id):
            raise _FakePoTokenRequired("PO token required")
    monkeypatch.setattr(backend, "_get_api", lambda options: _FakeApi())

    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    options = TranscriptOptions(enabled=True)

    with pytest.raises(TranscriptBackendError) as exc_info:
        backend.fetch(item, options)

    assert not isinstance(exc_info.value, RetryableTranscriptError)


def test_genuine_network_error_is_still_retryable(monkeypatch):
    """A plain network exception (e.g. ConnectionError) must still become
    RetryableTranscriptError so the service retries with backoff."""
    import scrapling_cli.transcripts.backends as _backends_mod
    monkeypatch.setattr(
        _backends_mod,
        "_load_transcript_api_exceptions",
        lambda: (_FakeCouldNotRetrieveTranscript, _FakePoTokenRequired),
    )

    backend = YouTubeTranscriptApiBackend()
    class _FakeApi:
        def list(self, video_id):
            raise ConnectionResetError("connection reset by peer")
    monkeypatch.setattr(backend, "_get_api", lambda options: _FakeApi())

    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    options = TranscriptOptions(enabled=True)

    with pytest.raises(RetryableTranscriptError):
        backend.fetch(item, options)


def test_non_retryable_backend_is_not_retried_by_service(tmp_path, monkeypatch):
    """Service must call a backend that raises TranscriptBackendError exactly ONCE
    (no retry loop), then continue to the next backend."""
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path)

    non_retryable = FakeBackend("youtube_transcript_api", error=TranscriptBackendError("ip blocked"))
    fallback = FakeBackend(
        "yt_dlp",
        TranscriptResult.available(source="yt_dlp_auto_subtitle", text="ok", language="en", backend_fingerprint="b"),
    )

    service = TranscriptService(options, backends=[non_retryable, fallback], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    result = service.resolve_item(item)

    assert result.status == "available"
    assert non_retryable.calls == 1  # NOT retried
    assert fallback.calls == 1


def test_retryable_backoff_is_exponential(tmp_path, monkeypatch):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path, request_delay_seconds=0, retry_attempts=4)
    backend = FakeBackend("youtube_transcript_api", error=RetryableTranscriptError("blocked"))
    service = TranscriptService(options, backends=[backend], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    sleeps = []

    import scrapling_cli.transcripts.service as service_mod

    monkeypatch.setattr(service_mod.time, "sleep", lambda seconds: sleeps.append(seconds))

    result = service.resolve_item(item)

    assert result.status == "unavailable"
    assert sleeps == [1.0, 2.0, 4.0]


def test_rate_limited_failure_extends_global_cooldown(tmp_path, monkeypatch):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path, request_delay_seconds=2, retry_attempts=2)
    failing = FakeBackend("youtube_transcript_api", error=RetryableTranscriptError("HTTP Error 429: Too Many Requests"))
    fallback = FakeBackend(
        "yt_dlp",
        TranscriptResult.available(source="yt_dlp_auto_subtitle", text="fallback", language="en", backend_fingerprint="b"),
    )
    service = TranscriptService(options, backends=[failing, fallback], cache=TranscriptCache(tmp_path))
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    sleeps = []

    import scrapling_cli.transcripts.service as service_mod

    clock = {"now": 0.0}

    def _sleep(seconds):
        sleeps.append(seconds)
        clock["now"] += seconds

    monkeypatch.setattr(service_mod.time, "sleep", _sleep)
    monkeypatch.setattr(service_mod.time, "monotonic", lambda: clock["now"])

    result = service.resolve_item(item)

    assert result.status == "available"
    assert sleeps == [15.0, 15.0]


def test_resolve_many_serializes_backend_fetches(tmp_path):
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path, workers=3, request_delay_seconds=0)
    concurrency = {"active": 0, "max_active": 0}
    lock = threading.Lock()

    class SerialProbeBackend:
        name = "youtube_transcript_api"

        def fingerprint(self, options):
            return f"{self.name}:{options.language}"

        def fetch(self, item, options):
            with lock:
                concurrency["active"] += 1
                concurrency["max_active"] = max(concurrency["max_active"], concurrency["active"])
            time.sleep(0.05)
            with lock:
                concurrency["active"] -= 1
            return TranscriptResult.available(
                source=self.name,
                text=f"ok:{item.id}",
                language="en",
                backend_fingerprint=self.fingerprint(options),
            )

    service = TranscriptService(options, backends=[SerialProbeBackend()], cache=TranscriptCache(tmp_path))
    items = [
        ContentItem(id="a", title="A", url="https://youtube.com/watch?v=a"),
        ContentItem(id="b", title="B", url="https://youtube.com/watch?v=b"),
        ContentItem(id="c", title="C", url="https://youtube.com/watch?v=c"),
    ]

    service.resolve_many(items)

    assert concurrency["max_active"] == 1
