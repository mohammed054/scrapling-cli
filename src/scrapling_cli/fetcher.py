from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Callable, Optional

try:
    from scrapling.fetchers import Fetcher, StealthyFetcher
except ImportError:  # pragma: no cover - runtime dependency guard
    Fetcher = None
    StealthyFetcher = None

from .models import ContentItem
from .utils import parse_date, repair_text, slugify_channel_name

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
CANDIDATE_MULTIPLIER = 2.5

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


class FetcherError(RuntimeError):
    """Raised when channel pages cannot be fetched after retries."""


@dataclass(slots=True)
class ChannelFetchResult:
    items: list[ContentItem]
    channel_name: str
    channel_slug: str
    scraped_item_count: int
    candidate_item_count: int


def resolve_channel_url(channel_input: str) -> str:
    channel = channel_input.strip()
    if channel.startswith("http"):
        return channel.rstrip("/")
    if channel.startswith("@"):
        return f"https://www.youtube.com/{channel}"
    if channel.startswith("UC"):
        return f"https://www.youtube.com/channel/{channel}"
    return f"https://www.youtube.com/@{channel}"


def _get_raw_html(page: object) -> str:
    for attr in ("html", "content", "text", "body"):
        value = getattr(page, attr, None)
        if not value:
            continue
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        if isinstance(value, str) and len(value) > 100:
            return value
    return str(page)


def _find_json_blob(html: str, variable_name: str) -> Optional[dict]:
    needles = [
        f"var {variable_name} = ",
        f'window["{variable_name}"] = ',
        f"window['{variable_name}'] = ",
        f"{variable_name} = ",
    ]
    for needle in needles:
        start = html.find(needle)
        if start == -1:
            continue
        brace_start = html.find("{", start + len(needle))
        if brace_start == -1:
            continue
        depth = 0
        index = brace_start
        in_string = False
        escape_next = False
        while index < len(html):
            char = html[index]
            if escape_next:
                escape_next = False
                index += 1
                continue
            if char == "\\" and in_string:
                escape_next = True
                index += 1
                continue
            if char == '"':
                in_string = not in_string
                index += 1
                continue
            if not in_string:
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(html[brace_start : index + 1])
                        except json.JSONDecodeError as exc:
                            logger.debug("fetcher.json_decode_error variable=%s error=%s", variable_name, exc)
                        break
            index += 1
    return None


def get_yt_initial_data(page: object) -> dict:
    return _find_json_blob(_get_raw_html(page), "ytInitialData") or {}


def get_yt_initial_player(page: object) -> dict:
    return _find_json_blob(_get_raw_html(page), "ytInitialPlayerResponse") or {}


def _fetch_page(url: str, *, retries: int = 3, use_stealth: bool = False) -> object | None:
    if Fetcher is None or StealthyFetcher is None:
        raise FetcherError("scrapling is not installed")
    for attempt in range(1, retries + 1):
        try:
            if use_stealth:
                page = StealthyFetcher.fetch(
                    url,
                    headless=True,
                    network_idle=True,
                    extra_headers=CHANNEL_HEADERS,
                )
            else:
                page = Fetcher.get(url, stealthy_headers=True, extra_headers=CHANNEL_HEADERS)

            if page and getattr(page, "status", 200) == 200:
                html = _get_raw_html(page)
                if "ytInitialData" in html or "ytInitialPlayerResponse" in html or len(html) > 50_000:
                    return page
                logger.debug("fetcher.small_response url=%s size=%s", url, len(html))
            else:
                logger.debug("fetcher.http_error url=%s status=%s", url, getattr(page, "status", "?"))
        except Exception as exc:  # noqa: BLE001
            logger.debug("fetcher.request_error url=%s attempt=%s error=%s", url, attempt, exc)
        if attempt < retries:
            time.sleep(2**attempt)
    if not use_stealth:
        logger.info("fetcher.retry_with_stealth url=%s", url)
        return _fetch_page(url, retries=2, use_stealth=True)
    return None


def _safe_text(obj: object, *keys: object, default: str = "") -> str:
    current = obj
    for key in keys:
        if current is None:
            return default
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and isinstance(key, int):
            current = current[key] if key < len(current) else None
        else:
            return default
    return repair_text(str(current).strip()) if current is not None else default


def _extract_text_runs(runs_obj: object) -> str:
    if not runs_obj:
        return ""
    runs = runs_obj if isinstance(runs_obj, list) else runs_obj.get("runs", [])
    return repair_text("".join(run.get("text", "") for run in runs if isinstance(run, dict)))


def _parse_view_count(text: str) -> int:
    if not text:
        return 0
    cleaned = re.sub(r"[^\d.kmb]", "", text.lower())
    try:
        if cleaned.endswith("k"):
            return int(float(cleaned[:-1]) * 1_000)
        if cleaned.endswith("m"):
            return int(float(cleaned[:-1]) * 1_000_000)
        if cleaned.endswith("b"):
            return int(float(cleaned[:-1]) * 1_000_000_000)
        return int(float(cleaned)) if cleaned else 0
    except (TypeError, ValueError):
        return 0


def _parse_duration_text(text: str) -> int:
    if not text:
        return 0
    parts = [int(part) for part in text.strip().split(":") if part.isdigit()]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0] if parts else 0


def _extract_thumbnail(renderer: dict) -> str:
    thumbnails = renderer.get("thumbnail", {}).get("thumbnails") or []
    if not thumbnails:
        return ""
    best = max(thumbnails, key=lambda thumb: (thumb.get("width") or 0) * (thumb.get("height") or 0))
    return best.get("url", "")


def _renderer_to_item(renderer: dict, *, is_short: bool, source_tab: str) -> ContentItem | None:
    video_id = renderer.get("videoId") or renderer.get("reelWatchEndpoint", {}).get("videoId")
    if not video_id:
        return None
    title = (_extract_text_runs(renderer.get("title")) or _safe_text(renderer, "headline", "simpleText")).strip()
    if not title or title in {"[Deleted video]", "[Private video]"}:
        return None

    duration_text = _safe_text(renderer, "lengthText", "simpleText")
    if not duration_text:
        for overlay in renderer.get("thumbnailOverlays", []):
            status = overlay.get("thumbnailOverlayTimeStatusRenderer", {})
            candidate = status.get("text", {}).get("simpleText", "")
            if candidate:
                duration_text = candidate
                break
    duration = _parse_duration_text(duration_text)
    view_text = _safe_text(renderer, "viewCountText", "simpleText") or _safe_text(
        renderer,
        "shortViewCountText",
        "simpleText",
    )
    published_relative = _safe_text(renderer, "publishedTimeText", "simpleText") or _safe_text(
        renderer,
        "relativePublishedTime",
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
        url = f"https://www.youtube.com/shorts/{video_id}" if is_short else f"https://www.youtube.com/watch?v={video_id}"

    return ContentItem(
        id=video_id,
        title=title,
        url=url,
        type="short" if is_short else "video",
        views=_parse_view_count(view_text),
        duration=duration,
        thumbnail=_extract_thumbnail(renderer),
        published_relative=published_relative,
        source_tab=source_tab,
    )


def _walk_contents(contents: list, *, source_tab: str) -> tuple[list[ContentItem], Optional[str]]:
    items: list[ContentItem] = []
    continuation: Optional[str] = None

    for entry in contents:
        inner = entry.get("richItemRenderer", {}).get("content", entry)
        video_renderer = inner.get("videoRenderer") or inner.get("gridVideoRenderer")
        if video_renderer:
            item = _renderer_to_item(video_renderer, is_short=False, source_tab=source_tab)
            if item:
                items.append(item)
            continue
        reel_renderer = inner.get("reelItemRenderer")
        if reel_renderer:
            item = _renderer_to_item(reel_renderer, is_short=True, source_tab=source_tab)
            if item:
                items.append(item)
            continue
        shorts_lockup = inner.get("shortsLockupViewModel")
        if shorts_lockup:
            video_id = (
                shorts_lockup.get("onTap", {})
                .get("innertubeCommand", {})
                .get("reelWatchEndpoint", {})
                .get("videoId")
            )
            headline = shorts_lockup.get("headline", {})
            title = repair_text(headline.get("content", "")) if isinstance(headline, dict) else ""
            if video_id and title:
                items.append(
                    ContentItem(
                        id=video_id,
                        title=title,
                        url=f"https://www.youtube.com/shorts/{video_id}",
                        type="short",
                        duration=30,
                        source_tab="shorts",
                    )
                )
            continue
        continuation_renderer = entry.get("continuationItemRenderer", {})
        if continuation_renderer:
            continuation = (
                continuation_renderer.get("continuationEndpoint", {})
                .get("continuationCommand", {})
                .get("token")
            )
    return items, continuation


def _extract_tab_contents(yt_data: dict, tab_name: str) -> tuple[list[ContentItem], Optional[str], str]:
    channel_name = repair_text(
        yt_data.get("header", {}).get("c4TabbedHeaderRenderer", {}).get("title")
        or _safe_text(yt_data, "metadata", "channelMetadataRenderer", "title")
        or ""
    )
    tabs = yt_data.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])
    for tab in tabs:
        renderer = tab.get("tabRenderer", {})
        if renderer.get("title", "").lower() != tab_name:
            continue
        content = renderer.get("content", {})
        rich_grid = content.get("richGridRenderer", {})
        if rich_grid:
            items, continuation = _walk_contents(rich_grid.get("contents", []), source_tab=tab_name)
            return items, continuation, channel_name
        section_list = content.get("sectionListRenderer", {})
        if section_list:
            items: list[ContentItem] = []
            continuation: Optional[str] = None
            for section in section_list.get("contents", []):
                item_section = section.get("itemSectionRenderer", {})
                for content_item in item_section.get("contents", []):
                    for key in ("gridRenderer", "reelShelfRenderer"):
                        renderer_block = content_item.get(key, {})
                        if renderer_block:
                            more, token = _walk_contents(
                                renderer_block.get("items", renderer_block.get("contents", [])),
                                source_tab=tab_name,
                            )
                            items.extend(more)
                            if token:
                                continuation = token
            return items, continuation, channel_name
    return [], None, channel_name


def _innertube_browse(token: str, *, retries: int = 3) -> dict | None:
    if Fetcher is None:
        raise FetcherError("scrapling is not installed")
    url = f"https://www.youtube.com/youtubei/v1/browse?key={INNERTUBE_KEY}"
    payload = {"context": INNERTUBE_CONTEXT, "continuation": token}
    for attempt in range(1, retries + 1):
        try:
            response = Fetcher.post(url, json=payload, extra_headers=INNERTUBE_HEADERS)
            if response and getattr(response, "status", 200) == 200:
                raw = _get_raw_html(response)
                if raw:
                    return json.loads(raw)
        except Exception as exc:  # noqa: BLE001
            logger.debug("fetcher.innertube_error attempt=%s error=%s", attempt, exc)
        if attempt < retries:
            time.sleep(2 * attempt)
    return None


def _extract_continuation_items(browse_data: dict, *, source_tab: str) -> tuple[list[ContentItem], Optional[str]]:
    for action in browse_data.get("onResponseReceivedActions", []):
        continuation_items = action.get("appendContinuationItemsAction", {}).get("continuationItems", [])
        if continuation_items:
            return _walk_contents(continuation_items, source_tab=source_tab)
    return [], None


def _parse_upload_date(player_data: dict) -> Optional[str]:
    micro = player_data.get("microformat", {}).get("playerMicroformatRenderer", {})
    published = micro.get("publishDate") or micro.get("uploadDate")
    return published.replace("-", "") if published else None


def _parse_likes(yt_data: dict) -> int:
    try:
        contents = (
            yt_data.get("contents", {})
            .get("twoColumnWatchNextResults", {})
            .get("results", {})
            .get("results", {})
            .get("contents", [])
        )
        for content in contents:
            primary = content.get("videoPrimaryInfoRenderer", {})
            if not primary:
                continue
            buttons = primary.get("videoActions", {}).get("menuRenderer", {}).get("topLevelButtons", [])
            for button in buttons:
                model = (
                    button.get("segmentedLikeDislikeButtonViewModel", {})
                    .get("likeButtonViewModel", {})
                    .get("likeButtonViewModel", {})
                    .get("toggleButtonViewModel", {})
                    .get("toggleButtonViewModel", {})
                    .get("defaultButtonViewModel", {})
                    .get("buttonViewModel", {})
                )
                label = repair_text(model.get("accessibilityText") or model.get("title", ""))
                count = _parse_view_count(label)
                if count:
                    return count
    except Exception as exc:  # noqa: BLE001
        logger.debug("fetcher.parse_likes_error error=%s", exc)
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
        for content in contents:
            secondary = content.get("videoSecondaryInfoRenderer", {})
            if secondary:
                return repair_text(_extract_text_runs(secondary.get("description", {}).get("runs", [])))
    except Exception as exc:  # noqa: BLE001
        logger.debug("fetcher.parse_description_error error=%s", exc)
    return ""


def _parse_chapters(player_data: dict) -> list[dict]:
    chapters: list[dict] = []
    try:
        chapter_blocks = (
            player_data.get("chapters", {})
            .get("playerOverlayChapterRenderer", {})
            .get("chapters", [])
        )
        for block in chapter_blocks:
            renderer = block.get("chapterRenderer", {})
            chapters.append(
                {
                    "title": repair_text(_extract_text_runs(renderer.get("title", {}).get("runs", []))),
                    "start": renderer.get("timeRangeStartMillis", 0) // 1000,
                    "end": 0,
                }
            )
    except Exception as exc:  # noqa: BLE001
        logger.debug("fetcher.parse_chapters_error error=%s", exc)
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
        for content in contents:
            secondary = content.get("videoSecondaryInfoRenderer", {})
            if not secondary:
                continue
            owner = secondary.get("owner", {}).get("videoOwnerRenderer", {})
            text = _safe_text(owner, "subscriberCountText", "simpleText")
            return _parse_view_count(text.replace("subscribers", "").replace("subscriber", ""))
    except Exception as exc:  # noqa: BLE001
        logger.debug("fetcher.parse_subscribers_error error=%s", exc)
    return 0


def enrich_content_item(item: ContentItem, *, retries: int = 2) -> ContentItem:
    if not item.url:
        return item
    for attempt in range(1, retries + 1):
        page = _fetch_page(item.url)
        if not page:
            if attempt < retries:
                time.sleep(2)
            continue
        yt_data = get_yt_initial_data(page)
        player_data = get_yt_initial_player(page)
        if not yt_data and not player_data:
            if attempt < retries:
                time.sleep(2)
            continue

        item.upload_date = _parse_upload_date(player_data) or item.upload_date
        item.date = parse_date(item.upload_date) or item.date
        item.likes = _parse_likes(yt_data)
        video_details = player_data.get("videoDetails", {})
        item.description = repair_text(video_details.get("shortDescription", "") or _parse_description(yt_data))
        item.chapters = _parse_chapters(player_data)
        item.subscribers = _parse_subscribers(yt_data)
        item.channel = repair_text(item.channel or video_details.get("author", ""))
        if not item.channel_url and video_details.get("channelId"):
            item.channel_url = f"https://www.youtube.com/channel/{video_details['channelId']}"
        item.tags = [repair_text(tag) for tag in video_details.get("keywords", [])]
        if video_details.get("viewCount"):
            try:
                item.views = int(video_details["viewCount"])
            except (TypeError, ValueError):
                pass
        if video_details.get("lengthSeconds"):
            try:
                item.duration = int(video_details["lengthSeconds"])
            except (TypeError, ValueError):
                pass
        item.refresh_metrics()
        return item
    return item


def _prefilter_candidates(entries: list[ContentItem], target_percent: float) -> list[ContentItem]:
    with_views = [entry for entry in entries if entry.views > 0]
    without_views = [entry for entry in entries if entry.views <= 0]
    if len(with_views) < len(entries) * 0.5:
        logger.info("fetcher.prefilter_skipped reason=insufficient_view_data total=%s", len(entries))
        return entries
    ranked = sorted(with_views, key=lambda entry: (-entry.views, entry.title.lower(), entry.id))
    target_selection = max(1, int(len(entries) * (target_percent / 100)))
    candidate_count = max(50, int(target_selection * CANDIDATE_MULTIPLIER))
    candidate_count = min(len(entries), min(175, candidate_count))
    zero_view_bonus = min(len(without_views), max(5, candidate_count // 10))
    view_ranked_count = max(0, candidate_count - zero_view_bonus)
    zero_view_ranked = sorted(without_views, key=lambda entry: (entry.title.lower(), entry.id))
    candidates = ranked[:view_ranked_count] + zero_view_ranked[:zero_view_bonus]
    logger.info("fetcher.prefilter total=%s candidates=%s", len(entries), len(candidates))
    return candidates


def _scrape_tab(channel_url: str, tab: str, *, max_pages: int = 30) -> tuple[list[ContentItem], str]:
    tab_url = f"{channel_url}/{tab}"
    page = _fetch_page(tab_url)
    if not page:
        raise FetcherError(f"could not load {tab_url}")

    yt_data = get_yt_initial_data(page)
    if not yt_data:
        raise FetcherError(f"ytInitialData not parsed from {tab_url}")

    items, continuation, channel_name = _extract_tab_contents(yt_data, tab)
    page_number = 1
    while continuation and page_number < max_pages:
        page_number += 1
        browse_data = _innertube_browse(continuation)
        if not browse_data:
            break
        more, continuation = _extract_continuation_items(browse_data, source_tab=tab)
        if not more:
            break
        items.extend(more)
        time.sleep(0.5)

    logger.info("fetcher.scrape_tab tab=%s items=%s channel=%s", tab, len(items), channel_name or "unknown")
    return items, channel_name


def fetch_channel_entries(
    channel_input: str,
    *,
    candidate_percent: float | None = None,
    enrich_pages: bool = True,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
    include_videos: bool = True,
    include_shorts: bool = True,
) -> ChannelFetchResult:
    channel_url = resolve_channel_url(channel_input)
    tabs = []
    if include_videos:
        tabs.append("videos")
    if include_shorts:
        tabs.append("shorts")
    if not tabs:
        raise FetcherError("at least one of videos or shorts must be enabled")

    all_items: list[ContentItem] = []
    channel_name = "unknown_channel"
    for tab in tabs:
        items, scraped_name = _scrape_tab(channel_url, tab)
        for item in items:
            item.channel_url = channel_url
        all_items.extend(items)
        if scraped_name and scraped_name != "unknown_channel":
            channel_name = scraped_name

    unique: list[ContentItem] = []
    seen_ids: set[str] = set()
    for item in all_items:
        if item.id and item.id not in seen_ids:
            seen_ids.add(item.id)
            unique.append(item)

    if not unique:
        raise FetcherError(f"no content found for {channel_input}")

    candidates = _prefilter_candidates(unique, candidate_percent) if candidate_percent else unique
    if enrich_pages:
        for index, item in enumerate(candidates, 1):
            if progress_callback:
                progress_callback(index, len(candidates), item.title)
            enrich_content_item(item)
            time.sleep(0.3)

    final_name = channel_name or channel_input
    return ChannelFetchResult(
        items=candidates,
        channel_name=final_name,
        channel_slug=slugify_channel_name(final_name),
        scraped_item_count=len(unique),
        candidate_item_count=len(candidates),
    )
