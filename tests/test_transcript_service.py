from __future__ import annotations

import io
import urllib.request

import pytest

from scrapling_cli.models import ContentItem, TranscriptOptions, TranscriptResult
from scrapling_cli.transcripts.backends import (
    OpenAIAsrBackend,
    RetryableTranscriptError,
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
    options = TranscriptOptions(enabled=True, cache_dir=tmp_path)
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
        lambda item: {
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
        lambda item: {
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
    monkeypatch.setattr(backend, "_download_audio", lambda item, workdir, YoutubeDL: audio_path)
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
