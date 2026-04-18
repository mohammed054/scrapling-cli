"""
filter.py — Date-range filtering for VideoRecord lists.
"""

import logging
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)


def filter_by_date(
    items: list[dict],
    from_date: Optional[date],
    to_date: Optional[date],
) -> list[dict]:
    """
    Keep items whose upload date falls within [from_date, to_date].
    Open-ended if either bound is None.
    Items with no date are kept (we can't exclude what we don't know).
    """
    if from_date is None and to_date is None:
        return items

    kept, excluded = [], 0
    for item in items:
        d = item.get("date")
        if d is None:
            kept.append(item)
            continue
        if from_date and d < from_date:
            excluded += 1
            continue
        if to_date and d > to_date:
            excluded += 1
            continue
        kept.append(item)

    logger.info(
        f"Date filter [{from_date} → {to_date}]: {len(kept)} kept, {excluded} excluded"
    )
    return kept
