from __future__ import annotations

from datetime import date

from scrapling_cli.models import ContentItem, TranscriptResult
from scrapling_cli.rendering import render_markdown
from scrapling_cli.reporting import export_csv, generate_channel_report


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


def test_generate_channel_report_includes_candidate_pool_metadata(tmp_path):
    item = ContentItem(
        id="vid",
        title="Example",
        url="https://youtube.com/watch?v=vid",
        date=date(2025, 4, 22),
        views=100,
    )
    report_path = generate_channel_report(
        channel_name="Example Channel",
        all_videos=[item],
        all_shorts=[],
        top_videos=[item],
        top_shorts=[],
        top_percent=10.0,
        rank_by="weighted",
        from_date=None,
        to_date=None,
        output_dir=tmp_path,
        scraped_item_count=120,
        candidate_item_count=40,
    )
    content = report_path.read_text(encoding="utf-8")
    assert "Unique items scraped: **120**" in content
    assert "Candidate items scored: **40**" in content
