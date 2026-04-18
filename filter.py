"""
filter.py — Date range filtering for video records.
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
    Keep only items whose upload date falls within [from_date, to_date].
    If either bound is None, that bound is open-ended.
    Items with no date are kept (can't exclude what we don't know).
    """
    if from_date is None and to_date is None:
        return items

    filtered = []
    excluded = 0

    for item in items:
        d = item.get("date")
        if d is None:
            # Keep date-unknown items
            filtered.append(item)
            continue

        if from_date and d < from_date:
            excluded += 1
            continue
        if to_date and d > to_date:
            excluded += 1
            continue

        filtered.append(item)

    logger.info(
        f"Date filter [{from_date} → {to_date}]: "
        f"{len(filtered)} kept, {excluded} excluded"
    )
    return filtered
