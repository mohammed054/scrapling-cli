from __future__ import annotations

import logging
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

console = Console()


def setup_logging(verbose: bool, log_file: Path | None = None) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handlers: list[logging.Handler] = [
        RichHandler(console=console, show_time=True, rich_tracebacks=True),
    ]
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers,
        force=True,
    )
    if verbose:
        return
    for logger_name in (
        "scrapling",
        "scrapling.fetchers",
        "httpx",
        "urllib3",
        "openai",
        "patchright",
        "playwright",
    ):
        logging.getLogger(logger_name).setLevel(logging.WARNING)
    if not verbose:
        for logger_name in ("scrapling", "scrapling.fetchers", "httpx", "urllib3", "openai"):
            logging.getLogger(logger_name).setLevel(logging.WARNING)
