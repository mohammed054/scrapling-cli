from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console

from .app import run_incremental_fetch
from .cli_common import add_transcript_arguments, build_transcript_options, parse_date_arg
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
    result = run_incremental_fetch(config)
    console.print(f"[green]Done.[/green] New files written: {result.total_written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
