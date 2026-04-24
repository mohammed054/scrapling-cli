from __future__ import annotations

import logging
from datetime import date
from typing import Optional

from .models import ContentItem

logger = logging.getLogger(__name__)


def filter_by_date(
    items: list[ContentItem],
    from_date: Optional[date],
    to_date: Optional[date],
) -> list[ContentItem]:
    if from_date is None and to_date is None:
        return list(items)

    kept: list[ContentItem] = []
    excluded = 0
    for item in items:
        if item.date is None:
            kept.append(item)
            continue
        if from_date and item.date < from_date:
            excluded += 1
            continue
        if to_date and item.date > to_date:
            excluded += 1
            continue
        kept.append(item)

    logger.info(
        "date_filter.complete from=%s to=%s kept=%s excluded=%s",
        from_date,
        to_date,
        len(kept),
        excluded,
    )
    return kept
