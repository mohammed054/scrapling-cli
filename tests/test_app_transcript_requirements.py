from __future__ import annotations

import argparse

import pytest

from scrapling_cli.app import TranscriptResolutionError, _resolve_transcripts_or_raise
from scrapling_cli.cli_common import add_transcript_arguments, build_transcript_options
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


def test_build_transcript_options_can_allow_missing_transcripts():
    parser = argparse.ArgumentParser()
    add_transcript_arguments(parser)

    args = parser.parse_args(["--allow-missing-transcripts"])
    options = build_transcript_options(args)

    assert options.require_success is False
