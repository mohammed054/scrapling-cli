"""
transcript.py — Transcript extraction with fallback chain.

Priority:
  1. youtube-transcript-api (official captions, auto-generated, multi-lang)
  2. Graceful "not available" message

Handles: missing transcripts, private videos, language fallbacks, retries.
"""

import logging
import time
from typing import Optional

log = logging.getLogger(__name__)

# Languages to try, in priority order
LANG_PRIORITY = ["en", "en-US", "en-GB", "en-AU"]

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 2.0   # seconds


class TranscriptFetcher:
    """
    Fetches transcripts for YouTube videos.
    Tries official captions first (manual, then auto-generated).
    Falls back to a placeholder if nothing is available.
    """

    def __init__(self):
        self._api_available = self._check_api()

    def get(self, url: str, video_id: str) -> str:
        """
        Public method: return transcript text for a video.
        Always returns a string (never raises).
        """
        if not video_id:
            video_id = self._extract_id(url)

        if not video_id:
            return "Transcript not available (could not determine video ID)"

        if self._api_available:
            result = self._fetch_with_api(video_id)
            if result:
                return result

        return "Transcript not available"

    # ------------------------------------------------------------------
    # Primary: youtube-transcript-api
    # ------------------------------------------------------------------

    def _fetch_with_api(self, video_id: str) -> Optional[str]:
        """Try youtube-transcript-api with retries."""
        from youtube_transcript_api import (
            YouTubeTranscriptApi,
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
        )

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # List available transcripts
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

                # Try manual transcripts first (higher quality)
                transcript = self._try_manual(transcript_list)

                # Fall back to auto-generated
                if not transcript:
                    transcript = self._try_auto(transcript_list)

                if transcript:
                    raw = transcript.fetch()
                    return self._format_transcript(raw)

                log.debug(f"No usable transcript for {video_id}")
                return None

            except (NoTranscriptFound, TranscriptsDisabled):
                log.debug(f"Transcripts disabled or not found for {video_id}")
                return None

            except VideoUnavailable:
                log.debug(f"Video unavailable: {video_id}")
                return None

            except Exception as e:
                log.warning(f"Transcript attempt {attempt}/{MAX_RETRIES} failed for {video_id}: {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * attempt)
                else:
                    return None

    def _try_manual(self, transcript_list) -> Optional[object]:
        """Try to get a manual transcript in preferred language order."""
        try:
            return transcript_list.find_manually_created_transcript(LANG_PRIORITY)
        except Exception:
            pass

        try:
            # Any manual transcript
            for t in transcript_list:
                if not t.is_generated:
                    return t
        except Exception:
            pass

        return None

    def _try_auto(self, transcript_list) -> Optional[object]:
        """Try to get an auto-generated transcript in preferred language order."""
        try:
            return transcript_list.find_generated_transcript(LANG_PRIORITY)
        except Exception:
            pass

        try:
            # Any auto-generated transcript
            for t in transcript_list:
                if t.is_generated:
                    return t
        except Exception:
            pass

        # Last resort: any transcript, translate to English
        try:
            for t in transcript_list:
                return t.translate("en")
        except Exception:
            pass

        return None

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    @staticmethod
    def _format_transcript(raw: list) -> str:
        """
        Convert list of {text, start, duration} dicts into readable paragraphs.
        Groups into ~120-second chunks for readability.
        """
        if not raw:
            return "Transcript not available"

        chunks = []
        current_chunk = []
        chunk_start = 0.0
        CHUNK_SECONDS = 120

        for segment in raw:
            text  = segment.get("text", "").strip()
            start = segment.get("start", 0)

            if not text:
                continue

            if start - chunk_start >= CHUNK_SECONDS and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                chunk_start = start

            current_chunk.append(text)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return "\n\n".join(chunks)

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _check_api() -> bool:
        try:
            import youtube_transcript_api  # noqa: F401
            return True
        except ImportError:
            log.warning(
                "youtube-transcript-api not installed. "
                "Transcripts will be unavailable. "
                "Run: pip install youtube-transcript-api"
            )
            return False

    @staticmethod
    def _extract_id(url: str) -> str:
        """Extract video ID from a YouTube URL."""
        import re
        patterns = [
            r"[?&]v=([a-zA-Z0-9_-]{11})",
            r"youtu\.be/([a-zA-Z0-9_-]{11})",
            r"shorts/([a-zA-Z0-9_-]{11})",
        ]
        for pattern in patterns:
            m = re.search(pattern, url)
            if m:
                return m.group(1)
        return ""
