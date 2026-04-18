"""
scorer.py — Weighted performance scoring engine.

Formula (default):
  score = 0.5 × norm_views
        + 0.2 × norm_likes
        + 0.1 × norm_comments
        + 0.2 × norm_engagement_rate

Optional modifiers:
  recency_decay  → score × exp(-days_since_upload / 365)
  clamp_outliers → values capped at 95th percentile before normalisation
"""

import math
import logging
from datetime import date
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

W_VIEWS      = 0.50
W_LIKES      = 0.20
W_COMMENTS   = 0.10
W_ENGAGEMENT = 0.20


def _percentile_clamp(values: list[float], pct: float = 95) -> list[float]:
    if not values:
        return values
    cap = float(np.percentile(values, pct))
    return [min(v, cap) for v in values]


def _normalize(values: list[float]) -> list[float]:
    lo, hi = min(values), max(values)
    span = hi - lo
    if span == 0:
        return [0.0] * len(values)
    return [(v - lo) / span for v in values]


def _engagement_rate(likes: int, comments: int, views: int) -> float:
    return (likes + comments) / views if views else 0.0


def _recency_decay(upload_date: Optional[date], ref: Optional[date] = None) -> float:
    if upload_date is None:
        return 1.0
    days = max(0, ((ref or date.today()) - upload_date).days)
    return math.exp(-days / 365)


def score_items(
    items: list[dict],
    use_recency_decay: bool = False,
    clamp_outliers: bool = True,
    outlier_percentile: float = 95,
    rank_by: str = "weighted",
) -> list[dict]:
    """
    Score and sort a list of VideoRecord dicts (descending).

    rank_by: 'weighted' | 'views' | 'likes' | 'engagement'
    """
    if not items:
        return items

    views_raw    = [float(v["views"])    for v in items]
    likes_raw    = [float(v["likes"])    for v in items]
    comments_raw = [float(v["comments"]) for v in items]

    if clamp_outliers and len(items) >= 5:
        views_raw    = _percentile_clamp(views_raw,    outlier_percentile)
        likes_raw    = _percentile_clamp(likes_raw,    outlier_percentile)
        comments_raw = _percentile_clamp(comments_raw, outlier_percentile)

    norm_views    = _normalize(views_raw)
    norm_likes    = _normalize(likes_raw)
    norm_comments = _normalize(comments_raw)
    eng_rates     = [_engagement_rate(v["likes"], v["comments"], v["views"]) for v in items]
    norm_eng      = _normalize(eng_rates)

    for i, item in enumerate(items):
        if rank_by == "views":
            raw_score = norm_views[i]
        elif rank_by == "likes":
            raw_score = norm_likes[i]
        elif rank_by == "engagement":
            raw_score = norm_eng[i]
        else:  # weighted
            raw_score = (
                W_VIEWS      * norm_views[i]
                + W_LIKES    * norm_likes[i]
                + W_COMMENTS * norm_comments[i]
                + W_ENGAGEMENT * norm_eng[i]
            )

        if use_recency_decay:
            raw_score *= _recency_decay(item.get("date"))

        item["score"] = round(raw_score, 6)
        item["_score_components"] = {
            "rank_by":        rank_by,
            "norm_views":     round(norm_views[i],    4),
            "norm_likes":     round(norm_likes[i],    4),
            "norm_comments":  round(norm_comments[i], 4),
            "engagement_rate":round(eng_rates[i],     6),
            "norm_engagement":round(norm_eng[i],      4),
        }

    items.sort(key=lambda x: x["score"], reverse=True)
    logger.info(
        f"Scored {len(items)} items [{rank_by}] — "
        f"top: {items[0]['score']:.4f} / bottom: {items[-1]['score']:.4f}"
    )
    return items


def select_top_percent(items: list[dict], percent: float) -> list[dict]:
    if not items:
        return []
    n = max(1, int(len(items) * percent / 100))
    selected = items[:n]
    logger.info(
        f"Top {percent}% → {n}/{len(items)} selected "
        f"(score {selected[-1]['score']:.4f} – {selected[0]['score']:.4f})"
    )
    return selected
