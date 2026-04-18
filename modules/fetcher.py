"""
fetcher.py — YouTube channel data extraction via yt-dlp
Extracts ALL videos and shorts with full metadata.
"""

import logging
import time
from typing import Optional
import yt_dlp

logger = logging.getLogger(__name__)


def _build_ydl_opts(cookies_file: Optional[str] = None) -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "ignoreerrors": True,
        "skip_download": True,
        "writesubtitles": False,
        "writethumbnail": False,
        "retries": 5,
        "fragment_retries": 5,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        },
    }
    if cookies_file:
        opts["cookiefile"] = cookies_file
    return opts


def resolve_channel_url(channel_input: str) -> str:
    """Normalize various channel input formats to a standard URL."""
    channel_input = channel_input.strip()
    if channel_input.startswith("http"):
        return channel_input
    if channel_input.startswith("@"):
        return f"https://www.youtube.com/{channel_input}"
    if channel_input.startswith("UC"):
        return f"https://www.youtube.com/channel/{channel_input}"
    return f"https://www.youtube.com/@{channel_input}"


def get_channel_name(channel_url: str, cookies_file: Optional[str] = None) -> str:
    """Extract channel name/handle for directory naming."""
    opts = _build_ydl_opts(cookies_file)
    opts["extract_flat"] = "in_playlist"
    opts["playlistend"] = 1
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(channel_url + "/videos", download=False)
            if info:
                uploader = info.get("uploader") or info.get("channel") or "unknown_channel"
                return uploader.strip().replace(" ", "_").lower()
    except Exception as e:
        logger.warning(f"Could not resolve channel name: {e}")
    return "unknown_channel"


def fetch_video_metadata(
    video_url: str,
    ydl: yt_dlp.YoutubeDL,
    retries: int = 3,
) -> Optional[dict]:
    """Fetch full metadata for a single video with retry logic."""
    for attempt in range(1, retries + 1):
        try:
            info = ydl.extract_info(video_url, download=False)
            if not info:
                return None
            return info
        except yt_dlp.utils.DownloadError as e:
            logger.debug(f"Attempt {attempt}/{retries} failed for {video_url}: {e}")
            if attempt < retries:
                time.sleep(2 * attempt)
        except Exception as e:
            logger.debug(f"Unexpected error for {video_url}: {e}")
            break
    return None


def fetch_channel_videos(
    channel_input: str,
    cookies_file: Optional[str] = None,
    progress_callback=None,
) -> tuple[list[dict], str]:
    """
    Fetch ALL videos and shorts from a channel.

    Returns:
        (list of raw video dicts, channel_name string)
    """
    channel_url = resolve_channel_url(channel_input)
    logger.info(f"Resolved channel URL: {channel_url}")

    # ── Step 1: flat-fetch ALL video URLs from /videos and /shorts tabs ──
    flat_opts = _build_ydl_opts(cookies_file)
    flat_opts["extract_flat"] = True
    flat_opts["ignoreerrors"] = True

    all_entries = []
    channel_name = "unknown_channel"
    tabs = ["/videos", "/shorts"]

    for tab in tabs:
        tab_url = channel_url + tab
        logger.info(f"Scanning tab: {tab_url}")
        try:
            with yt_dlp.YoutubeDL(flat_opts) as ydl:
                info = ydl.extract_info(tab_url, download=False)
                if info and "entries" in info:
                    entries = [e for e in info["entries"] if e]
                    all_entries.extend(entries)
                    if channel_name == "unknown_channel":
                        channel_name = (
                            info.get("uploader")
                            or info.get("channel")
                            or "unknown_channel"
                        )
                    logger.info(f"  → Found {len(entries)} items in {tab}")
        except Exception as e:
            logger.warning(f"Error scanning {tab_url}: {e}")

    # Deduplicate by video ID
    seen_ids = set()
    unique_entries = []
    for e in all_entries:
        vid_id = e.get("id") or e.get("url", "")
        if vid_id and vid_id not in seen_ids:
            seen_ids.add(vid_id)
            unique_entries.append(e)

    logger.info(f"Total unique videos found: {len(unique_entries)}")

    if not unique_entries:
        logger.warning("No videos found. The channel may be private or the URL is incorrect.")
        return [], channel_name

    # ── Step 2: fetch full metadata for each video ──
    full_opts = _build_ydl_opts(cookies_file)
    full_opts["extract_flat"] = False

    videos = []
    total = len(unique_entries)

    with yt_dlp.YoutubeDL(full_opts) as ydl:
        for idx, entry in enumerate(unique_entries, 1):
            vid_id = entry.get("id") or entry.get("url", "")
            video_url = (
                entry.get("url")
                if entry.get("url", "").startswith("http")
                else f"https://www.youtube.com/watch?v={vid_id}"
            )

            logger.debug(f"[{idx}/{total}] Fetching: {video_url}")

            if progress_callback:
                progress_callback(idx, total, entry.get("title", video_url))

            meta = fetch_video_metadata(video_url, ydl)
            if meta:
                videos.append(meta)
            else:
                logger.warning(f"Skipped (no metadata): {video_url}")

    logger.info(f"Successfully fetched metadata for {len(videos)} videos")
    return videos, channel_name.strip().replace(" ", "_").lower()
