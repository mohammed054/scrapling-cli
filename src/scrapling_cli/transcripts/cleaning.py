from __future__ import annotations

import html
import json
import re

TIMESTAMP_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}$")
SRT_TIMESTAMP_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3}\s+-->\s+\d{2}:\d{2}:\d{2},\d{3}$")


def clean_plain_text(text: str) -> str:
    lines = []
    last = ""
    for raw_line in text.splitlines():
        line = html.unescape(re.sub(r"<[^>]+>", "", raw_line)).strip()
        line = re.sub(r"\s+", " ", line)
        if not line or line == last:
            continue
        lines.append(line)
        last = line
    return " ".join(lines).strip()


def clean_vtt_payload(payload: str) -> str:
    lines: list[str] = []
    for raw_line in payload.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line in {"WEBVTT", "Kind: captions", "Language: en"}:
            continue
        if TIMESTAMP_PATTERN.match(line):
            continue
        if line.isdigit():
            continue
        lines.append(line)
    return clean_plain_text("\n".join(lines))


def clean_srt_payload(payload: str) -> str:
    lines: list[str] = []
    for raw_line in payload.splitlines():
        line = raw_line.strip()
        if not line or line.isdigit() or SRT_TIMESTAMP_PATTERN.match(line):
            continue
        lines.append(line)
    return clean_plain_text("\n".join(lines))


def clean_json3_payload(payload: str) -> str:
    data = json.loads(payload)
    lines: list[str] = []
    for event in data.get("events", []):
        for segment in event.get("segs", []):
            text = (segment.get("utf8") or "").replace("\n", " ").strip()
            if text:
                lines.append(text)
    return clean_plain_text("\n".join(lines))


def clean_subtitle_payload(payload: str, extension: str) -> str:
    normalized_extension = extension.lower().lstrip(".")
    if normalized_extension in {"vtt", "srv1", "srv2", "srv3"}:
        return clean_vtt_payload(payload)
    if normalized_extension == "srt":
        return clean_srt_payload(payload)
    if normalized_extension == "json3":
        return clean_json3_payload(payload)
    return clean_plain_text(payload)


def merge_transcript_chunks(chunks: list[str]) -> str:
    return clean_plain_text("\n".join(chunk.strip() for chunk in chunks if chunk.strip()))
