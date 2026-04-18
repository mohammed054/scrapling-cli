"""
classifier.py — Content type classification and full metadata normalization.
Converts raw yt-dlp info dicts into rich VideoRecord dicts.
"""

import logging
from datetime import datetime, date
from typing import Optional

logger = logging.getLogger(__name__)

SHORT_THRESHOLD_SECONDS = 60


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _parse_date(raw_date) -> Optional[date]:
    if not raw_date:
        return None
    try:
        return datetime.strptime(str(raw_date), "%Y%m%d").date()
    except ValueError:
        return None


def _extract_chapters(raw: dict) -> list[dict]:
    """Extract chapter markers if available."""
    chapters = raw.get("chapters") or []
    result = []
    for ch in chapters:
        result.append({
            "title": ch.get("title", ""),
            "start": ch.get("start_time", 0),
            "end": ch.get("end_time", 0),
        })
    return result


def _extract_top_comments(raw: dict, limit: int = 10) -> list[dict]:
    """Extract top comments from yt-dlp comment data if fetched."""
    comments_data = raw.get("comments") or []
    result = []
    for c in comments_data[:limit]:
        result.append({
            "author": c.get("author", ""),
            "text": (c.get("text") or "").strip(),
            "likes": _safe_int(c.get("like_count"), 0),
            "is_pinned": c.get("is_pinned", False),
        })
    return result


def normalize_video(raw: dict) -> Optional[dict]:
    """
    Convert raw yt-dlp info dict to a full VideoRecord.
    Returns None for invalid/private/deleted videos.
    """
    vid_id = raw.get("id", "")
    title = (raw.get("title") or "").strip()

    if not vid_id or not title or title in ("[Deleted video]", "[Private video]"):
        logger.debug(f"Skipping invalid: {vid_id!r} / {title!r}")
        return None

    duration    = _safe_int(raw.get("duration"), 0)
    views       = _safe_int(raw.get("view_count"), 0)
    likes       = _safe_int(raw.get("like_count"), 0)
    comment_cnt = _safe_int(raw.get("comment_count"), 0)
    upload_date = _parse_date(raw.get("upload_date"))

    video_type = "short" if 0 < duration < SHORT_THRESHOLD_SECONDS else "video"
    if "/shorts/" in (raw.get("webpage_url") or raw.get("url") or ""):
        video_type = "short"

    url = (
        raw.get("webpage_url")
        or raw.get("url")
        or f"https://www.youtube.com/watch?v={vid_id}"
    )

    # Thumbnail — prefer highest quality
    thumbnail = raw.get("thumbnail") or ""
    thumbs = raw.get("thumbnails") or []
    if thumbs:
        best = max(thumbs, key=lambda t: (t.get("width") or 0) * (t.get("height") or 0))
        thumbnail = best.get("url") or thumbnail

    return {
        "id":            vid_id,
        "title":         title,
        "views":         views,
        "likes":         likes,
        "comments":      comment_cnt,
        "date":          upload_date,
        "duration":      duration,
        "type":          video_type,
        "url":           url,
        "description":   (raw.get("description") or "").strip(),
        "transcript":    "",                           # filled later
        "score":         0.0,                          # filled by scorer
        "channel":       raw.get("uploader") or raw.get("channel") or "",
        "channel_url":   raw.get("uploader_url") or raw.get("channel_url") or "",
        "subscribers":   _safe_int(raw.get("channel_follower_count"), 0),
        "thumbnail":     thumbnail,
        "tags":          list(raw.get("tags") or []),
        "category":      raw.get("categories", [None])[0] if raw.get("categories") else "",
        "language":      raw.get("language") or "",
        "age_limit":     _safe_int(raw.get("age_limit"), 0),
        "chapters":      _extract_chapters(raw),
        "top_comments":  _extract_top_comments(raw),
        "like_ratio":    round(likes / max(views, 1) * 100, 4),
        "comment_ratio": round(comment_cnt / max(views, 1) * 100, 4),
        "_score_components": {},
    }


def classify_all(raw_videos: list[dict]) -> tuple[list[dict], list[dict]]:
    """Normalize and split into (videos, shorts). Skips invalid entries."""
    videos, shorts, skipped = [], [], 0
    for raw in raw_videos:
        record = normalize_video(raw)
        if record is None:
            skipped += 1
            continue
        (shorts if record["type"] == "short" else videos).append(record)

    logger.info(f"Classification: {len(videos)} videos, {len(shorts)} shorts, {skipped} skipped")
    return videos, shorts
