from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console

from .app import TranscriptResolutionError, run_incremental_fetch
from .cli_common import (
    add_transcript_arguments,
    build_transcript_options,
    describe_cookie_source,
    describe_hosted_asr,
    parse_date_arg,
)
from .cli_ui import render_banner, render_key_values, render_result
from .logging_utils import setup_logging
from .models import FetchNewRunConfig

console = Console()

DEFAULT_CHANNELS = ["https://www.youtube.com/ibmtechnology"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch-new",
        description="Fetch only newly published channel items since the last recorded run",
    )
    parser.add_argument("--channels", "-c", nargs="+", default=DEFAULT_CHANNELS, help="Channels to watch")
    parser.add_argument("--days-back", type=int, default=7, help="Fallback window when state is empty")
    parser.add_argument("--output-dir", "-o", default="output_new", help="Output directory for new items")
    parser.add_argument(
        "--state-file",
        default="state.json",
        help="State file that stores the last successful run date per channel input",
    )
    parser.add_argument("--force-from", type=parse_date_arg, default=None, help="Override last-run date")
    add_transcript_arguments(parser)
    parser.add_argument("--log-file", default=None, help="Optional log file path")
    parser.add_argument("--no-banner", action="store_true", help="Skip the startup banner")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(args.verbose, Path(args.log_file) if args.log_file else None)

    config = FetchNewRunConfig(
        channels=args.channels,
        days_back=args.days_back,
        output_dir=Path(args.output_dir),
        state_file=Path(args.state_file),
        force_from=args.force_from,
        verbose=args.verbose,
        log_file=Path(args.log_file) if args.log_file else None,
        transcript_options=build_transcript_options(args),
    )
    if not args.no_banner:
        render_banner(console, subtitle="Fresh-content fetcher warming up")
    render_key_values(
        console,
        title="Run Config",
        rows=[
            ("Channels", len(args.channels)),
            ("Days back", args.days_back),
            ("Transcripts", "on" if args.transcripts else "off"),
            ("Hosted ASR", describe_hosted_asr(config.transcript_options) if args.transcripts else "n/a"),
            ("Cookies", describe_cookie_source(config.transcript_options) if args.transcripts else "n/a"),
            ("Workers", config.transcript_options.workers if args.transcripts else "n/a"),
            ("Output", config.output_dir),
            ("State file", config.state_file),
        ],
    )
    if (
        args.transcripts
        and describe_hosted_asr(config.transcript_options) != "off"
        and describe_cookie_source(config.transcript_options) == "off"
    ):
        console.print(
            "[yellow]Cookies are off. If YouTube asks yt-dlp to sign in, add "
            "--cookies-from-browser chrome or set YTDLP_COOKIES_FROM_BROWSER=chrome in .env.[/yellow]"
        )
    try:
        result = run_incremental_fetch(config)
    except TranscriptResolutionError as exc:
        render_result(
            console,
            title="Transcript Resolution Failed",
            rows=[("Reason", exc)],
            style="red",
        )
        return 1
    render_result(
        console,
        title="Done",
        rows=[
            ("Channels", len(result.channel_results)),
            ("New files written", result.total_written),
        ],
        style="green",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
