from __future__ import annotations

import logging
import math
from datetime import date
from typing import Optional

from .models import ContentItem, ScoreComponents
from .utils import stable_sort

logger = logging.getLogger(__name__)

W_VIEWS = 0.50
W_LIKES = 0.20
W_COMMENTS = 0.10
W_ENGAGEMENT = 0.20


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[int(position)]
    ratio = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * ratio


def _percentile_clamp(values: list[float], percentile: float = 95) -> list[float]:
    if not values:
        return values
    cap = _percentile(values, percentile)
    return [min(value, cap) for value in values]


def _normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    low = min(values)
    high = max(values)
    span = high - low
    if span == 0:
        return [0.0 for _ in values]
    return [(value - low) / span for value in values]


def _engagement_rate(item: ContentItem) -> float:
    return (item.likes + item.comments) / item.views if item.views else 0.0


def _recency_decay(upload_date: Optional[date], reference: Optional[date] = None) -> float:
    if upload_date is None:
        return 1.0
    days_since = max(0, ((reference or date.today()) - upload_date).days)
    return math.exp(-days_since / 365)


def score_items(
    items: list[ContentItem],
    *,
    use_recency_decay: bool = False,
    clamp_outliers: bool = True,
    outlier_percentile: float = 95,
    rank_by: str = "weighted",
) -> list[ContentItem]:
    if not items:
        return []

    views_raw = [float(item.views) for item in items]
    likes_raw = [float(item.likes) for item in items]
    comments_raw = [float(item.comments) for item in items]

    if clamp_outliers and len(items) >= 5:
        views_raw = _percentile_clamp(views_raw, outlier_percentile)
        likes_raw = _percentile_clamp(likes_raw, outlier_percentile)
        comments_raw = _percentile_clamp(comments_raw, outlier_percentile)

    norm_views = _normalize(views_raw)
    norm_likes = _normalize(likes_raw)
    norm_comments = _normalize(comments_raw)
    engagement_rates = [_engagement_rate(item) for item in items]
    norm_engagement = _normalize(engagement_rates)

    for index, item in enumerate(items):
        if rank_by == "views":
            raw_score = norm_views[index]
        elif rank_by == "likes":
            raw_score = norm_likes[index]
        elif rank_by == "engagement":
            raw_score = norm_engagement[index]
        else:
            raw_score = (
                W_VIEWS * norm_views[index]
                + W_LIKES * norm_likes[index]
                + W_COMMENTS * norm_comments[index]
                + W_ENGAGEMENT * norm_engagement[index]
            )

        if use_recency_decay:
            raw_score *= _recency_decay(item.date)

        item.score = round(raw_score, 6)
        item.score_components = ScoreComponents(
            rank_by=rank_by,
            norm_views=round(norm_views[index], 4),
            norm_likes=round(norm_likes[index], 4),
            norm_comments=round(norm_comments[index], 4),
            engagement_rate=round(engagement_rates[index], 6),
            norm_engagement=round(norm_engagement[index], 4),
        )

    ranked = stable_sort(items, score_first=True)
    logger.info(
        "scoring.complete items=%s rank_by=%s top_score=%.4f bottom_score=%.4f",
        len(ranked),
        rank_by,
        ranked[0].score,
        ranked[-1].score,
    )
    return ranked


def select_top_percent(items: list[ContentItem], percent: float) -> list[ContentItem]:
    if not items:
        return []
    count = max(1, int(len(items) * percent / 100))
    selected = stable_sort(items[:count], score_first=True)
    logger.info(
        "selection.complete percent=%s selected=%s total=%s",
        percent,
        len(selected),
        len(items),
    )
    return selected
