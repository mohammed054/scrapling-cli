"""
classifier.py — Content type classification and metadata normalization.
Converts raw yt-dlp info dicts into clean VideoRecord dicts.
"""

import logging
import re
from datetime import datetime, date
from typing import Optional

logger = logging.getLogger(__name__)

SHORT_THRESHOLD_SECONDS = 60  # < 60s → short


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _parse_date(raw_date: str) -> Optional[date]:
    """Parse yt-dlp upload_date (YYYYMMDD) to a date object."""
    if not raw_date:
        return None
    try:
        return datetime.strptime(str(raw_date), "%Y%m%d").date()
    except ValueError:
        return None


def normalize_video(raw: dict) -> Optional[dict]:
    """
    Convert raw yt-dlp info dict to a clean VideoRecord.
    Returns None for invalid/private/deleted videos.
    """
    vid_id = raw.get("id", "")
    title = raw.get("title", "").strip()

    # Skip clearly invalid entries
    if not vid_id or not title or title in ("[Deleted video]", "[Private video]"):
        logger.debug(f"Skipping invalid entry: {vid_id!r} / {title!r}")
        return None

    duration = _safe_int(raw.get("duration"), 0)
    views = _safe_int(raw.get("view_count"), 0)
    likes = _safe_int(raw.get("like_count"), 0)
    comments = _safe_int(raw.get("comment_count"), 0)
    upload_date = _parse_date(raw.get("upload_date"))

    video_type = "short" if 0 < duration < SHORT_THRESHOLD_SECONDS else "video"
    # Also check YouTube's own "shorts" flag if available
    if raw.get("webpage_url", "").find("/shorts/") != -1:
        video_type = "short"

    url = raw.get("webpage_url") or raw.get("url") or f"https://www.youtube.com/watch?v={vid_id}"

    description = raw.get("description") or ""

    return {
        "id": vid_id,
        "title": title,
        "views": views,
        "likes": likes,
        "comments": comments,
        "date": upload_date,
        "duration": duration,
        "type": video_type,
        "url": url,
        "description": description,
        "transcript": "",  # filled later
        "score": 0.0,      # filled by scorer
        "channel": raw.get("uploader") or raw.get("channel") or "",
    }


def classify_all(raw_videos: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Normalize and split raw video list into (videos, shorts).
    Skips invalid entries.
    """
    videos = []
    shorts = []
    skipped = 0

    for raw in raw_videos:
        record = normalize_video(raw)
        if record is None:
            skipped += 1
            continue
        if record["type"] == "short":
            shorts.append(record)
        else:
            videos.append(record)

    logger.info(
        f"Classification: {len(videos)} videos, {len(shorts)} shorts, {skipped} skipped"
    )
    return videos, shorts
