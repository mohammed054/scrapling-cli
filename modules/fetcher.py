"""
fetcher.py — YouTube channel data extraction via Scrapling.

Strategy:
  1. Fetch channel /videos and /shorts tabs using Scrapling's Fetcher
     (fast HTTP with stealthy headers — no browser required for initial load)
  2. Extract ytInitialData JSON embedded in the page <script> tags
  3. Paginate via YouTube's InnerTube API (POST /youtubei/v1/browse)
     using continuation tokens found in ytInitialData
  4. Optionally fetch individual video pages for richer metadata
     (description, chapters, subscriber count, etc.)

No yt-dlp. No Selenium. Pure Scrapling.
"""

import json
import logging
import re
import time
from typing import Optional, Callable

from scrapling.fetchers import Fetcher, StealthyFetcher

logger = logging.getLogger(__name__)

# ── InnerTube client context (mimics YouTube web frontend) ────────────────────
INNERTUBE_CONTEXT = {
    "client": {
        "clientName": "WEB",
        "clientVersion": "2.20240815.01.00",
        "hl": "en",
        "gl": "US",
    }
}

INNERTUBE_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

COMMON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# ─────────────────────────────────────────────────────────────────────────────
# URL helpers
# ─────────────────────────────────────────────────────────────────────────────

def resolve_channel_url(channel_input: str) -> str:
    """Normalise @handle / full URL / UC-ID to a canonical YouTube URL."""
    s = channel_input.strip()
    if s.startswith("http"):
        return s.rstrip("/")
    if s.startswith("@"):
        return f"https://www.youtube.com/{s}"
    if s.startswith("UC"):
        return f"https://www.youtube.com/channel/{s}"
    return f"https://www.youtube.com/@{s}"


# ─────────────────────────────────────────────────────────────────────────────
# Page fetching
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_page(url: str, retries: int = 3, use_stealth: bool = False) -> Optional[object]:
    """
    Fetch a URL with Scrapling.
    Tries Fetcher (fast HTTP) first; falls back to StealthyFetcher on failure.
    Returns a Scrapling page object or None.
    """
    for attempt in range(1, retries + 1):
        try:
            if use_stealth:
                page = StealthyFetcher.fetch(
                    url, headless=True, network_idle=True,
                    extra_headers=COMMON_HEADERS,
                )
            else:
                page = Fetcher.get(
                    url,
                    stealthy_headers=True,
                    extra_headers=COMMON_HEADERS,
                )
            if page and page.status == 200:
                return page
            logger.debug(f"HTTP {page.status if page else '?'} on attempt {attempt}: {url}")
        except Exception as e:
            logger.debug(f"Fetch attempt {attempt} failed ({url}): {e}")
        if attempt < retries:
            time.sleep(2 ** attempt)

    # Last resort — stealth browser
    if not use_stealth:
        logger.info(f"Retrying with StealthyFetcher: {url}")
        return _fetch_page(url, retries=2, use_stealth=True)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# ytInitialData extraction
# ─────────────────────────────────────────────────────────────────────────────

_YT_INITIAL_DATA_RE = re.compile(
    r'(?:var\s+ytInitialData|window\["ytInitialData"\])\s*=\s*(\{.+?\});\s*</script>',
    re.DOTALL,
)
_YT_INITIAL_PLAYER_RE = re.compile(
    r'ytInitialPlayerResponse\s*=\s*(\{.+?\});\s*(?:var|</script>)',
    re.DOTALL,
)


def _extract_json_from_scripts(page, pattern: re.Pattern) -> Optional[dict]:
    """Search all <script> tags for a JSON blob matching `pattern`."""
    for script in page.css("script"):
        raw = script.text or ""
        if not raw:
            continue
        m = pattern.search(raw)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError as e:
                logger.debug(f"JSON parse error: {e}")
    return None


def get_yt_initial_data(page) -> dict:
    data = _extract_json_from_scripts(page, _YT_INITIAL_DATA_RE)
    if data is None:
        logger.warning("ytInitialData not found in page scripts")
        return {}
    return data


def get_yt_initial_player(page) -> dict:
    data = _extract_json_from_scripts(page, _YT_INITIAL_PLAYER_RE)
    return data or {}


# ─────────────────────────────────────────────────────────────────────────────
# ytInitialData → video record parsing
# ─────────────────────────────────────────────────────────────────────────────

def _safe_text(obj, *keys, default: str = "") -> str:
    """Navigate nested dicts/lists and return a string value safely."""
    cur = obj
    for k in keys:
        if cur is None:
            return default
        if isinstance(cur, dict):
            cur = cur.get(k)
        elif isinstance(cur, list) and isinstance(k, int):
            cur = cur[k] if k < len(cur) else None
        else:
            return default
    return str(cur).strip() if cur is not None else default


def _parse_view_count(text: str) -> int:
    """Convert '1.2M views', '42,000 views', '1,234' → int."""
    if not text:
        return 0
    s = text.lower().replace("views", "").replace(",", "").strip()
    try:
        if s.endswith("k"):
            return int(float(s[:-1]) * 1_000)
        if s.endswith("m"):
            return int(float(s[:-1]) * 1_000_000)
        if s.endswith("b"):
            return int(float(s[:-1]) * 1_000_000_000)
        return int(float(s))
    except (ValueError, TypeError):
        return 0


def _parse_duration_text(text: str) -> int:
    """'10:23' or '1:02:45' → seconds."""
    if not text:
        return 0
    parts = [int(p) for p in text.strip().split(":") if p.isdigit()]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 1:
        return parts[0]
    return 0


def _parse_subscriber_text(text: str) -> int:
    """'1.2M subscribers' → int."""
    return _parse_view_count(text.replace("subscribers", "").replace("subscriber", ""))


def _extract_text_runs(runs_obj) -> str:
    """Concatenate YouTube 'runs' arrays into a plain string."""
    if not runs_obj:
        return ""
    runs = runs_obj if isinstance(runs_obj, list) else runs_obj.get("runs", [])
    return "".join(r.get("text", "") for r in runs if isinstance(r, dict))


def _extract_thumbnail(renderer: dict) -> str:
    """Pick the highest-resolution thumbnail URL."""
    thumbs = (
        renderer.get("thumbnail", {}).get("thumbnails")
        or renderer.get("channelThumbnailSupportedRenderers", {})
           .get("channelThumbnailWithLinkRenderer", {})
           .get("thumbnail", {}).get("thumbnails")
        or []
    )
    if thumbs:
        best = max(thumbs, key=lambda t: (t.get("width") or 0) * (t.get("height") or 0))
        return best.get("url", "")
    return ""


def _renderer_to_raw(renderer: dict, is_short: bool = False) -> Optional[dict]:
    """
    Convert a raw videoRenderer / reelItemRenderer dict to our internal raw dict.
    Returns None if the entry is invalid (deleted / private / no ID).
    """
    vid_id = renderer.get("videoId") or renderer.get("reelWatchEndpoint", {}).get("videoId")
    if not vid_id:
        return None

    title = (
        _extract_text_runs(renderer.get("title"))
        or _safe_text(renderer, "headline", "simpleText")
    ).strip()
    if not title or title in ("[Deleted video]", "[Private video]"):
        return None

    # Duration
    duration_text = (
        _safe_text(renderer, "lengthText", "simpleText")
        or _safe_text(renderer, "thumbnailOverlays", 0,
                      "thumbnailOverlayTimeStatusRenderer", "text", "simpleText")
    )
    duration = _parse_duration_text(duration_text)

    # Views — multiple possible fields
    view_text = (
        _safe_text(renderer, "viewCountText", "simpleText")
        or _safe_text(renderer, "shortViewCountText", "simpleText")
    )
    views = _parse_view_count(view_text)

    # Published time (relative — we'll store as string; exact dates come from video pages)
    published_relative = (
        _safe_text(renderer, "publishedTimeText", "simpleText")
        or _safe_text(renderer, "relativePublishedTime")
    )

    # URL
    url = (
        renderer.get("navigationEndpoint", {})
                .get("commandMetadata", {})
                .get("webCommandMetadata", {})
                .get("url", "")
    )
    if url and not url.startswith("http"):
        url = f"https://www.youtube.com{url}"
    if not url:
        if is_short:
            url = f"https://www.youtube.com/shorts/{vid_id}"
        else:
            url = f"https://www.youtube.com/watch?v={vid_id}"

    return {
        "id": vid_id,
        "title": title,
        "views": views,
        "likes": 0,           # not on listing pages; filled by video-page fetch
        "comments": 0,        # same
        "duration": duration,
        "url": url,
        "thumbnail": _extract_thumbnail(renderer),
        "published_relative": published_relative,
        "description": "",
        "tags": [],
        "category": "",
        "language": "",
        "chapters": [],
        "top_comments": [],
        "channel": "",
        "channel_url": "",
        "subscribers": 0,
        "_is_short": is_short or (0 < duration <= 60),
        # upload_date filled later if we do per-video fetches
        "upload_date": None,
    }


def _walk_grid_contents(contents: list) -> tuple[list[dict], Optional[str]]:
    """
    Walk richGridRenderer / gridRenderer contents.
    Returns ([raw_video_dict, ...], continuation_token_or_None).
    """
    items = []
    continuation = None

    for item in contents:
        # richItemRenderer wraps the actual content
        inner = (
            item.get("richItemRenderer", {}).get("content")
            or item.get("gridVideoRenderer")
            or item
        )

        vr = (
            inner.get("videoRenderer")
            or inner.get("gridVideoRenderer")
        )
        if vr:
            raw = _renderer_to_raw(vr, is_short=False)
            if raw:
                items.append(raw)
            continue

        # Reels / shorts shelf
        rr = inner.get("reelItemRenderer")
        if rr:
            raw = _renderer_to_raw(rr, is_short=True)
            if raw:
                items.append(raw)
            continue

        # Continuation token
        ct = item.get("continuationItemRenderer")
        if ct:
            token = (
                ct.get("continuationEndpoint", {})
                  .get("continuationCommand", {})
                  .get("token")
            )
            if token:
                continuation = token

    return items, continuation


def _extract_tab_contents(yt_data: dict, tab_name: str) -> tuple[list[dict], Optional[str], str]:
    """
    Extract video list + continuation token from ytInitialData for a given tab.
    Returns (items, continuation_token, channel_name).
    """
    channel_name = ""
    items = []
    continuation = None

    try:
        # Channel name
        header = yt_data.get("header", {})
        c4h = header.get("c4TabbedHeaderRenderer", {})
        channel_name = c4h.get("title", "") or _safe_text(yt_data, "metadata",
                                "channelMetadataRenderer", "title")

        tabs = (
            yt_data.get("contents", {})
                   .get("twoColumnBrowseResultsRenderer", {})
                   .get("tabs", [])
        )

        for tab in tabs:
            tr = tab.get("tabRenderer", {})
            title = tr.get("title", "").lower()
            if tab_name == "videos" and title not in ("videos", "home"):
                continue
            if tab_name == "shorts" and title != "shorts":
                continue

            content = tr.get("content", {})

            # richGridRenderer (most common)
            rgr = content.get("richGridRenderer", {})
            if rgr:
                items, continuation = _walk_grid_contents(rgr.get("contents", []))
                break

            # sectionListRenderer fallback
            slr = content.get("sectionListRenderer", {})
            if slr:
                for section in slr.get("contents", []):
                    isr = section.get("itemSectionRenderer", {})
                    for c in isr.get("contents", []):
                        gr = c.get("gridRenderer", {})
                        if gr:
                            more, tok = _walk_grid_contents(gr.get("items", []))
                            items.extend(more)
                            if tok:
                                continuation = tok
                break

    except Exception as e:
        logger.warning(f"Error parsing ytInitialData tab '{tab_name}': {e}")

    return items, continuation, channel_name


# ─────────────────────────────────────────────────────────────────────────────
# InnerTube API pagination
# ─────────────────────────────────────────────────────────────────────────────

def _innertube_browse(continuation_token: str, retries: int = 3) -> Optional[dict]:
    """POST to YouTube's InnerTube /browse endpoint to get next page."""
    url = f"https://www.youtube.com/youtubei/v1/browse?key={INNERTUBE_KEY}"
    payload = {
        "context": INNERTUBE_CONTEXT,
        "continuation": continuation_token,
    }
    for attempt in range(1, retries + 1):
        try:
            resp = Fetcher.post(
                url,
                json=payload,
                extra_headers={
                    **COMMON_HEADERS,
                    "Content-Type": "application/json",
                    "X-YouTube-Client-Name": "1",
                    "X-YouTube-Client-Version": "2.20240815.01.00",
                },
            )
            if resp and resp.status == 200:
                return json.loads(resp.content)
        except Exception as e:
            logger.debug(f"InnerTube attempt {attempt} failed: {e}")
        if attempt < retries:
            time.sleep(2 * attempt)
    return None


def _extract_continuation_items(browse_data: dict) -> tuple[list[dict], Optional[str]]:
    """Extract items + next continuation token from an InnerTube browse response."""
    items = []
    continuation = None

    try:
        # Structure: onResponseReceivedActions[0].appendContinuationItemsAction.continuationItems
        for action in browse_data.get("onResponseReceivedActions", []):
            acia = action.get("appendContinuationItemsAction", {})
            cont_items = acia.get("continuationItems", [])
            if cont_items:
                more, tok = _walk_grid_contents(cont_items)
                items.extend(more)
                if tok:
                    continuation = tok
                break
    except Exception as e:
        logger.debug(f"Error extracting continuation items: {e}")

    return items, continuation


# ─────────────────────────────────────────────────────────────────────────────
# Individual video page enrichment
# ─────────────────────────────────────────────────────────────────────────────

def _parse_upload_date_from_player(player_data: dict) -> Optional[str]:
    """Extract upload date string (YYYYMMDD or ISO) from ytInitialPlayerResponse."""
    micro = player_data.get("microformat", {}).get("playerMicroformatRenderer", {})
    pub = micro.get("publishDate") or micro.get("uploadDate")
    if pub:
        return pub.replace("-", "")  # → YYYYMMDD
    return None


def _parse_likes_from_data(yt_data: dict) -> int:
    """
    Extract like count from ytInitialData on a video page.
    YouTube hides exact counts; we parse the accessibility label.
    """
    try:
        contents = (
            yt_data.get("contents", {})
                   .get("twoColumnWatchNextResults", {})
                   .get("results", {})
                   .get("results", {})
                   .get("contents", [])
        )
        for c in contents:
            pir = c.get("videoPrimaryInfoRenderer", {})
            if not pir:
                continue
            # Dig into videoActions → segmentedLikeDislikeButtonViewModel
            actions = pir.get("videoActions", {})
            menu = actions.get("menuRenderer", {})
            for item in menu.get("topLevelButtons", []):
                # segmentedLikeDislikeButtonViewModel
                sldvm = (
                    item.get("segmentedLikeDislikeButtonViewModel", {})
                        .get("likeButtonViewModel", {})
                        .get("likeButtonViewModel", {})
                        .get("toggleButtonViewModel", {})
                        .get("toggleButtonViewModel", {})
                        .get("defaultButtonViewModel", {})
                        .get("buttonViewModel", {})
                )
                label = sldvm.get("accessibilityText", "") or sldvm.get("title", "")
                count = _parse_view_count(label.replace("like", "").replace("this video", ""))
                if count:
                    return count
    except Exception:
        pass
    return 0


def _parse_description_from_data(yt_data: dict) -> str:
    """Extract description from ytInitialData on a video page."""
    try:
        contents = (
            yt_data.get("contents", {})
                   .get("twoColumnWatchNextResults", {})
                   .get("results", {})
                   .get("results", {})
                   .get("contents", [])
        )
        for c in contents:
            vsir = c.get("videoSecondaryInfoRenderer", {})
            if not vsir:
                continue
            desc = vsir.get("description", {})
            return _extract_text_runs(desc.get("runs", []))
    except Exception:
        pass
    return ""


def _parse_chapters_from_player(player_data: dict) -> list[dict]:
    """Extract chapters from ytInitialPlayerResponse."""
    chapters = []
    try:
        chaps = (
            player_data.get("chapters", {})
                       .get("playerOverlayChapterRenderer", {})
                       .get("chapters", [])
        )
        for ch in chaps:
            cr = ch.get("chapterRenderer", {})
            chapters.append({
                "title": _extract_text_runs(cr.get("title", {}).get("runs", [])),
                "start": cr.get("timeRangeStartMillis", 0) // 1000,
                "end": 0,
            })
    except Exception:
        pass
    return chapters


def _parse_subscriber_from_data(yt_data: dict) -> int:
    """Extract subscriber count from video page ytInitialData."""
    try:
        contents = (
            yt_data.get("contents", {})
                   .get("twoColumnWatchNextResults", {})
                   .get("results", {})
                   .get("results", {})
                   .get("contents", [])
        )
        for c in contents:
            vsir = c.get("videoSecondaryInfoRenderer", {})
            if not vsir:
                continue
            sc = vsir.get("owner", {}).get("videoOwnerRenderer", {})
            st = _safe_text(sc, "subscriberCountText", "simpleText")
            return _parse_subscriber_text(st)
    except Exception:
        pass
    return 0


def enrich_video_page(raw: dict, retries: int = 2) -> dict:
    """
    Fetch an individual video page and enrich `raw` with:
    - exact upload date (from ytInitialPlayerResponse)
    - likes (from ytInitialData)
    - description, chapters (from ytInitialData / player)
    - subscriber count
    """
    url = raw.get("url", "")
    if not url:
        return raw

    for attempt in range(1, retries + 1):
        page = _fetch_page(url)
        if not page:
            if attempt < retries:
                time.sleep(2)
            continue

        yt_data = get_yt_initial_data(page)
        player_data = get_yt_initial_player(page)

        # Upload date
        raw_date = _parse_upload_date_from_player(player_data)
        if raw_date:
            raw["upload_date"] = raw_date

        # Likes
        likes = _parse_likes_from_data(yt_data)
        raw["likes"] = likes

        # Description (prefer player short description for compactness)
        desc = (
            player_data.get("videoDetails", {}).get("shortDescription", "")
            or _parse_description_from_data(yt_data)
        )
        raw["description"] = desc

        # Chapters
        raw["chapters"] = _parse_chapters_from_player(player_data)

        # Subscribers
        raw["subscribers"] = _parse_subscriber_from_data(yt_data)

        # Channel info from player
        vd = player_data.get("videoDetails", {})
        raw["channel"] = raw.get("channel") or vd.get("author", "")
        raw["channel_url"] = raw.get("channel_url") or (
            f"https://www.youtube.com/channel/{vd.get('channelId', '')}"
            if vd.get("channelId") else ""
        )

        # Tags from player
        raw["tags"] = list(vd.get("keywords", []))

        # View count from player (more accurate than listing page)
        vc = vd.get("viewCount")
        if vc:
            try:
                raw["views"] = int(vc)
            except (ValueError, TypeError):
                pass

        # Duration from player
        ls = vd.get("lengthSeconds")
        if ls:
            try:
                raw["duration"] = int(ls)
            except (ValueError, TypeError):
                pass

        return raw

    return raw


# ─────────────────────────────────────────────────────────────────────────────
# Pre-filter helpers
# ─────────────────────────────────────────────────────────────────────────────

CANDIDATE_MULTIPLIER = 2.5


def _prefilter_candidates(entries: list[dict], target_percent: float) -> list[dict]:
    """Keep top (target_percent × CANDIDATE_MULTIPLIER)% by view count."""
    with_views = [e for e in entries if e.get("views", 0) > 0]
    without_views = [e for e in entries if e.get("views", 0) == 0]

    if len(with_views) < len(entries) * 0.5:
        logger.info("Pre-filter skipped — too few entries have view data; keeping all")
        return entries

    with_views.sort(key=lambda e: e.get("views", 0), reverse=True)
    n = max(50, min(len(entries), int(len(entries) * (target_percent / 100) * CANDIDATE_MULTIPLIER)))
    candidates = with_views[:n] + without_views
    logger.info(
        f"Pre-filter: {len(entries)} → {len(candidates)} candidates "
        f"({len(entries) - len(candidates)} low-view entries skipped)"
    )
    return candidates


# ─────────────────────────────────────────────────────────────────────────────
# Channel tab scraping
# ─────────────────────────────────────────────────────────────────────────────

def _scrape_tab(
    channel_url: str,
    tab: str,   # "videos" or "shorts"
    max_pages: int = 20,
) -> tuple[list[dict], str]:
    """
    Scrape a single channel tab, paginating via InnerTube continuations.
    Returns (list_of_raw_dicts, channel_name).
    """
    tab_url = f"{channel_url}/{tab}"
    logger.info(f"Scraping tab: {tab_url}")

    page = _fetch_page(tab_url)
    if not page:
        logger.warning(f"Could not load {tab_url}")
        return [], ""

    yt_data = get_yt_initial_data(page)
    if not yt_data:
        logger.warning(f"No ytInitialData on {tab_url}")
        return [], ""

    items, continuation, channel_name = _extract_tab_contents(yt_data, tab)
    logger.info(f"  Initial page: {len(items)} items, continuation={'yes' if continuation else 'no'}")

    page_num = 1
    while continuation and page_num < max_pages:
        page_num += 1
        logger.debug(f"  Fetching continuation page {page_num}…")
        browse_data = _innertube_browse(continuation)
        if not browse_data:
            logger.warning("InnerTube continuation returned nothing; stopping pagination")
            break
        more, continuation = _extract_continuation_items(browse_data)
        if not more:
            break
        items.extend(more)
        logger.debug(f"  Page {page_num}: +{len(more)} items (total {len(items)})")
        time.sleep(0.4)   # polite delay

    logger.info(f"Tab '{tab}': {len(items)} total items scraped")
    return items, channel_name


# ─────────────────────────────────────────────────────────────────────────────
# Main entry point
# ─────────────────────────────────────────────────────────────────────────────

def fetch_channel_videos(
    channel_input: str,
    top_percent: float = 15.0,
    enrich_pages: bool = True,
    progress_callback: Optional[Callable] = None,
    no_shorts: bool = False,
    no_videos: bool = False,
) -> tuple[list[dict], str]:
    """
    Scrape a YouTube channel and return (raw_video_list, channel_name).

    Steps:
      1. Scrape /videos and /shorts tabs (with pagination)
      2. Deduplicate by video ID
      3. Pre-filter to top candidates by view count
      4. Enrich candidates with per-video page data (exact date, likes, description…)

    Args:
        channel_input:   @handle, full URL, or UC-ID
        top_percent:     Target selection %; candidates = top (% × 2.5)
        enrich_pages:    If True, fetch each candidate's video page for full metadata
        progress_callback: fn(current, total, title) for UI progress
        no_shorts:       Skip shorts tab
        no_videos:       Skip videos tab

    Returns:
        (list_of_raw_dicts, slugified_channel_name)
    """
    channel_url = resolve_channel_url(channel_input)
    logger.info(f"Resolved URL: {channel_url}")

    all_entries: list[dict] = []
    channel_name = "unknown_channel"

    tabs_to_scrape = []
    if not no_videos:
        tabs_to_scrape.append("videos")
    if not no_shorts:
        tabs_to_scrape.append("shorts")

    for tab in tabs_to_scrape:
        entries, name = _scrape_tab(channel_url, tab)
        all_entries.extend(entries)
        if name and name != "unknown_channel":
            channel_name = name

    # Deduplicate by video ID
    seen: set[str] = set()
    unique: list[dict] = []
    for e in all_entries:
        vid = e.get("id", "")
        if vid and vid not in seen:
            seen.add(vid)
            unique.append(e)

    logger.info(f"Unique entries after dedup: {len(unique)}")

    if not unique:
        logger.warning("No videos found. Check the channel handle or try again later.")
        return [], _slugify_name(channel_name)

    # Pre-filter to top candidates
    candidates = _prefilter_candidates(unique, top_percent)

    # Per-video page enrichment
    if enrich_pages:
        total = len(candidates)
        logger.info(f"Enriching {total} candidates with per-video page data…")
        for idx, entry in enumerate(candidates, 1):
            if progress_callback:
                progress_callback(idx, total, entry.get("title", ""))
            logger.debug(f"[{idx}/{total}] Enriching: {entry.get('title', '')[:50]}")
            enrich_video_page(entry)
            time.sleep(0.25)   # polite delay between requests
    else:
        logger.info("Per-video enrichment skipped (enrich_pages=False)")

    return candidates, _slugify_name(channel_name)


def _slugify_name(name: str) -> str:
    """Lowercase, replace spaces/special chars with underscores."""
    import re
    s = name.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s-]+", "_", s)
    return s or "unknown_channel"
