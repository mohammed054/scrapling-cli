from __future__ import annotations

import json
import re
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable, Optional

from .models import ContentItem

SHORT_THRESHOLD_SECONDS = 62
MAX_FILENAME_LEN = 100
_MOJIBAKE_MARKERS = ("\u00c3", "\u00e2", "\u00f0", "\u00c2")

_RELATIVE_PATTERNS = [
    (re.compile(r"(\d+)\s*year"), 365),
    (re.compile(r"(\d+)\s*month"), 30),
    (re.compile(r"(\d+)\s*week"), 7),
    (re.compile(r"(\d+)\s*day"), 1),
]


def repair_text(text: str) -> str:
    if not text:
        return ""
    current = text
    for _ in range(3):
        if not any(marker in current for marker in _MOJIBAKE_MARKERS):
            break
        repaired = None
        for codec in ("cp1252", "latin1"):
            try:
                candidate = current.encode(codec).decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            repaired = candidate
            break
        if not repaired or repaired == current:
            break
        current = repaired
    return current


def slugify(text: str, *, max_len: int = MAX_FILENAME_LEN, separator: str = "-") -> str:
    normalized = unicodedata.normalize("NFKD", repair_text(text)).encode("ascii", "ignore").decode("ascii")
    lowered = normalized.lower()
    cleaned = re.sub(r"[^a-z0-9\s\-]", " ", lowered)
    collapsed = re.sub(r"[\s\-]+", separator, cleaned).strip(separator)
    return collapsed[:max_len] or "untitled"


def slugify_channel_name(name: str) -> str:
    return slugify(name or "unknown_channel", max_len=120, separator="_")


def format_number(value: object) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def format_duration(seconds: object) -> str:
    try:
        total = int(seconds)
    except (TypeError, ValueError):
        return "unknown"
    hours, rem = divmod(total, 3600)
    minutes, secs = divmod(rem, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def parse_date(value: object) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    raw = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            text = raw[:10] if "T" in raw else raw
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def approx_date_from_relative(relative: str) -> Optional[date]:
    if not relative:
        return None
    lowered = relative.lower()
    today = date.today()
    for pattern, multiplier in _RELATIVE_PATTERNS:
        match = pattern.search(lowered)
        if match:
            return today - timedelta(days=int(match.group(1)) * multiplier)
    if "yesterday" in lowered:
        return today - timedelta(days=1)
    if any(token in lowered for token in ("today", "just now", "hour", "minute")):
        return today
    return None


def content_sort_key(item: ContentItem, *, score_first: bool) -> tuple:
    safe_date = item.date or date.min
    if score_first:
        return (-round(item.score, 6), -safe_date.toordinal(), item.title.lower(), item.id)
    return (-safe_date.toordinal(), item.title.lower(), item.id)


def stable_sort(items: Iterable[ContentItem], *, score_first: bool) -> list[ContentItem]:
    return sorted(items, key=lambda item: content_sort_key(item, score_first=score_first))


def build_filename(item: ContentItem) -> str:
    stamp = item.date.strftime("%Y-%m-%d") if item.date and item.upload_date else "no-date"
    return f"{slugify(item.title)}-{stamp}.md"


def output_date(item: ContentItem) -> Optional[date]:
    return item.date if item.date and item.upload_date else None


def is_short(item: ContentItem) -> bool:
    return (
        item.type == "short"
        or "/shorts/" in item.url
        or item.source_tab == "shorts"
        or 0 < item.duration <= SHORT_THRESHOLD_SECONDS
    )


def prune_markdown_files(directory: Path) -> None:
    if not directory.exists():
        return
    for path in directory.glob("*.md"):
        path.unlink()


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path
