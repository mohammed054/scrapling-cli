from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console

from .app import TranscriptResolutionError, run_channel_analysis
from .cli_common import add_transcript_arguments, build_transcript_options, parse_date_arg
from .logging_utils import setup_logging
from .models import ChannelRunConfig

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scrapling-cli",
        description="Analyze a YouTube channel and export deterministic transcript-aware reports",
    )
    parser.add_argument("--channel", "-c", required=True, help="@handle, full URL, or UC channel ID")

    filtering = parser.add_argument_group("Filtering")
    filtering.add_argument("--top-percent", "-p", type=float, default=15.0, help="Top X%% to select")
    filtering.add_argument("--from-date", type=parse_date_arg, default=None, help="Include uploads on/after date")
    filtering.add_argument("--to-date", type=parse_date_arg, default=None, help="Include uploads on/before date")
    filtering.add_argument("--no-shorts", action="store_true", help="Skip Shorts entirely")
    filtering.add_argument("--no-videos", action="store_true", help="Skip long-form videos entirely")

    scoring = parser.add_argument_group("Scoring")
    scoring.add_argument(
        "--rank-by",
        choices=["weighted", "views", "engagement", "likes"],
        default="weighted",
        help="Scoring method",
    )
    scoring.add_argument("--recency-decay", action="store_true", help="Apply score decay by age")
    scoring.add_argument("--clamp-outliers", action="store_true", help="Clamp metric outliers before scoring")

    enrich = parser.add_argument_group("Enrichment")
    enrich.add_argument("--no-enrich", action="store_true", help="Skip watch-page enrichment")
    add_transcript_arguments(parser)

    export = parser.add_argument_group("Export")
    export.add_argument("--output-dir", "-o", default="output", help="Base output directory")
    export.add_argument("--export-csv", action="store_true", help="Export full scored CSVs")
    export.add_argument("--no-report", action="store_true", help="Skip channel_report.md generation")
    export.add_argument("--dry-run", action="store_true", help="Run analysis without writing files")

    misc = parser.add_argument_group("Misc")
    misc.add_argument("--log-file", default=None, help="Optional log file path")
    misc.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging(args.verbose, Path(args.log_file) if args.log_file else None)
    config = ChannelRunConfig(
        channel=args.channel,
        top_percent=args.top_percent,
        from_date=args.from_date,
        to_date=args.to_date,
        rank_by=args.rank_by,
        recency_decay=args.recency_decay,
        clamp_outliers=args.clamp_outliers,
        no_shorts=args.no_shorts,
        no_videos=args.no_videos,
        no_enrich=args.no_enrich,
        output_dir=Path(args.output_dir),
        export_csv=args.export_csv,
        no_report=args.no_report,
        dry_run=args.dry_run,
        verbose=args.verbose,
        log_file=Path(args.log_file) if args.log_file else None,
        transcript_options=build_transcript_options(args),
    )

    try:
        result = run_channel_analysis(config)
    except TranscriptResolutionError as exc:
        console.print(f"[red]Transcript resolution failed.[/red] {exc}")
        return 1
    if not result.top_videos and not result.top_shorts:
        console.print("[yellow]No items matched the current filters.[/yellow]")
        return 0
    if args.dry_run:
        console.print(
            f"[green]Dry run complete.[/green] {len(result.top_videos)} videos and {len(result.top_shorts)} shorts selected."
        )
        return 0

    console.print(
        f"[green]Done.[/green] Output root: {result.output_root} | "
        f"videos: {len(result.top_videos)} | shorts: {len(result.top_shorts)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
