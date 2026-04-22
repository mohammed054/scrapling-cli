from __future__ import annotations

from datetime import date

from scrapling_cli.models import ContentItem
from scrapling_cli.scoring import score_items, select_top_percent


def test_score_items_orders_by_score_then_date_then_title():
    items = [
        ContentItem(id="a", title="Alpha", url="https://x/a", views=100, likes=10, comments=2, date=date(2025, 1, 1)),
        ContentItem(id="b", title="Beta", url="https://x/b", views=1000, likes=30, comments=4, date=date(2025, 1, 2)),
        ContentItem(id="c", title="Gamma", url="https://x/c", views=400, likes=20, comments=8, date=date(2025, 1, 3)),
    ]
    ranked = score_items(items, rank_by="weighted", clamp_outliers=False)
    assert [item.id for item in ranked] == ["b", "c", "a"]
    assert ranked[0].score_components.rank_by == "weighted"


def test_select_top_percent_keeps_at_least_one():
    items = [
        ContentItem(id="a", title="Alpha", url="https://x/a", score=0.9),
        ContentItem(id="b", title="Beta", url="https://x/b", score=0.1),
    ]
    selected = select_top_percent(items, 1)
    assert len(selected) == 1
    assert selected[0].id == "a"
