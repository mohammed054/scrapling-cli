#!/usr/bin/env python3
"""
scrapling-cli — YouTube channel performance scraper & analyzer.

Usage:
  python scrapling_cli.py --channel @erickimberling --top-percent 15 \\
      --from-date 2020-01-01 --to-date 2025-06-01 \\
      --recency-decay --clamp-outliers --transcripts --verbose
"""

import argparse
import logging
import os
import sys
from datetime import datetime, date
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    Progress,
    BarColumn,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
)
from rich.table import Table
from rich import print as rprint

# ─── local modules ────────────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))
from modules.fetcher import fetch_channel_videos, resolve_channel_url
from modules.classifier import classify_all
from modules.filter import filter_by_date
from modules.scorer import score_items, select_top_percent
from modules.transcript import enrich_with_transcripts
from modules.writer import write_all

# ─── console ──────────────────────────────────────────────────────────────────
console = Console()


# ─── logging setup ────────────────────────────────────────────────────────────
def setup_logging(verbose: bool, log_file: str = None):
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [RichHandler(console=console, show_time=True, rich_tracebacks=True)]
    if log_file:
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers,
    )


logger = logging.getLogger(__name__)


# ─── CLI argument parsing ─────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        prog="scrapling-cli",
        description="🎬 YouTube channel performance scraper — top % video extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrapling_cli.py --channel @erickimberling --top-percent 15
  python scrapling_cli.py --channel https://www.youtube.com/@erickimberling \\
      --top-percent 15 --from-date 2020-01-01 --to-date 2025-06-01 \\
      --recency-decay --clamp-outliers --transcripts --verbose
        """,
    )

    # ── Required ──
    parser.add_argument(
        "--channel", "-c",
        required=True,
        help="YouTube channel handle (@name), URL, or channel ID",
    )

    # ── Filtering ──
    parser.add_argument(
        "--top-percent", "-p",
        type=float,
        default=15.0,
        metavar="PERCENT",
        help="Top X%% to select from videos AND shorts (default: 15)",
    )
    parser.add_argument(
        "--from-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=None,
        metavar="YYYY-MM-DD",
        help="Filter: only include videos uploaded on or after this date",
    )
    parser.add_argument(
        "--to-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        default=None,
        metavar="YYYY-MM-DD",
        help="Filter: only include videos uploaded on or before this date",
    )

    # ── Scoring options ──
    parser.add_argument(
        "--recency-decay",
        action="store_true",
        default=False,
        help="Apply exponential recency decay to score (exp(-days/365))",
    )
    parser.add_argument(
        "--clamp-outliers",
        action="store_true",
        default=False,
        help="Clamp viral outliers at 95th percentile before normalization",
    )
    parser.add_argument(
        "--no-shorts",
        action="store_true",
        default=False,
        help="Skip shorts entirely",
    )
    parser.add_argument(
        "--no-videos",
        action="store_true",
        default=False,
        help="Skip long-form videos entirely",
    )

    # ── Transcript ──
    parser.add_argument(
        "--transcripts",
        action="store_true",
        default=False,
        help="Fetch transcripts for top-performing content (adds time)",
    )

    # ── Output ──
    parser.add_argument(
        "--output-dir", "-o",
        default="output",
        help="Base output directory (default: ./output)",
    )
    parser.add_argument(
        "--log-file",
        default=None,
        metavar="PATH",
        help="Optional path to write logs to a file",
    )

    # ── Misc ──
    parser.add_argument(
        "--cookies",
        default=None,
        metavar="PATH",
        help="Path to a Netscape cookies.txt file (for age-restricted content)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Enable debug-level logging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Fetch & score but do NOT write files (preview mode)",
    )

    return parser.parse_args()


# ─── progress helpers ─────────────────────────────────────────────────────────
def make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )


# ─── summary table ─────────────────────────────────────────────────────────────
def print_summary_table(label: str, items: list[dict]):
    if not items:
        console.print(f"[yellow]No {label} to display.[/yellow]")
        return

    table = Table(title=f"Top {label}", show_header=True, header_style="bold cyan")
    table.add_column("#", justify="right", style="dim")
    table.add_column("Title", max_width=50)
    table.add_column("Date", justify="center")
    table.add_column("Views", justify="right")
    table.add_column("Likes", justify="right")
    table.add_column("Score", justify="right", style="bold green")

    for i, item in enumerate(items, 1):
        d = item.get("date")
        table.add_row(
            str(i),
            item.get("title", "")[:50],
            d.strftime("%Y-%m-%d") if d else "?",
            f"{item.get('views', 0):,}",
            f"{item.get('likes', 0):,}",
            f"{item.get('score', 0):.4f}",
        )

    console.print(table)


# ─── main pipeline ─────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    setup_logging(args.verbose, args.log_file)

    console.print(Panel.fit(
        "[bold cyan]scrapling-cli[/bold cyan] 🎬  YouTube Performance Extractor\n"
        f"Channel: [yellow]{args.channel}[/yellow]  |  "
        f"Top: [green]{args.top_percent}%[/green]  |  "
        f"Dates: [blue]{args.from_date or 'any'} → {args.to_date or 'any'}[/blue]",
        border_style="cyan",
    ))

    # ── STEP 1: Fetch all channel videos ───────────────────────────────────────
    console.rule("[bold]Step 1 / 6 — Fetching channel videos[/bold]")
    raw_videos = []
    channel_name = "unknown_channel"

    with make_progress() as progress:
        fetch_task = progress.add_task("[cyan]Scanning channel…", total=None)

        def fetch_cb(current, total, title):
            progress.update(
                fetch_task,
                total=total,
                completed=current,
                description=f"[cyan]Fetching [{current}/{total}]: {title[:50]}…",
            )

        raw_videos, channel_name = fetch_channel_videos(
            args.channel,
            cookies_file=args.cookies,
            progress_callback=fetch_cb,
        )

    if not raw_videos:
        console.print("[bold red]No videos fetched. Exiting.[/bold red]")
        sys.exit(1)

    console.print(f"[green]✓[/green] Fetched {len(raw_videos)} raw entries for [bold]{channel_name}[/bold]")

    # ── STEP 2: Classify ───────────────────────────────────────────────────────
    console.rule("[bold]Step 2 / 6 — Classifying content[/bold]")
    videos, shorts = classify_all(raw_videos)
    console.print(f"[green]✓[/green] {len(videos)} long-form videos | {len(shorts)} shorts")

    if args.no_shorts:
        shorts = []
        console.print("[dim]Shorts skipped (--no-shorts)[/dim]")
    if args.no_videos:
        videos = []
        console.print("[dim]Videos skipped (--no-videos)[/dim]")

    # ── STEP 3: Date filter ────────────────────────────────────────────────────
    console.rule("[bold]Step 3 / 6 — Filtering by date range[/bold]")
    videos = filter_by_date(videos, args.from_date, args.to_date)
    shorts = filter_by_date(shorts, args.from_date, args.to_date)
    console.print(
        f"[green]✓[/green] After date filter: [bold]{len(videos)}[/bold] videos, "
        f"[bold]{len(shorts)}[/bold] shorts"
    )

    # ── STEP 4: Score & select top X% ─────────────────────────────────────────
    console.rule("[bold]Step 4 / 6 — Scoring & selecting top performers[/bold]")

    top_videos = []
    top_shorts = []

    if videos:
        scored_videos = score_items(
            videos,
            use_recency_decay=args.recency_decay,
            clamp_outliers=args.clamp_outliers,
        )
        top_videos = select_top_percent(scored_videos, args.top_percent)
        console.print(f"[green]✓[/green] Top {args.top_percent}% videos: [bold]{len(top_videos)}[/bold]")
        print_summary_table("Videos", top_videos)

    if shorts:
        scored_shorts = score_items(
            shorts,
            use_recency_decay=args.recency_decay,
            clamp_outliers=args.clamp_outliers,
        )
        top_shorts = select_top_percent(scored_shorts, args.top_percent)
        console.print(f"[green]✓[/green] Top {args.top_percent}% shorts: [bold]{len(top_shorts)}[/bold]")
        print_summary_table("Shorts", top_shorts)

    if not top_videos and not top_shorts:
        console.print("[bold red]Nothing to write after filtering. Exiting.[/bold red]")
        sys.exit(0)

    # ── STEP 5: Transcripts ────────────────────────────────────────────────────
    if args.transcripts:
        console.rule("[bold]Step 5 / 6 — Fetching transcripts[/bold]")
        all_top = top_videos + top_shorts
        total_t = len(all_top)

        with make_progress() as progress:
            t_task = progress.add_task("[magenta]Fetching transcripts…", total=total_t)

            def transcript_cb(current, total, title):
                progress.update(
                    t_task,
                    completed=current,
                    description=f"[magenta]Transcript [{current}/{total}]: {title[:50]}…",
                )

            enrich_with_transcripts(all_top, progress_callback=transcript_cb)

        console.print(f"[green]✓[/green] Transcripts processed for {total_t} items")
    else:
        console.print("[dim]Step 5 skipped — transcripts not requested (use --transcripts)[/dim]")

    # ── STEP 6: Write markdown files ──────────────────────────────────────────
    console.rule("[bold]Step 6 / 6 — Writing markdown files[/bold]")

    if args.dry_run:
        console.print("[yellow]DRY RUN — no files written.[/yellow]")
        sys.exit(0)

    base_out = os.path.join(args.output_dir, channel_name)
    videos_dir = os.path.join(base_out, "videos")
    shorts_dir = os.path.join(base_out, "shorts")

    written_total = 0

    if top_videos:
        with make_progress() as progress:
            w_task = progress.add_task("[blue]Writing video files…", total=len(top_videos))

            def write_cb_v(current, total, title):
                progress.update(w_task, completed=current,
                                description=f"[blue]Writing video [{current}/{total}]…")

            paths = write_all(top_videos, videos_dir, progress_callback=write_cb_v)
            written_total += len(paths)

    if top_shorts:
        with make_progress() as progress:
            ws_task = progress.add_task("[blue]Writing short files…", total=len(top_shorts))

            def write_cb_s(current, total, title):
                progress.update(ws_task, completed=current,
                                description=f"[blue]Writing short [{current}/{total}]…")

            paths = write_all(top_shorts, shorts_dir, progress_callback=write_cb_s)
            written_total += len(paths)

    # ── Final summary ──────────────────────────────────────────────────────────
    console.print(Panel.fit(
        f"[bold green]✅ Done![/bold green]\n\n"
        f"  Channel:   [bold]{channel_name}[/bold]\n"
        f"  Videos written:  [cyan]{len(top_videos)}[/cyan]  → {videos_dir}\n"
        f"  Shorts written:  [cyan]{len(top_shorts)}[/cyan]  → {shorts_dir}\n"
        f"  Total files:     [bold green]{written_total}[/bold green]\n"
        f"  Output root:     [yellow]{os.path.abspath(base_out)}[/yellow]",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
