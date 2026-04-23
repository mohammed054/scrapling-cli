from __future__ import annotations

import logging

from .models import ContentItem
from .utils import approx_date_from_relative, is_short, parse_date

logger = logging.getLogger(__name__)


def normalize_item(item: ContentItem) -> ContentItem | None:
    if not item.id or not item.title:
        logger.debug("Skipping invalid content item: id=%r title=%r", item.id, item.title)
        return None
    if item.title in {"[Deleted video]", "[Private video]"}:
        return None

    item.date = parse_date(item.upload_date) or item.date or approx_date_from_relative(item.published_relative)
    item.type = "short" if is_short(item) else "video"
    item.refresh_metrics()
    return item


def classify_all(items: list[ContentItem]) -> tuple[list[ContentItem], list[ContentItem]]:
    videos: list[ContentItem] = []
    shorts: list[ContentItem] = []
    skipped = 0

    for item in items:
        normalized = normalize_item(item)
        if normalized is None:
            skipped += 1
            continue
        if normalized.type == "short":
            shorts.append(normalized)
        else:
            videos.append(normalized)

    logger.info(
        "classification.complete videos=%s shorts=%s skipped=%s",
        len(videos),
        len(shorts),
        skipped,
    )
    return videos, shorts
