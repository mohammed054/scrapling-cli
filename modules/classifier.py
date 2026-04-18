"""
classifier.py — Normalise raw fetcher dicts into full VideoRecord dicts
and split them into (videos, shorts).

Works with data produced by the Scrapling-based fetcher (no yt-dlp).
"""

import logging
import re
from datetime import datetime, date, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

SHORT_THRESHOLD_SECONDS = 62   # YouTube Shorts ≤ 60 s; give a tiny buffer


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _parse_date(raw_date) -> Optional[date]:
    """Accept YYYYMMDD str, YYYY-MM-DD str, or date object."""
    if raw_date is None:
        return None
    if isinstance(raw_date, date):
        return raw_date
    s = str(raw_date).strip()
    # YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s[:10] if "T" in s else s, fmt).date()
        except ValueError:
            continue
    return None


_RELATIVE_PATTERNS = [
    # (regex, days_multiplier)
    (re.compile(r"(\d+)\s*year"),  365),
    (re.compile(r"(\d+)\s*month"), 30),
    (re.compile(r"(\d+)\s*week"),  7),
    (re.compile(r"(\d+)\s*day"),   1),
]


def _approx_date_from_relative(relative: str) -> Optional[date]:
    """
    Convert 'X years ago', '3 months ago' etc. into an approximate date.
    Returns None if the string doesn't match any pattern.
    """
    if not relative:
        return None
    s = relative.lower()
    today = date.today()
    for pattern, mult in _RELATIVE_PATTERNS:
        m = pattern.search(s)
        if m:
            n = int(m.group(1))
            return today - timedelta(days=n * mult)
    if "yesterday" in s:
        return today - timedelta(days=1)
    if "today" in s or "just now" in s or "hour" in s or "minute" in s:
        return today
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Normalisation
# ─────────────────────────────────────────────────────────────────────────────

def normalize_video(raw: dict) -> Optional[dict]:
    """
    Convert a raw dict (from fetcher) to a canonical VideoRecord dict.
    Returns None for invalid / private / deleted entries.
    """
    vid_id = raw.get("id", "").strip()
    title = (raw.get("title") or "").strip()

    if not vid_id or not title or title in ("[Deleted video]", "[Private video]"):
        logger.debug(f"Skipping: id={vid_id!r} title={title!r}")
        return None

    duration = _safe_int(raw.get("duration"), 0)
    views    = _safe_int(raw.get("views"), 0)
    likes    = _safe_int(raw.get("likes"), 0)
    comments = _safe_int(raw.get("comments"), 0)

    # Resolve upload date: prefer exact date, fall back to relative text
    upload_date = (
        _parse_date(raw.get("upload_date"))
        or _approx_date_from_relative(raw.get("published_relative", ""))
    )

    # Classify type
    force_short = raw.get("_is_short", False)
    is_short_url = "/shorts/" in (raw.get("url") or "")
    is_short_dur = 0 < duration <= SHORT_THRESHOLD_SECONDS
    video_type = "short" if (force_short or is_short_url or is_short_dur) else "video"

    url = raw.get("url") or f"https://www.youtube.com/watch?v={vid_id}"

    return {
        "id":            vid_id,
        "title":         title,
        "views":         views,
        "likes":         likes,
        "comments":      comments,
        "date":          upload_date,
        "duration":      duration,
        "type":          video_type,
        "url":           url,
        "description":   (raw.get("description") or "").strip(),
        "transcript":    "",         # filled by transcript module
        "score":         0.0,        # filled by scorer
        "channel":       raw.get("channel", ""),
        "channel_url":   raw.get("channel_url", ""),
        "subscribers":   _safe_int(raw.get("subscribers"), 0),
        "thumbnail":     raw.get("thumbnail", ""),
        "tags":          list(raw.get("tags") or []),
        "category":      raw.get("category", ""),
        "language":      raw.get("language", ""),
        "age_limit":     _safe_int(raw.get("age_limit"), 0),
        "chapters":      raw.get("chapters", []),
        "top_comments":  raw.get("top_comments", []),
        "like_ratio":    round(likes / max(views, 1) * 100, 4),
        "comment_ratio": round(comments / max(views, 1) * 100, 4),
        "_score_components": {},
    }


def classify_all(raw_videos: list[dict]) -> tuple[list[dict], list[dict]]:
    """Normalise and split into (videos, shorts). Skips invalid entries."""
    videos: list[dict] = []
    shorts: list[dict] = []
    skipped = 0

    for raw in raw_videos:
        record = normalize_video(raw)
        if record is None:
            skipped += 1
            continue
        (shorts if record["type"] == "short" else videos).append(record)

    logger.info(
        f"Classification: {len(videos)} videos, {len(shorts)} shorts, {skipped} skipped"
    )
    return videos, shorts
