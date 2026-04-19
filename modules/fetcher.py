"""
fetcher.py — YouTube channel data extraction via Scrapling.

Strategy:
  1. Fetch channel /videos and /shorts tabs using Scrapling's Fetcher
  2. Extract ytInitialData JSON from raw HTML using brace-counting
     (NOT regex termination — YouTube embeds more JS after the JSON)
  3. Paginate via YouTube's InnerTube API (POST /youtubei/v1/browse)
  4. Enrich top candidates via per-video page fetches

No yt-dlp. Pure Scrapling.
"""

import json
import logging
import re
import time
from typing import Optional, Callable

from scrapling.fetchers import Fetcher, StealthyFetcher

logger = logging.getLogger(__name__)

INNERTUBE_CONTEXT = {
    "client": {
        "clientName": "WEB",
        "clientVersion": "2.20240815.01.00",
        "hl": "en",
        "gl": "US",
    }
}
INNERTUBE_KEY = "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

CHANNEL_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

INNERTUBE_HEADERS = {
    "Content-Type": "application/json",
    "X-YouTube-Client-Name": "1",
    "X-YouTube-Client-Version": "2.20240815.01.00",
    "Origin": "https://www.youtube.com",
    "Referer": "https://www.youtube.com/",
}

CANDIDATE_MULTIPLIER = 2.5


# ─────────────────────────────────────────────────────────────────────────────
# URL resolution
# ─────────────────────────────────────────────────────────────────────────────

def resolve_channel_url(channel_input: str) -> str:
    s = channel_input.strip()
    if s.startswith("http"):
        return s.rstrip("/")
    if s.startswith("@"):
        return f"https://www.youtube.com/{s}"
    if s.startswith("UC"):
        return f"https://www.youtube.com/channel/{s}"
    return f"https://www.youtube.com/@{s}"


# ─────────────────────────────────────────────────────────────────────────────
# Robust JSON extraction from raw HTML (brace-counting)
# ─────────────────────────────────────────────────────────────────────────────

def _find_json_blob(html: str, var_name: str) -> Optional[dict]:
    """
    Locate var_name = {...} in raw HTML and extract JSON via brace-counting.
    This is robust against the regex-termination failure where YouTube places
    additional JS between the JSON blob and </script>.
    """
    needles = [
        f"var {var_name} = ",
        f'window["{var_name}"] = ',
        f"window['{var_name}'] = ",
        f"{var_name} = ",
    ]

    for needle in needles:
        idx = html.find(needle)
        if idx == -1:
            continue

        brace_start = html.find("{", idx + len(needle))
        if brace_start == -1:
            continue

        depth = 0
        i = brace_start
        in_string = False
        escape_next = False

        while i < len(html):
            ch = html[i]

            if escape_next:
                escape_next = False
                i += 1
                continue

            if ch == "\\" and in_string:
                escape_next = True
                i += 1
                continue

            if ch == '"' and not escape_next:
                in_string = not in_string
                i += 1
                continue

            if not in_string:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        json_str = html[brace_start : i + 1]
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError as e:
                            logger.debug(f"JSON decode error for '{var_name}': {e}")
                        break
            i += 1

    logger.debug(f"'{var_name}' not found in page HTML")
    return None


def _get_raw_html(page) -> str:
    """Get raw HTML string from a Scrapling response object."""
    for attr in ("html", "content", "text", "body"):
        val = getattr(page, attr, None)
        if val:
            if isinstance(val, bytes):
                return val.decode("utf-8", errors="replace")
            if isinstance(val, str) and len(val) > 100:
                return val
    return str(page)


# ─────────────────────────────────────────────────────────────────────────────
# Page fetching
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_page(url: str, retries: int = 3, use_stealth: bool = False) -> Optional[object]:
    """Fetch a URL. Falls back automatically to StealthyFetcher if plain HTTP fails."""
    for attempt in range(1, retries + 1):
        try:
            if use_stealth:
                logger.debug(f"StealthyFetcher attempt {attempt}: {url}")
                page = StealthyFetcher.fetch(
                    url, headless=True, network_idle=True,
                    extra_headers=CHANNEL_HEADERS,
                )
            else:
                logger.debug(f"Fetcher attempt {attempt}: {url}")
                page = Fetcher.get(
                    url, stealthy_headers=True,
                    extra_headers=CHANNEL_HEADERS,
                )

            if page and getattr(page, "status", 200) == 200:
                html = _get_raw_html(page)
                if "ytInitialData" in html or "ytInitialPlayerResponse" in html:
                    return page
                elif len(html) > 50_000:
                    logger.warning(
                        f"Got {len(html):,}-char page with no ytInitialData "
                        f"(bot detection page?)"
                    )
                    return page
                logger.debug(f"  Small/empty response ({len(html)} chars), retrying")
            else:
                status = getattr(page, "status", "?") if page else "None"
                logger.debug(f"  HTTP {status} on attempt {attempt}: {url}")

        except Exception as e:
            logger.debug(f"  Fetch attempt {attempt} failed: {e}")

        if attempt < retries:
            time.sleep(2 ** attempt)

    if not use_stealth:
        logger.info(f"Plain HTTP failed — falling back to StealthyFetcher: {url}")
        return _fetch_page(url, retries=2, use_stealth=True)

    logger.warning(f"All fetch attempts failed: {url}")
    return None


# ─────────────────────────────────────────────────────────────────────────────
# ytInitialData / ytInitialPlayerResponse
# ─────────────────────────────────────────────────────────────────────────────

def get_yt_initial_data(page) -> dict:
    html = _get_raw_html(page)
    data = _find_json_blob(html, "ytInitialData")
    if not data:
        logger.warning("ytInitialData not found in page HTML")
    return data or {}


def get_yt_initial_player(page) -> dict:
    html = _get_raw_html(page)
    return _find_json_blob(html, "ytInitialPlayerResponse") or {}


# ─────────────────────────────────────────────────────────────────────────────
# Parsing helpers
# ─────────────────────────────────────────────────────────────────────────────

def _safe_text(obj, *keys, default: str = "") -> str:
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


def _extract_text_runs(runs_obj) -> str:
    if not runs_obj:
        return ""
    runs = runs_obj if isinstance(runs_obj, list) else runs_obj.get("runs", [])
    return "".join(r.get("text", "") for r in runs if isinstance(r, dict))


def _parse_view_count(text: str) -> int:
    if not text:
        return 0
    s = re.sub(r"[^\d.kmb]", "", text.lower())
    try:
        if s.endswith("k"):
            return int(float(s[:-1]) * 1_000)
        if s.endswith("m"):
            return int(float(s[:-1]) * 1_000_000)
        if s.endswith("b"):
            return int(float(s[:-1]) * 1_000_000_000)
        return int(float(s)) if s else 0
    except (ValueError, TypeError):
        return 0


def _parse_duration_text(text: str) -> int:
    if not text:
        return 0
    parts = [int(p) for p in text.strip().split(":") if p.isdigit()]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0] if parts else 0


def _extract_thumbnail(renderer: dict) -> str:
    thumbs = renderer.get("thumbnail", {}).get("thumbnails") or []
    if thumbs:
        best = max(thumbs, key=lambda t: (t.get("width") or 0) * (t.get("height") or 0))
        return best.get("url", "")
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# Renderer → raw dict
# ─────────────────────────────────────────────────────────────────────────────

def _renderer_to_raw(renderer: dict, is_short: bool = False) -> Optional[dict]:
    vid_id = (
        renderer.get("videoId")
        or renderer.get("reelWatchEndpoint", {}).get("videoId")
    )
    if not vid_id:
        return None

    title = (
        _extract_text_runs(renderer.get("title"))
        or _safe_text(renderer, "headline", "simpleText")
    ).strip()
    if not title or title in ("[Deleted video]", "[Private video]"):
        return None

    # Duration — check multiple locations
    duration_text = _safe_text(renderer, "lengthText", "simpleText")
    if not duration_text:
        for overlay in renderer.get("thumbnailOverlays", []):
            tsr = overlay.get("thumbnailOverlayTimeStatusRenderer", {})
            dur = tsr.get("text", {}).get("simpleText", "")
            if dur:
                duration_text = dur
                break
    duration = _parse_duration_text(duration_text)

    view_text = (
        _safe_text(renderer, "viewCountText", "simpleText")
        or _safe_text(renderer, "shortViewCountText", "simpleText")
    )
    views = _parse_view_count(view_text)

    published_relative = (
        _safe_text(renderer, "publishedTimeText", "simpleText")
        or _safe_text(renderer, "relativePublishedTime")
    )

    url = (
        renderer.get("navigationEndpoint", {})
                .get("commandMetadata", {})
                .get("webCommandMetadata", {})
                .get("url", "")
    )
    if url and not url.startswith("http"):
        url = f"https://www.youtube.com{url}"
    if not url:
        url = (
            f"https://www.youtube.com/shorts/{vid_id}"
            if is_short else
            f"https://www.youtube.com/watch?v={vid_id}"
        )

    return {
        "id":                 vid_id,
        "title":              title,
        "views":              views,
        "likes":              0,
        "comments":           0,
        "duration":           duration,
        "url":                url,
        "thumbnail":          _extract_thumbnail(renderer),
        "published_relative": published_relative,
        "description":        "",
        "tags":               [],
        "category":           "",
        "language":           "",
        "chapters":           [],
        "top_comments":       [],
        "channel":            "",
        "channel_url":        "",
        "subscribers":        0,
        "_is_short":          is_short or (0 < duration <= 62),
        "upload_date":        None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Content walkers
# ─────────────────────────────────────────────────────────────────────────────

def _walk_contents(contents: list) -> tuple[list[dict], Optional[str]]:
    items: list[dict] = []
    continuation: Optional[str] = None

    for item in contents:
        inner = item.get("richItemRenderer", {}).get("content", item)

        vr = inner.get("videoRenderer") or inner.get("gridVideoRenderer")
        if vr:
            raw = _renderer_to_raw(vr, is_short=False)
            if raw:
                items.append(raw)
            continue

        rr = inner.get("reelItemRenderer")
        if rr:
            raw = _renderer_to_raw(rr, is_short=True)
            if raw:
                items.append(raw)
            continue

        # shortsLockupViewModel (newer Shorts layout)
        slvm = inner.get("shortsLockupViewModel")
        if slvm:
            vid_id = (
                slvm.get("onTap", {})
                    .get("innertubeCommand", {})
                    .get("reelWatchEndpoint", {})
                    .get("videoId")
            )
            headline = slvm.get("headline", {})
            title = headline.get("content", "") if isinstance(headline, dict) else ""
            if vid_id and title:
                items.append({
                    "id": vid_id, "title": title,
                    "views": 0, "likes": 0, "comments": 0, "duration": 30,
                    "url": f"https://www.youtube.com/shorts/{vid_id}",
                    "thumbnail": "", "published_relative": "",
                    "description": "", "tags": [], "category": "",
                    "language": "", "chapters": [], "top_comments": [],
                    "channel": "", "channel_url": "", "subscribers": 0,
                    "_is_short": True, "upload_date": None,
                })
            continue

        ct = item.get("continuationItemRenderer", {})
        if ct:
            token = (
                ct.get("continuationEndpoint", {})
                  .get("continuationCommand", {})
                  .get("token")
            )
            if token:
                continuation = token

    return items, continuation


def _extract_tab_contents(
    yt_data: dict, tab_name: str
) -> tuple[list[dict], Optional[str], str]:
    channel_name = ""
    items: list[dict] = []
    continuation: Optional[str] = None

    try:
        header = yt_data.get("header", {})
        c4h = header.get("c4TabbedHeaderRenderer", {})
        channel_name = (
            c4h.get("title")
            or _safe_text(yt_data, "metadata", "channelMetadataRenderer", "title")
            or ""
        )

        tabs = (
            yt_data.get("contents", {})
                   .get("twoColumnBrowseResultsRenderer", {})
                   .get("tabs", [])
        )

        for tab in tabs:
            tr = tab.get("tabRenderer", {})
            title = tr.get("title", "").lower()

            if tab_name == "videos" and title != "videos":
                continue
            if tab_name == "shorts" and title != "shorts":
                continue

            content = tr.get("content", {})

            rgr = content.get("richGridRenderer", {})
            if rgr:
                items, continuation = _walk_contents(rgr.get("contents", []))
                break

            slr = content.get("sectionListRenderer", {})
            if slr:
                for section in slr.get("contents", []):
                    isr = section.get("itemSectionRenderer", {})
                    for c in isr.get("contents", []):
                        for key in ("gridRenderer", "reelShelfRenderer"):
                            gr = c.get(key, {})
                            if gr:
                                more, tok = _walk_contents(
                                    gr.get("items", gr.get("contents", []))
                                )
                                items.extend(more)
                                if tok:
                                    continuation = tok
                break

    except Exception as e:
        logger.warning(f"Error parsing ytInitialData for tab '{tab_name}': {e}", exc_info=True)

    return items, continuation, channel_name


# ─────────────────────────────────────────────────────────────────────────────
# InnerTube pagination
# ─────────────────────────────────────────────────────────────────────────────

def _innertube_browse(token: str, retries: int = 3) -> Optional[dict]:
    url = f"https://www.youtube.com/youtubei/v1/browse?key={INNERTUBE_KEY}"
    payload = {"context": INNERTUBE_CONTEXT, "continuation": token}

    for attempt in range(1, retries + 1):
        try:
            resp = Fetcher.post(url, json=payload, extra_headers=INNERTUBE_HEADERS)
            if resp and getattr(resp, "status", 200) == 200:
                raw = _get_raw_html(resp)
                if raw:
                    return json.loads(raw)
        except Exception as e:
            logger.debug(f"InnerTube attempt {attempt}: {e}")
        if attempt < retries:
            time.sleep(2 * attempt)
    return None


def _extract_continuation_items(browse_data: dict) -> tuple[list[dict], Optional[str]]:
    items: list[dict] = []
    continuation: Optional[str] = None
    for action in browse_data.get("onResponseReceivedActions", []):
        acia = action.get("appendContinuationItemsAction", {})
        cont_items = acia.get("continuationItems", [])
        if cont_items:
            items, continuation = _walk_contents(cont_items)
            break
    return items, continuation


# ─────────────────────────────────────────────────────────────────────────────
# Per-video enrichment
# ─────────────────────────────────────────────────────────────────────────────

def _parse_upload_date(player_data: dict) -> Optional[str]:
    micro = player_data.get("microformat", {}).get("playerMicroformatRenderer", {})
    pub = micro.get("publishDate") or micro.get("uploadDate")
    return pub.replace("-", "") if pub else None


def _parse_likes(yt_data: dict) -> int:
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
            for btn in (
                pir.get("videoActions", {})
                   .get("menuRenderer", {})
                   .get("topLevelButtons", [])
            ):
                sld = (
                    btn.get("segmentedLikeDislikeButtonViewModel", {})
                       .get("likeButtonViewModel", {})
                       .get("likeButtonViewModel", {})
                       .get("toggleButtonViewModel", {})
                       .get("toggleButtonViewModel", {})
                       .get("defaultButtonViewModel", {})
                       .get("buttonViewModel", {})
                )
                label = sld.get("accessibilityText") or sld.get("title", "")
                n = _parse_view_count(label)
                if n:
                    return n
    except Exception:
        pass
    return 0


def _parse_description(yt_data: dict) -> str:
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
            if vsir:
                return _extract_text_runs(vsir.get("description", {}).get("runs", []))
    except Exception:
        pass
    return ""


def _parse_chapters(player_data: dict) -> list[dict]:
    chapters = []
    try:
        for ch in (
            player_data.get("chapters", {})
                       .get("playerOverlayChapterRenderer", {})
                       .get("chapters", [])
        ):
            cr = ch.get("chapterRenderer", {})
            chapters.append({
                "title": _extract_text_runs(cr.get("title", {}).get("runs", [])),
                "start": cr.get("timeRangeStartMillis", 0) // 1000,
                "end": 0,
            })
    except Exception:
        pass
    return chapters


def _parse_subscribers(yt_data: dict) -> int:
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
            if vsir:
                sc = vsir.get("owner", {}).get("videoOwnerRenderer", {})
                st = _safe_text(sc, "subscriberCountText", "simpleText")
                return _parse_view_count(
                    st.replace("subscribers", "").replace("subscriber", "")
                )
    except Exception:
        pass
    return 0


def enrich_video_page(raw: dict, retries: int = 2) -> dict:
    """Fetch video page for: exact date, likes, description, chapters, tags."""
    url = raw.get("url", "")
    if not url:
        return raw

    for attempt in range(1, retries + 1):
        page = _fetch_page(url)
        if not page:
            if attempt < retries:
                time.sleep(2)
            continue

        yt_data     = get_yt_initial_data(page)
        player_data = get_yt_initial_player(page)

        if not yt_data and not player_data:
            if attempt < retries:
                time.sleep(2)
            continue

        d = _parse_upload_date(player_data)
        if d:
            raw["upload_date"] = d

        raw["likes"] = _parse_likes(yt_data)

        vd = player_data.get("videoDetails", {})
        raw["description"] = vd.get("shortDescription", "") or _parse_description(yt_data)
        raw["chapters"]    = _parse_chapters(player_data)
        raw["subscribers"] = _parse_subscribers(yt_data)
        raw["channel"]     = raw.get("channel") or vd.get("author", "")
        raw["channel_url"] = raw.get("channel_url") or (
            f"https://www.youtube.com/channel/{vd.get('channelId', '')}"
            if vd.get("channelId") else ""
        )
        raw["tags"] = list(vd.get("keywords", []))

        vc = vd.get("viewCount")
        if vc:
            try:
                raw["views"] = int(vc)
            except (ValueError, TypeError):
                pass

        ls = vd.get("lengthSeconds")
        if ls:
            try:
                raw["duration"] = int(ls)
            except (ValueError, TypeError):
                pass

        return raw

    return raw


# ─────────────────────────────────────────────────────────────────────────────
# Pre-filter
# ─────────────────────────────────────────────────────────────────────────────

def _prefilter_candidates(entries: list[dict], target_percent: float) -> list[dict]:
    with_views    = [e for e in entries if e.get("views", 0) > 0]
    without_views = [e for e in entries if e.get("views", 0) == 0]

    if len(with_views) < len(entries) * 0.5:
        logger.info("Pre-filter skipped — not enough view data; keeping all")
        return entries

    with_views.sort(key=lambda e: e["views"], reverse=True)
    n = max(50, min(
        len(entries),
        int(len(entries) * (target_percent / 100) * CANDIDATE_MULTIPLIER)
    ))
    candidates = with_views[:n] + without_views
    logger.info(
        f"Pre-filter: {len(entries)} → {len(candidates)} candidates "
        f"({len(entries) - len(candidates)} low-view entries skipped)"
    )
    return candidates


# ─────────────────────────────────────────────────────────────────────────────
# Tab scraping
# ─────────────────────────────────────────────────────────────────────────────

def _scrape_tab(
    channel_url: str,
    tab: str,
    max_pages: int = 30,
) -> tuple[list[dict], str]:
    tab_url = f"{channel_url}/{tab}"
    logger.info(f"Scraping tab: {tab_url}")

    page = _fetch_page(tab_url)
    if not page:
        logger.warning(f"Could not load: {tab_url}")
        return [], ""

    yt_data = get_yt_initial_data(page)
    if not yt_data:
        logger.warning(f"No ytInitialData parsed from: {tab_url}")
        html = _get_raw_html(page)
        logger.debug(f"  HTML snippet (first 500 chars): {html[:500]}")
        return [], ""

    items, continuation, channel_name = _extract_tab_contents(yt_data, tab)
    logger.info(
        f"  Initial: {len(items)} items  "
        f"continuation={'yes' if continuation else 'no'}  "
        f"channel='{channel_name}'"
    )

    page_num = 1
    while continuation and page_num < max_pages:
        page_num += 1
        browse = _innertube_browse(continuation)
        if not browse:
            logger.warning("InnerTube returned no data; stopping pagination")
            break
        more, continuation = _extract_continuation_items(browse)
        if not more:
            break
        items.extend(more)
        logger.debug(f"  Page {page_num}: +{len(more)} items (total {len(items)})")
        time.sleep(0.5)

    logger.info(f"Tab '{tab}': {len(items)} total entries")
    return items, channel_name


# ─────────────────────────────────────────────────────────────────────────────
# Public entry point
# ─────────────────────────────────────────────────────────────────────────────

def fetch_channel_videos(
    channel_input: str,
    top_percent: float = 15.0,
    enrich_pages: bool = True,
    progress_callback: Optional[Callable] = None,
    no_shorts: bool = False,
    no_videos: bool = False,
) -> tuple[list[dict], str]:
    channel_url = resolve_channel_url(channel_input)
    logger.info(f"Resolved URL: {channel_url}")

    all_entries: list[dict] = []
    channel_name = "unknown_channel"

    tabs = []
    if not no_videos:
        tabs.append("videos")
    if not no_shorts:
        tabs.append("shorts")

    for tab in tabs:
        entries, name = _scrape_tab(channel_url, tab)
        all_entries.extend(entries)
        if name and name != "unknown_channel":
            channel_name = name

    seen: set[str] = set()
    unique: list[dict] = []
    for e in all_entries:
        vid = e.get("id", "")
        if vid and vid not in seen:
            seen.add(vid)
            unique.append(e)

    logger.info(f"Unique entries after dedup: {len(unique)}")

    if not unique:
        logger.warning("No videos found. Check the channel handle and try again.")
        return [], _slugify_name(channel_name)

    candidates = _prefilter_candidates(unique, top_percent)

    if enrich_pages:
        total = len(candidates)
        logger.info(f"Enriching {total} candidates with per-video page data…")
        for idx, entry in enumerate(candidates, 1):
            if progress_callback:
                progress_callback(idx, total, entry.get("title", ""))
            logger.debug(f"[{idx}/{total}] Enriching: {entry.get('title','')[:55]}")
            enrich_video_page(entry)
            time.sleep(0.3)
    else:
        logger.info("Per-video enrichment skipped (--no-enrich)")
        if progress_callback:
            progress_callback(len(candidates), len(candidates), "done")

    return candidates, _slugify_name(channel_name)


def _slugify_name(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s-]+", "_", s)
    return s or "unknown_channel"
