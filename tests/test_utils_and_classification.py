from __future__ import annotations

from datetime import date

from scrapling_cli.classification import classify_all
from scrapling_cli.fetcher import (
    WATCH_PAGE_PLAIN_TIMEOUT,
    WATCH_PAGE_SKIP_STEALTH_STATUSES,
    WATCH_PAGE_STEALTH_TIMEOUT,
    _fetch_page,
    _find_json_blob,
    _renderer_to_item,
    enrich_content_item,
    fetch_channel_entries,
)
from scrapling_cli.models import ContentItem
from scrapling_cli.rendering import render_markdown
from scrapling_cli.utils import build_filename, repair_text, slugify_channel_name


def test_find_json_blob_handles_nested_braces_and_strings():
    html = """
    <script>
    var ytInitialData = {"foo":{"bar":"{baz}","items":[1,2,3]},"title":"ok"};
    var more = true;
    </script>
    """
    blob = _find_json_blob(html, "ytInitialData")
    assert blob == {"foo": {"bar": "{baz}", "items": [1, 2, 3]}, "title": "ok"}


def test_renderer_to_item_builds_short_url_from_reel_renderer():
    renderer = {
        "reelWatchEndpoint": {"videoId": "abc123"},
        "headline": {"simpleText": "Short title"},
        "thumbnail": {"thumbnails": [{"url": "thumb.jpg", "width": 100, "height": 100}]},
    }
    item = _renderer_to_item(renderer, is_short=True, source_tab="shorts")
    assert item is not None
    assert item.type == "short"
    assert item.url == "https://www.youtube.com/shorts/abc123"


def test_classify_all_splits_videos_and_shorts():
    items = [
        ContentItem(id="video1", title="Long form", url="https://youtube.com/watch?v=video1", duration=600),
        ContentItem(id="short1", title="Short", url="https://youtube.com/shorts/short1", duration=30),
    ]
    videos, shorts = classify_all(items)
    assert [item.id for item in videos] == ["video1"]
    assert [item.id for item in shorts] == ["short1"]


def test_build_filename_is_deterministic():
    item = ContentItem(
        id="vid",
        title="What Is MCP? Integrate AI Agents with Databases & APIs!",
        url="https://youtube.com/watch?v=vid",
        date=date(2025, 4, 22),
        upload_date="20250422",
    )
    assert build_filename(item) == "what-is-mcp-integrate-ai-agents-with-databases-apis-2025-04-22.md"


def test_build_filename_uses_fallback_date_when_upload_date_missing():
    item = ContentItem(
        id="vid",
        title="Fallback Date Example",
        url="https://youtube.com/watch?v=vid",
        date=date(2025, 3, 29),
        published_relative="4 weeks ago",
    )
    assert build_filename(item) == "fallback-date-example-2025-03-29.md"


def test_slugify_channel_name_is_stable():
    assert slugify_channel_name("IBM Technology") == "ibm_technology"


def test_repair_text_fixes_common_mojibake_sequences():
    repaired = repair_text(
        "Use code here " + "\u00e2\u2020\u2019" + " now " + "\u00f0\u0178\u00a4\u201d"
    )
    assert repaired == "Use code here \u2192 now \U0001F914"


def test_fetch_page_skips_stealth_fallback_for_blocked_watch_page(monkeypatch):
    import scrapling_cli.fetcher as fetcher_mod

    calls = {"plain": 0, "stealth": 0}

    class DummyPage:
        status = 429
        text = ""

    class DummyFetcher:
        @staticmethod
        def get(url, **kwargs):
            calls["plain"] += 1
            assert kwargs["timeout"] == WATCH_PAGE_PLAIN_TIMEOUT
            return DummyPage()

    class DummyStealthyFetcher:
        @staticmethod
        def fetch(url, **kwargs):
            calls["stealth"] += 1
            raise AssertionError("stealth fallback should not be used for 429 watch pages")

    monkeypatch.setattr(fetcher_mod, "Fetcher", DummyFetcher)
    monkeypatch.setattr(fetcher_mod, "StealthyFetcher", DummyStealthyFetcher)

    result = _fetch_page(
        "https://www.youtube.com/watch?v=blocked",
        retries=1,
        allow_stealth_fallback=True,
        plain_timeout=WATCH_PAGE_PLAIN_TIMEOUT,
        stealth_timeout=WATCH_PAGE_STEALTH_TIMEOUT,
        skip_stealth_on_statuses=WATCH_PAGE_SKIP_STEALTH_STATUSES,
    )
    assert result is None
    assert calls == {"plain": 1, "stealth": 0}


def test_enrich_content_item_uses_fast_watch_page_fetch(monkeypatch):
    import scrapling_cli.fetcher as fetcher_mod

    captured = {}

    def fake_fetch_page(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return None

    monkeypatch.setattr(fetcher_mod, "_fetch_page", fake_fetch_page)

    item = ContentItem(id="vid", title="Example", url="https://youtube.com/watch?v=vid")
    enrich_content_item(item)

    assert captured["url"] == "https://youtube.com/watch?v=vid"
    assert captured["retries"] == 1
    assert captured["allow_stealth_fallback"] is True
    assert captured["plain_timeout"] == WATCH_PAGE_PLAIN_TIMEOUT
    assert captured["stealth_timeout"] == WATCH_PAGE_STEALTH_TIMEOUT
    assert captured["skip_stealth_on_statuses"] == WATCH_PAGE_SKIP_STEALTH_STATUSES
    assert captured["stealth_disable_resources"] is True
    assert captured["stealth_network_idle"] is False


def test_render_markdown_marks_approximate_dates():
    item = ContentItem(
        id="vid",
        title="Approximate Date Example",
        url="https://youtube.com/watch?v=vid",
        date=date(2025, 3, 29),
        published_relative="4 weeks ago",
        channel="IBM Technology",
        channel_url="https://www.youtube.com/ibmtechnology",
    )

    markdown = render_markdown(item, include_score_details=False)

    assert "| **Date** | Approx. 2025-03-29 (4 weeks ago) |" in markdown
    assert "| **Channel** | [IBM Technology](https://www.youtube.com/ibmtechnology) |" in markdown


def test_fetch_channel_entries_sets_channel_name_from_tab_scrape(monkeypatch):
    import scrapling_cli.fetcher as fetcher_mod

    def fake_scrape_tab(channel_url, tab, *, max_pages=30):
        return (
            [
                ContentItem(
                    id="vid",
                    title="Example Video",
                    url="https://www.youtube.com/watch?v=vid",
                    published_relative="2 days ago",
                )
            ],
            "IBM Technology",
        )

    monkeypatch.setattr(fetcher_mod, "_scrape_tab", fake_scrape_tab)

    result = fetch_channel_entries(
        "https://www.youtube.com/ibmtechnology",
        enrich_pages=False,
        include_videos=True,
        include_shorts=False,
    )

    assert result.channel_name == "IBM Technology"
    assert len(result.items) == 1
    assert result.items[0].channel == "IBM Technology"
    assert result.items[0].channel_url == "https://www.youtube.com/ibmtechnology"
