"""
scorer.py — Full performance scoring engine.

Formula:
  score = 0.5 * norm_views + 0.2 * norm_likes + 0.1 * norm_comments + 0.2 * engagement_rate

With optional:
  - Recency decay:  score *= exp(-days_since / 365)
  - Outlier clamp:  values capped at 95th percentile before normalization
"""

import math
import logging
from datetime import date
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

# Scoring weights (must sum to 1.0)
W_VIEWS = 0.5
W_LIKES = 0.2
W_COMMENTS = 0.1
W_ENGAGEMENT = 0.2


def _percentile_clamp(values: list[float], pct: float = 95) -> list[float]:
    """Clamp values at given percentile to suppress extreme outliers."""
    if not values:
        return values
    cap = float(np.percentile(values, pct))
    return [min(v, cap) for v in values]


def _normalize(values: list[float]) -> list[float]:
    """Min-max normalize a list to [0, 1]. Returns zeros if range is 0."""
    min_v = min(values)
    max_v = max(values)
    span = max_v - min_v
    if span == 0:
        return [0.0] * len(values)
    return [(v - min_v) / span for v in values]


def _engagement_rate(likes: int, comments: int, views: int) -> float:
    """Safe engagement rate: (likes + comments) / views."""
    if views == 0:
        return 0.0
    return (likes + comments) / views


def _recency_decay(upload_date: Optional[date], reference_date: Optional[date] = None) -> float:
    """Exponential recency decay: exp(-days_since / 365). Returns 1.0 if date unknown."""
    if upload_date is None:
        return 1.0
    ref = reference_date or date.today()
    days = (ref - upload_date).days
    days = max(0, days)  # guard against future dates
    return math.exp(-days / 365)


def score_items(
    items: list[dict],
    use_recency_decay: bool = False,
    clamp_outliers: bool = True,
    outlier_percentile: float = 95,
) -> list[dict]:
    """
    Compute and attach performance scores to a list of VideoRecord dicts.
    Returns the list sorted descending by score.
    """
    if not items:
        return items

    # Extract raw metrics
    views_raw = [float(v["views"]) for v in items]
    likes_raw = [float(v["likes"]) for v in items]
    comments_raw = [float(v["comments"]) for v in items]

    # Outlier clamping (95th pct)
    if clamp_outliers and len(items) >= 5:
        views_raw = _percentile_clamp(views_raw, outlier_percentile)
        likes_raw = _percentile_clamp(likes_raw, outlier_percentile)
        comments_raw = _percentile_clamp(comments_raw, outlier_percentile)

    # Normalize
    norm_views = _normalize(views_raw)
    norm_likes = _normalize(likes_raw)
    norm_comments = _normalize(comments_raw)

    # Raw engagement rates, then normalize them too
    eng_rates = [
        _engagement_rate(v["likes"], v["comments"], v["views"]) for v in items
    ]
    norm_engagement = _normalize(eng_rates)

    # Compute final scores
    for i, item in enumerate(items):
        raw_score = (
            W_VIEWS * norm_views[i]
            + W_LIKES * norm_likes[i]
            + W_COMMENTS * norm_comments[i]
            + W_ENGAGEMENT * norm_engagement[i]
        )

        if use_recency_decay:
            decay = _recency_decay(item.get("date"))
            raw_score *= decay

        item["score"] = round(raw_score, 6)
        # Also store component breakdowns for transparency
        item["_score_components"] = {
            "norm_views": round(norm_views[i], 4),
            "norm_likes": round(norm_likes[i], 4),
            "norm_comments": round(norm_comments[i], 4),
            "engagement_rate": round(eng_rates[i], 6),
            "norm_engagement": round(norm_engagement[i], 4),
        }

    # Sort descending
    items.sort(key=lambda x: x["score"], reverse=True)

    logger.info(
        f"Scored {len(items)} items. "
        f"Top score: {items[0]['score']:.4f} | "
        f"Bottom score: {items[-1]['score']:.4f}"
    )
    return items


def select_top_percent(items: list[dict], percent: float) -> list[dict]:
    """
    Select the top N% items from a pre-sorted list.
    Ensures at least 1 item is returned if the list is non-empty.
    """
    if not items:
        return []
    n = max(1, int(len(items) * (percent / 100)))
    selected = items[:n]
    logger.info(
        f"Top {percent}% → {n}/{len(items)} items selected "
        f"(score range: {selected[-1]['score']:.4f} – {selected[0]['score']:.4f})"
    )
    return selected
