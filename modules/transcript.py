"""
transcript.py — Transcript extraction via youtube-transcript-api.

No yt-dlp. The youtube-transcript-api calls YouTube's caption endpoint
directly and is fast, clean, and reliable.

Priority:
  1. Manually-created English transcript
  2. Auto-generated English transcript
  3. Any available transcript (auto-translated to English if needed)
  4. "Transcript not available"
"""

import logging
import re
import time
from typing import Optional

logger = logging.getLogger(__name__)

_API_AVAILABLE = False
_yta_instance = None  # reuse a single instance across calls
try:
    from youtube_transcript_api import (
        YouTubeTranscriptApi,
        TranscriptsDisabled,
        NoTranscriptFound,
    )
    _yta_instance = YouTubeTranscriptApi()
    _API_AVAILABLE = True
except ImportError:
    logger.warning(
        "youtube-transcript-api not installed. "
        "Install with: pip install youtube-transcript-api"
    )


def _clean(text: str) -> str:
    """Strip HTML tags, VTT artefacts, dedup blank lines."""
    lines = text.splitlines()
    seen: set[str] = set()
    clean: list[str] = []
    for line in lines:
        line = line.strip()
        if re.match(r"^\d{2}:\d{2}|^WEBVTT|^Kind:|^Language:|^<\d", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line and line not in seen:
            seen.add(line)
            clean.append(line)
    return " ".join(clean)


def fetch_transcript(video_id: str, _video_url: str = "", retries: int = 2) -> str:
    """
    Fetch transcript for a video.
    Returns clean text or 'Transcript not available'.
    `_video_url` is accepted for API-compatibility but unused here.
    """
    if not _API_AVAILABLE:
        return "Transcript not available (youtube-transcript-api not installed)"

    for attempt in range(1, retries + 1):
        try:
            # youtube-transcript-api v0.6+ dropped the static list_transcripts()
            # method — use an instance and call .list() instead.
            tl = _yta_instance.list(video_id)
            transcript = None

            # 1. Manual English
            try:
                transcript = tl.find_manually_created_transcript(["en", "en-US", "en-GB"])
            except Exception:
                pass

            # 2. Auto-generated English
            if transcript is None:
                try:
                    transcript = tl.find_generated_transcript(["en", "en-US"])
                except Exception:
                    pass

            # 3. Any available (translate to English)
            if transcript is None:
                for t in tl:
                    try:
                        transcript = t.translate("en")
                    except Exception:
                        transcript = t
                    break

            if transcript is None:
                return "Transcript not available"

            entries = transcript.fetch()
            # v1.x returns Snippet objects (use .text attribute);
            # older versions returned dicts (use ["text"]).  Handle both.
            parts = []
            for e in entries:
                text = getattr(e, "text", None)
                if text is None and isinstance(e, dict):
                    text = e.get("text", "")
                if text:
                    parts.append(text)
            raw = " ".join(parts)
            cleaned = _clean(raw)
            logger.debug(f"Transcript fetched: {video_id} ({len(cleaned)} chars)")
            return cleaned if cleaned else "Transcript not available"

        except (TranscriptsDisabled, NoTranscriptFound):
            return "Transcript not available"
        except Exception as e:
            logger.debug(f"Transcript attempt {attempt} failed for {video_id}: {e}")
            if attempt < retries:
                time.sleep(1.5)

    return "Transcript not available"


def enrich_with_transcripts(
    items: list[dict],
    progress_callback=None,
) -> list[dict]:
    """Attach transcripts to a list of VideoRecord dicts (in-place)."""
    total = len(items)
    for idx, item in enumerate(items, 1):
        if progress_callback:
            progress_callback(idx, total, item.get("title", ""))
        item["transcript"] = fetch_transcript(item["id"], item.get("url", ""))
    return items