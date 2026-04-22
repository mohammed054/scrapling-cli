from __future__ import annotations

from datetime import date

from scrapling_cli.classification import classify_all
from scrapling_cli.fetcher import _find_json_blob, _renderer_to_item
from scrapling_cli.models import ContentItem
from scrapling_cli.utils import build_filename, slugify_channel_name


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


def test_slugify_channel_name_is_stable():
    assert slugify_channel_name("IBM Technology") == "ibm_technology"
