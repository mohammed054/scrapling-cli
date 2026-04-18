"""
transcript.py — Transcript extraction with multi-tier fallback.

Priority:
  1. youtube-transcript-api (preferred — clean, formatted)
  2. yt-dlp subtitle extraction
  3. "Transcript not available"
"""

import logging
import re
import time
from typing import Optional

logger = logging.getLogger(__name__)

_TRANSCRIPT_API_AVAILABLE = False
try:
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
    _TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    logger.warning("youtube-transcript-api not installed; falling back to yt-dlp subtitles only.")


def _clean_transcript_text(text: str) -> str:
    """Remove duplicate lines, excessive whitespace, and VTT artifacts."""
    lines = text.splitlines()
    seen = set()
    clean = []
    for line in lines:
        line = line.strip()
        # Skip VTT timing lines and tags
        if re.match(r"^\d{2}:\d{2}|^WEBVTT|^Kind:|^Language:|^<\d", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)  # strip HTML tags
        line = re.sub(r"\s+", " ", line).strip()
        if line and line not in seen:
            seen.add(line)
            clean.append(line)
    return " ".join(clean)


def _fetch_via_transcript_api(video_id: str) -> Optional[str]:
    """Attempt transcript fetch using youtube-transcript-api."""
    if not _TRANSCRIPT_API_AVAILABLE:
        return None
    try:
        # Prefer English; fall back to auto-generated; fall back to any available
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None

        try:
            transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
        except Exception:
            pass

        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(["en", "en-US"])
            except Exception:
                pass

        if transcript is None:
            # Just grab whatever is available first
            for t in transcript_list:
                transcript = t
                break

        if transcript is None:
            return None

        data = transcript.fetch()
        text = " ".join(entry["text"] for entry in data)
        return _clean_transcript_text(text)

    except Exception as e:
        logger.debug(f"transcript-api failed for {video_id}: {e}")
        return None


def _fetch_via_yt_dlp(video_url: str) -> Optional[str]:
    """Fallback: extract subtitles using yt-dlp."""
    try:
        import yt_dlp
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en", "en-US"],
                "subtitlesformat": "vtt",
                "outtmpl": os.path.join(tmpdir, "sub"),
                "ignoreerrors": True,
            }
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([video_url])

            for fname in os.listdir(tmpdir):
                if fname.endswith(".vtt"):
                    with open(os.path.join(tmpdir, fname), "r", encoding="utf-8", errors="ignore") as f:
                        raw = f.read()
                    cleaned = _clean_transcript_text(raw)
                    if cleaned:
                        return cleaned

    except Exception as e:
        logger.debug(f"yt-dlp subtitle fallback failed for {video_url}: {e}")
    return None


def fetch_transcript(video_id: str, video_url: str, retries: int = 2) -> str:
    """
    Fetch transcript for a video with full fallback chain.
    Returns clean text or 'Transcript not available'.
    """
    for attempt in range(1, retries + 1):
        # ── Tier 1: youtube-transcript-api ──
        result = _fetch_via_transcript_api(video_id)
        if result:
            logger.debug(f"Transcript via transcript-api: {video_id}")
            return result

        # ── Tier 2: yt-dlp subtitles ──
        result = _fetch_via_yt_dlp(video_url)
        if result:
            logger.debug(f"Transcript via yt-dlp subtitles: {video_id}")
            return result

        if attempt < retries:
            logger.debug(f"Transcript attempt {attempt} failed for {video_id}, retrying…")
            time.sleep(1)

    logger.debug(f"No transcript available: {video_id}")
    return "Transcript not available"


def enrich_with_transcripts(
    items: list[dict],
    progress_callback=None,
) -> list[dict]:
    """Fetch and attach transcripts to a list of VideoRecord dicts (in-place)."""
    total = len(items)
    for idx, item in enumerate(items, 1):
        if progress_callback:
            progress_callback(idx, total, item.get("title", ""))
        item["transcript"] = fetch_transcript(item["id"], item["url"])
    return items
