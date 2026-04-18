"""
fetcher.py — YouTube channel data extraction via yt-dlp

TWO-PHASE STRATEGY (fast):
  Phase 1: Flat-scan ALL videos (fast playlist scan, no per-video requests)
           → gets view_count from playlist page for free
  Phase 2: Pre-filter to top (percent * CANDIDATE_MULTIPLIER) candidates by views
           → full metadata fetch ONLY for those candidates
  Result:  5811 videos at top-15% → ~870 full fetches instead of 5811
"""

import logging
import time
from typing import Optional, Callable
import yt_dlp

logger = logging.getLogger(__name__)

# Buffer multiplier: fetch 2.5x the target % so re-scoring with full
# metrics (likes, comments, engagement) can still find the real top X%
CANDIDATE_MULTIPLIER = 2.5


def _build_ydl_opts(cookies_file: Optional[str] = None, flat: bool = False) -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": flat,
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


def _flat_scan_tab(
    tab_url: str,
    cookies_file: Optional[str],
) -> tuple[list[dict], str]:
    """
    Fast flat scan of one channel tab.
    Returns (entries, channel_name).
    No per-video HTTP requests — reads playlist page only.
    """
    opts = _build_ydl_opts(cookies_file, flat=True)
    channel_name = "unknown_channel"
    entries = []
    logger.info(f"Flat scanning: {tab_url}")
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(tab_url, download=False)
            if info and "entries" in info:
                entries = [e for e in info["entries"] if e]
                channel_name = (
                    info.get("uploader")
                    or info.get("channel")
                    or "unknown_channel"
                )
                logger.info(f"  → Found {len(entries)} items")
    except Exception as e:
        logger.warning(f"Error scanning {tab_url}: {e}")
    return entries, channel_name


def _prefilter_candidates(entries: list[dict], target_percent: float) -> list[dict]:
    """
    Pre-filter flat entries to top candidates using view_count (available
    from the playlist scan — no extra requests needed).

    Keeps top (target_percent * CANDIDATE_MULTIPLIER)% by views as candidates.
    Falls back to all entries if view data is sparse.
    """
    with_views = [e for e in entries if e.get("view_count") is not None]
    without_views = [e for e in entries if e.get("view_count") is None]

    if len(with_views) < len(entries) * 0.5:
        logger.info(
            f"Pre-filter skipped: only {len(with_views)}/{len(entries)} "
            "entries have view_count in flat scan — fetching all"
        )
        return entries

    # Sort by views descending, take top buffer%
    with_views.sort(key=lambda e: e.get("view_count", 0), reverse=True)
    candidate_count = max(
        50,
        min(len(entries), int(len(entries) * (target_percent / 100) * CANDIDATE_MULTIPLIER)),
    )
    candidates = with_views[:candidate_count] + without_views

    saved = len(entries) - len(candidates)
    logger.info(
        f"Pre-filter: {len(entries)} total → {len(candidates)} candidates "
        f"({saved} low-view videos skipped, saving ~{saved} HTTP requests)"
    )
    return candidates


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
    top_percent: float = 15.0,
    cookies_file: Optional[str] = None,
    fetch_comments: int = 0,
    progress_callback: Optional[Callable] = None,
) -> tuple[list[dict], str]:
    """
    Two-phase channel fetch:
      1. Flat-scan all tabs (fast, no per-video requests)
      2. Pre-filter by views → full fetch only top candidates

    Returns:
        (list of full metadata dicts, channel_name string)
    """
    channel_url = resolve_channel_url(channel_input)
    logger.info(f"Resolved channel URL: {channel_url}")

    # ── PHASE 1: Fast flat scan ───────────────────────────────────────────────
    all_entries: list[dict] = []
    channel_name = "unknown_channel"

    for tab in ["/videos", "/shorts"]:
        entries, name = _flat_scan_tab(channel_url + tab, cookies_file)
        all_entries.extend(entries)
        if name != "unknown_channel":
            channel_name = name

    # Deduplicate by ID
    seen_ids: set[str] = set()
    unique_entries: list[dict] = []
    for e in all_entries:
        vid_id = e.get("id") or e.get("url", "")
        if vid_id and vid_id not in seen_ids:
            seen_ids.add(vid_id)
            unique_entries.append(e)

    logger.info(f"Total unique entries: {len(unique_entries)}")

    if not unique_entries:
        logger.warning("No videos found. Check channel URL or use --cookies.")
        return [], channel_name.strip().replace(" ", "_").lower()

    # ── PHASE 2: Pre-filter → full metadata for candidates only ──────────────
    candidates = _prefilter_candidates(unique_entries, top_percent)
    full_opts = _build_ydl_opts(cookies_file, flat=False)
    if fetch_comments > 0:
        full_opts["getcomments"] = True
        full_opts["extractor_args"] = {
            "youtube": {"max_comments": [str(fetch_comments), "0", "0", "0"]}
        }
    videos: list[dict] = []
    total = len(candidates)

    logger.info(f"Full metadata fetch: {total} candidates")

    with yt_dlp.YoutubeDL(full_opts) as ydl:
        for idx, entry in enumerate(candidates, 1):
            vid_id = entry.get("id") or entry.get("url", "")
            raw_url = entry.get("url", "")
            video_url = (
                raw_url if raw_url.startswith("http")
                else f"https://www.youtube.com/watch?v={vid_id}"
            )

            if progress_callback:
                progress_callback(idx, total, entry.get("title", video_url))

            logger.debug(f"[{idx}/{total}] Fetching: {video_url}")
            meta = fetch_video_metadata(video_url, ydl)
            if meta:
                videos.append(meta)
            else:
                logger.warning(f"Skipped (no metadata): {video_url}")

    logger.info(f"Successfully fetched full metadata for {len(videos)} videos")
    return videos, channel_name.strip().replace(" ", "_").lower()
