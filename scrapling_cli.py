#!/usr/bin/env python3
"""
scrapling-cli — YouTube channel performance scraper & analyzer.
Production-ready. Full-featured. No shortcuts.
"""

import argparse
import logging
import os
import sys
from datetime import datetime, date
from pathlib import Path

import pyfiglet
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    Progress, BarColumn, SpinnerColumn,
    TextColumn, TimeElapsedColumn, MofNCompleteColumn,
)
from rich.table import Table
from rich import box

sys.path.insert(0, str(Path(__file__).parent))
from modules.fetcher import fetch_channel_videos
from modules.classifier import classify_all
from modules.filter import filter_by_date
from modules.scorer import score_items, select_top_percent
from modules.transcript import enrich_with_transcripts
from modules.writer import write_all
from modules.reporter import generate_channel_report, export_csv

console = Console()


# ── ASCII BANNER ──────────────────────────────────────────────────────────────
def print_banner():
    try:
        ascii_art = pyfiglet.figlet_format("SCRAPLING", font="ansi_shadow")
        lines = ascii_art.strip().split("\n")
        colors = ["bright_cyan", "cyan", "bright_blue", "blue", "bright_cyan", "cyan", "bright_blue"]
        for i, line in enumerate(lines):
            console.print(f"[{colors[i % len(colors)]}]{line}[/]")
        sub = pyfiglet.figlet_format("CLI", font="ansi_shadow")
        for line in sub.strip().split("\n"):
            console.print(f"[dim cyan]{line}[/]")
    except Exception:
        console.print("[bold bright_cyan]═══  SCRAPLING CLI  ═══[/bold bright_cyan]")

    console.print()
    console.print(Panel(
        "[bold white]YouTube Channel Performance Extractor[/bold white]\n"
        "[dim]Top-% scoring · Transcripts · Comments · Tags · Chapters · CSV export[/dim]",
        border_style="bright_cyan",
        padding=(0, 4),
    ))
    console.print()


# ── LOGGING ───────────────────────────────────────────────────────────────────
def setup_logging(verbose: bool, log_file: str = None):
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [RichHandler(console=console, show_time=True, rich_tracebacks=True)]
    if log_file:
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(level=level, format="%(message)s", datefmt="[%X]", handlers=handlers)


logger = logging.getLogger(__name__)


# ── ARG PARSING ───────────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        prog="scrapling-cli",
        description="YouTube channel top-performer extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick run - top 15 percent
  python scrapling_cli.py --channel "@erickimberling" --top-percent 15

  # Full feature run - everything enabled
  python scrapling_cli.py --channel "@erickimberling" --top-percent 15 ^
      --from-date 2020-01-01 --to-date 2025-06-01 ^
      --rank-by weighted --recency-decay --clamp-outliers ^
      --transcripts --fetch-comments 10 --export-csv --verbose
        """,
    )

    req = parser.add_argument_group("Required")
    req.add_argument("--channel", "-c", required=True,
                     help="Channel handle (@name), full URL, or channel ID")

    flt = parser.add_argument_group("Filtering")
    flt.add_argument("--top-percent", "-p", type=float, default=15.0, metavar="PERCENT",
                     help="Top X%% selected from videos AND shorts separately (default: 15)")
    flt.add_argument("--from-date",
                     type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
                     default=None, metavar="YYYY-MM-DD",
                     help="Only include videos uploaded on or after this date")
    flt.add_argument("--to-date",
                     type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
                     default=None, metavar="YYYY-MM-DD",
                     help="Only include videos uploaded on or before this date")
    flt.add_argument("--no-shorts", action="store_true", default=False,
                     help="Skip Shorts entirely")
    flt.add_argument("--no-videos", action="store_true", default=False,
                     help="Skip long-form videos entirely")

    sc = parser.add_argument_group("Scoring")
    sc.add_argument("--rank-by", choices=["weighted", "views", "engagement", "likes"],
                    default="weighted",
                    help="Scoring method: weighted|views|engagement|likes (default: weighted)")
    sc.add_argument("--recency-decay", action="store_true", default=False,
                    help="Apply exp(-days/365) recency decay to scores")
    sc.add_argument("--clamp-outliers", action="store_true", default=False,
                    help="Clamp viral outliers at 95th percentile before normalization")

    en = parser.add_argument_group("Enrichment")
    en.add_argument("--transcripts", action="store_true", default=False,
                    help="Fetch transcripts for each top video")
    en.add_argument("--fetch-comments", type=int, default=0, metavar="N",
                    help="Fetch top N comments per video (0=disabled, recommended: 10-20)")

    ex = parser.add_argument_group("Export")
    ex.add_argument("--output-dir", "-o", default="output",
                    help="Base output directory (default: ./output)")
    ex.add_argument("--export-csv", action="store_true", default=False,
                    help="Export full scored dataset as CSV files")
    ex.add_argument("--no-report", action="store_true", default=False,
                    help="Skip generating channel_report.md")

    ms = parser.add_argument_group("Misc")
    ms.add_argument("--cookies", default=None, metavar="PATH",
                    help="Netscape cookies.txt for age-restricted content")
    ms.add_argument("--log-file", default=None, metavar="PATH",
                    help="Write full logs to file")
    ms.add_argument("--verbose", "-v", action="store_true", default=False,
                    help="Debug-level logging")
    ms.add_argument("--dry-run", action="store_true", default=False,
                    help="Score & preview without writing files")

    return parser.parse_args()


# ── PROGRESS ──────────────────────────────────────────────────────────────────
def make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=35),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )


# ── HELPERS ───────────────────────────────────────────────────────────────────
def _dur(seconds) -> str:
    try:
        s = int(seconds)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"
    except Exception:
        return "?"


def step_header(n: int, total: int, label: str):
    console.print()
    console.rule(f"[bold bright_cyan]  Step {n}/{total} — {label}  [/]")
    console.print()


def print_summary_table(label: str, items: list[dict]):
    if not items:
        console.print(f"[yellow]No {label} to display.[/yellow]")
        return

    table = Table(
        title=f"🏆 Top {label}",
        show_header=True,
        header_style="bold bright_cyan",
        box=box.ROUNDED,
        border_style="cyan",
        row_styles=["", "dim"],
    )
    table.add_column("#", justify="right", style="bold yellow", width=4)
    table.add_column("Title", max_width=45)
    table.add_column("Date", justify="center", style="dim", width=12)
    table.add_column("Views", justify="right", style="bright_white", width=12)
    table.add_column("Likes", justify="right", style="green", width=9)
    table.add_column("Comments", justify="right", style="blue", width=10)
    table.add_column("Dur", justify="center", style="dim", width=8)
    table.add_column("Score", justify="right", style="bold bright_green", width=10)

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, item in enumerate(items, 1):
        d = item.get("date")
        table.add_row(
            medals.get(i, str(i)),
            item.get("title", "")[:45],
            d.strftime("%Y-%m-%d") if d else "?",
            f"{item.get('views', 0):,}",
            f"{item.get('likes', 0):,}",
            f"{item.get('comments', 0):,}",
            _dur(item.get("duration", 0)),
            f"{item.get('score', 0):.4f}",
        )

    console.print(table)
    console.print()


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    print_banner()
    setup_logging(args.verbose, args.log_file)

    TOTAL_STEPS = 7

    console.print(Panel(
        "\n".join([
            f"  [bright_cyan]Channel[/]         {args.channel}",
            f"  [bright_cyan]Top percent[/]     [bold green]{args.top_percent}%[/]",
            f"  [bright_cyan]Rank by[/]         [bold]{args.rank_by}[/]",
            f"  [bright_cyan]Date range[/]      {args.from_date or 'any'} → {args.to_date or 'any'}",
            f"  [bright_cyan]Recency decay[/]   {'[green]✅ on[/]' if args.recency_decay else '[dim]off[/]'}",
            f"  [bright_cyan]Clamp outliers[/]  {'[green]✅ on[/]' if args.clamp_outliers else '[dim]off[/]'}",
            f"  [bright_cyan]Transcripts[/]     {'[green]✅ on[/]' if args.transcripts else '[dim]off[/]'}",
            f"  [bright_cyan]Comments[/]        {'[green]✅ top ' + str(args.fetch_comments) + '[/]' if args.fetch_comments else '[dim]off[/]'}",
            f"  [bright_cyan]Export CSV[/]      {'[green]✅ on[/]' if args.export_csv else '[dim]off[/]'}",
            f"  [bright_cyan]Output dir[/]      {args.output_dir}",
        ]),
        title="[bold]⚙  Run Configuration[/bold]",
        border_style="bright_cyan",
        padding=(1, 2),
    ))

    # ── 1. Fetch ──────────────────────────────────────────────────────────────
    step_header(1, TOTAL_STEPS, "Fetching channel data (two-phase fast scan)")
    raw_videos, channel_name = [], "unknown_channel"

    with make_progress() as progress:
        task = progress.add_task("[cyan]Scanning…", total=None)
        def fetch_cb(current, total, title):
            progress.update(task, total=total, completed=current,
                            description=f"[cyan]Full fetch [{current}/{total}]: {title[:40]}…")
        raw_videos, channel_name = fetch_channel_videos(
            args.channel,
            top_percent=args.top_percent,
            cookies_file=args.cookies,
            fetch_comments=args.fetch_comments,
            progress_callback=fetch_cb,
        )

    if not raw_videos:
        console.print("[bold red]✗ No videos fetched. Check channel handle. Exiting.[/bold red]")
        sys.exit(1)

    console.print(f"[green]✓[/green] Fetched [bold]{len(raw_videos)}[/bold] entries "
                  f"for [bold bright_cyan]{channel_name}[/bold bright_cyan]")

    # ── 2. Classify ───────────────────────────────────────────────────────────
    step_header(2, TOTAL_STEPS, "Classifying: Videos vs Shorts")
    videos, shorts = classify_all(raw_videos)
    console.print(f"[green]✓[/green] [bold]{len(videos)}[/bold] long-form videos  "
                  f"| [bold]{len(shorts)}[/bold] shorts")

    if args.no_shorts:
        shorts = []
        console.print("[dim]  Shorts skipped (--no-shorts)[/dim]")
    if args.no_videos:
        videos = []
        console.print("[dim]  Videos skipped (--no-videos)[/dim]")

    # ── 3. Date filter ────────────────────────────────────────────────────────
    step_header(3, TOTAL_STEPS, "Applying date filter")
    videos = filter_by_date(videos, args.from_date, args.to_date)
    shorts = filter_by_date(shorts, args.from_date, args.to_date)
    console.print(f"[green]✓[/green] After filter: [bold]{len(videos)}[/bold] videos, "
                  f"[bold]{len(shorts)}[/bold] shorts")

    # ── 4. Score & select ─────────────────────────────────────────────────────
    step_header(4, TOTAL_STEPS, f"Scoring [{args.rank_by}] & selecting top {args.top_percent}%")
    top_videos, top_shorts = [], []

    if videos:
        scored = score_items(videos, use_recency_decay=args.recency_decay,
                             clamp_outliers=args.clamp_outliers, rank_by=args.rank_by)
        top_videos = select_top_percent(scored, args.top_percent)
        console.print(f"[green]✓[/green] Top {args.top_percent}% videos → [bold]{len(top_videos)}[/bold]")
        print_summary_table("Videos", top_videos[:20])

    if shorts:
        scored_s = score_items(shorts, use_recency_decay=args.recency_decay,
                               clamp_outliers=args.clamp_outliers, rank_by=args.rank_by)
        top_shorts = select_top_percent(scored_s, args.top_percent)
        console.print(f"[green]✓[/green] Top {args.top_percent}% shorts → [bold]{len(top_shorts)}[/bold]")
        print_summary_table("Shorts", top_shorts[:20])

    if not top_videos and not top_shorts:
        console.print("[bold red]Nothing selected. Exiting.[/bold red]")
        sys.exit(0)

    if args.dry_run:
        console.print(Panel("[yellow]DRY RUN — no files written.[/yellow]", border_style="yellow"))
        sys.exit(0)

    # ── 5. Transcripts ────────────────────────────────────────────────────────
    step_header(5, TOTAL_STEPS, "Fetching transcripts")
    all_top = top_videos + top_shorts

    if args.transcripts:
        with make_progress() as progress:
            t = progress.add_task("[magenta]Transcripts…", total=len(all_top))
            enrich_with_transcripts(
                all_top,
                progress_callback=lambda c, tot, _: progress.update(t, completed=c)
            )
        console.print(f"[green]✓[/green] Transcripts done for [bold]{len(all_top)}[/bold] items")
    else:
        console.print("[dim]  Skipped — use --transcripts to enable[/dim]")

    # ── 6. Write markdown ─────────────────────────────────────────────────────
    step_header(6, TOTAL_STEPS, "Writing markdown files")
    base_out   = os.path.join(args.output_dir, channel_name)
    videos_dir = os.path.join(base_out, "videos")
    shorts_dir = os.path.join(base_out, "shorts")
    written_total = 0

    if top_videos:
        with make_progress() as progress:
            wt = progress.add_task("[blue]Writing videos…", total=len(top_videos))
            write_all(top_videos, videos_dir,
                      progress_callback=lambda c, t, _: progress.update(wt, completed=c))
        written_total += len(top_videos)

    if top_shorts:
        with make_progress() as progress:
            ws = progress.add_task("[blue]Writing shorts…", total=len(top_shorts))
            write_all(top_shorts, shorts_dir,
                      progress_callback=lambda c, t, _: progress.update(ws, completed=c))
        written_total += len(top_shorts)

    console.print(f"[green]✓[/green] [bold]{written_total}[/bold] markdown files written")

    # ── 7. Reports & CSV ──────────────────────────────────────────────────────
    step_header(7, TOTAL_STEPS, "Generating report & exports")

    if not args.no_report:
        rpath = generate_channel_report(
            channel_name=channel_name,
            all_videos=videos, all_shorts=shorts,
            top_videos=top_videos, top_shorts=top_shorts,
            top_percent=args.top_percent, rank_by=args.rank_by,
            from_date=args.from_date, to_date=args.to_date,
            output_dir=base_out,
        )
        console.print(f"[green]✓[/green] Channel report → [dim]{rpath}[/dim]")

    if args.export_csv:
        sv = sorted(videos, key=lambda x: x.get("score", 0), reverse=True)
        ss = sorted(shorts, key=lambda x: x.get("score", 0), reverse=True)
        export_csv(sv, os.path.join(base_out, "scored_videos.csv"))
        export_csv(ss, os.path.join(base_out, "scored_shorts.csv"))
        console.print(f"[green]✓[/green] CSVs exported → [dim]{base_out}[/dim]")
    else:
        console.print("[dim]  CSV skipped — use --export-csv to enable[/dim]")

    # ── Final panel ───────────────────────────────────────────────────────────
    console.print()
    console.print(Panel(
        f"[bold bright_green]✅  ALL DONE[/bold bright_green]\n\n"
        f"  [bright_cyan]Channel[/]         [bold]{channel_name}[/bold]\n"
        f"  [bright_cyan]Videos written[/]  [bold]{len(top_videos)}[/bold]  →  {videos_dir}\n"
        f"  [bright_cyan]Shorts written[/]  [bold]{len(top_shorts)}[/bold]  →  {shorts_dir}\n"
        f"  [bright_cyan]Total files[/]     [bold bright_green]{written_total}[/bold bright_green]\n"
        f"  [bright_cyan]Report[/]          {os.path.join(base_out, 'channel_report.md')}\n"
        f"  [bright_cyan]Root dir[/]        [yellow]{os.path.abspath(base_out)}[/yellow]",
        title="[bold bright_green]scrapling-cli[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 4),
    ))


if __name__ == "__main__":
    main()
