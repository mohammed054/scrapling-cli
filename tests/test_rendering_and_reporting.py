from __future__ import annotations

from datetime import date

from scrapling_cli.models import ContentItem, TranscriptResult
from scrapling_cli.rendering import render_markdown
from scrapling_cli.reporting import export_csv


def test_render_markdown_includes_transcript_metadata():
    item = ContentItem(
        id="vid",
        title="Example",
        url="https://youtube.com/watch?v=vid",
        date=date(2025, 4, 22),
        transcript=TranscriptResult.available(
            source="youtube_transcript_api",
            text="Hello world",
            language="en",
            backend_fingerprint="x",
        ),
    )
    output = render_markdown(item, include_score_details=False)
    assert "| **Status** | `available` |" in output
    assert "Hello world" in output


def test_export_csv_writes_transcript_columns(tmp_path):
    item = ContentItem(
        id="vid",
        title="Example",
        url="https://youtube.com/watch?v=vid",
        date=date(2025, 4, 22),
        transcript=TranscriptResult.unavailable(
            source="yt_dlp",
            error="no subtitles",
            language="en",
            backend_fingerprint="x",
        ),
    )
    path = export_csv([item], tmp_path / "items.csv")
    content = path.read_text(encoding="utf-8")
    assert "transcript_status" in content
    assert "no subtitles" in content
