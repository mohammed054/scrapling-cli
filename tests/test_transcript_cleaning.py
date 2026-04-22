from __future__ import annotations

import json

from scrapling_cli.transcripts.cleaning import (
    clean_json3_payload,
    clean_subtitle_payload,
    clean_vtt_payload,
    merge_transcript_chunks,
)


def test_clean_vtt_payload_strips_metadata_and_timestamps():
    payload = """WEBVTT

00:00:00.000 --> 00:00:01.000
Hello

00:00:01.000 --> 00:00:02.000
world
"""
    assert clean_vtt_payload(payload) == "Hello world"


def test_clean_json3_payload_extracts_segments():
    payload = json.dumps({"events": [{"segs": [{"utf8": "Hello "}, {"utf8": "world"}]}]})
    assert clean_json3_payload(payload) == "Hello world"


def test_clean_subtitle_payload_routes_by_extension():
    payload = "1\n00:00:00,000 --> 00:00:01,000\nHello\n"
    assert clean_subtitle_payload(payload, "srt") == "Hello"


def test_merge_transcript_chunks_is_deterministic():
    assert merge_transcript_chunks([" Hello", "world ", "world"]) == "Hello world"
