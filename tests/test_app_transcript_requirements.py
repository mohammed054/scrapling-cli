from __future__ import annotations

import argparse
import os

import pytest

from scrapling_cli.app import TranscriptResolutionError, _resolve_transcripts_or_raise
from scrapling_cli.cli_common import (
    add_transcript_arguments,
    build_transcript_options,
    describe_cookie_source,
    describe_hosted_asr,
    load_env_file,
)
from scrapling_cli.models import ContentItem, TranscriptOptions, TranscriptResult


class SequencedTranscriptService:
    def __init__(self, *results):
        self._results = list(results)
        self.calls = 0

    def resolve_many(self, items):
        result = self._results[min(self.calls, len(self._results) - 1)]
        self.calls += 1
        for item in items:
            item.transcript = result(item) if callable(result) else result
        return items

    def is_retryable_failure(self, result):
        error = (result.error or "").lower()
        return result.status == "unavailable" and "429" in error

    def seconds_until_next_request(self):
        return 0.0


def test_resolve_transcripts_or_raise_retries_until_item_is_available(monkeypatch):
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    options = TranscriptOptions(enabled=True, require_success=True, request_delay_seconds=4.0)
    service = SequencedTranscriptService(
        TranscriptResult.unavailable(source="youtube_transcript_api", error="429 Too Many Requests", language="en"),
        TranscriptResult.available(source="yt_dlp_auto_subtitle", text="ok", language="en"),
    )
    sleeps = []

    import scrapling_cli.app as app_mod

    monkeypatch.setattr(app_mod.time, "sleep", lambda seconds: sleeps.append(seconds))

    _resolve_transcripts_or_raise(service, [item], options)

    assert item.transcript.status == "available"
    assert service.calls == 2
    assert sleeps == [30.0]


def test_resolve_transcripts_or_raise_raises_for_permanent_failure():
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    options = TranscriptOptions(enabled=True, require_success=True)
    service = SequencedTranscriptService(
        TranscriptResult.unavailable(source="yt_dlp", error="no subtitles exposed by yt-dlp", language="en")
    )

    with pytest.raises(TranscriptResolutionError) as exc_info:
        _resolve_transcripts_or_raise(service, [item], options)

    assert "Could not resolve all transcripts" in str(exc_info.value)
    assert "no subtitles exposed by yt-dlp" in str(exc_info.value)


def test_resolve_transcripts_or_raise_allows_missing_when_opted_out():
    item = ContentItem(id="vid", title="Title", url="https://youtube.com/watch?v=vid")
    options = TranscriptOptions(enabled=True, require_success=False)
    service = SequencedTranscriptService(
        TranscriptResult.unavailable(source="yt_dlp", error="no subtitles exposed by yt-dlp", language="en")
    )

    _resolve_transcripts_or_raise(service, [item], options)

    assert item.transcript.status == "unavailable"
    assert service.calls == 1


def test_build_transcript_options_requires_success_by_default():
    parser = argparse.ArgumentParser()
    add_transcript_arguments(parser)

    args = parser.parse_args([])
    options = build_transcript_options(args)

    assert options.require_success is True
    assert options.rate_limit_cooldown_seconds == 300.0
    assert options.rate_limit_cooldown_cap_seconds == 3600.0
    assert options.openrouter_asr_model == "openai/whisper-large-v3"


def test_build_transcript_options_can_allow_missing_transcripts():
    parser = argparse.ArgumentParser()
    add_transcript_arguments(parser)

    args = parser.parse_args(["--allow-missing-transcripts"])
    options = build_transcript_options(args)

    assert options.require_success is False


def test_build_transcript_options_accepts_openrouter_asr_model():
    parser = argparse.ArgumentParser()
    add_transcript_arguments(parser)

    args = parser.parse_args(["--openrouter-asr-model", "openai/whisper-1"])
    options = build_transcript_options(args)

    assert options.openrouter_asr_model == "openai/whisper-1"


def test_build_transcript_options_accepts_cookie_sources(tmp_path):
    parser = argparse.ArgumentParser()
    add_transcript_arguments(parser)

    cookie_file = tmp_path / "cookies.txt"
    args = parser.parse_args(["--cookies-from-browser", "chrome", "--cookies", str(cookie_file)])
    options = build_transcript_options(args)

    assert options.cookies_from_browser == "chrome"
    assert options.cookies_file == cookie_file


def test_load_env_file_reads_local_keys_without_overriding(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENROUTER_API_KEY=from-file\nOPENAI_API_KEY=from-file-openai\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "already-set")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    load_env_file(env_file)

    assert os.environ["OPENROUTER_API_KEY"] == "already-set"
    assert os.environ["OPENAI_API_KEY"] == "from-file-openai"


def test_describe_hosted_asr_reports_openrouter():
    options = TranscriptOptions(enabled=True, openai_api_key="", openrouter_api_key="test-key")

    assert describe_hosted_asr(options) == "openrouter"


def test_describe_cookie_source_reports_browser():
    options = TranscriptOptions(enabled=True, cookies_from_browser="chrome")

    assert describe_cookie_source(options) == "browser:chrome"
