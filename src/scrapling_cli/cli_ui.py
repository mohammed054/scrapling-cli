from __future__ import annotations

from collections.abc import Iterable

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def _figlet_text(value: str) -> str:
    try:
        from pyfiglet import figlet_format
    except ImportError:
        return f"=== {value} ==="
    return figlet_format(value, font="slant").rstrip()


def render_banner(console: Console, *, subtitle: str) -> None:
    banner = Text(_figlet_text("SCRAPPING"), style="bold cyan")
    subtitle_text = Text(subtitle, style="bright_white")
    subtitle_text.append("\nTranscript-aware YouTube channel analysis", style="dim")
    console.print()
    console.print(
        Panel.fit(
            Text.assemble(banner, "\n", subtitle_text),
            border_style="bright_magenta",
            box=box.ASCII,
            padding=(1, 2),
        )
    )


def render_key_values(console: Console, *, title: str, rows: Iterable[tuple[str, object]]) -> None:
    table = Table.grid(padding=(0, 2))
    table.add_column(style="cyan", no_wrap=True)
    table.add_column(style="bright_white")
    for label, value in rows:
        table.add_row(label, str(value))
    console.print(
        Panel.fit(
            table,
            title=f"[bold]{title}[/bold]",
            border_style="bright_black",
            box=box.ASCII,
            padding=(0, 1),
        )
    )


def render_result(console: Console, *, title: str, rows: Iterable[tuple[str, object]], style: str) -> None:
    table = Table.grid(padding=(0, 2))
    table.add_column(style="cyan", no_wrap=True)
    table.add_column(style="bright_white")
    for label, value in rows:
        table.add_row(label, str(value))
    console.print(
        Panel.fit(
            table,
            title=f"[bold {style}]{title}[/bold {style}]",
            border_style=style,
            box=box.ASCII,
            padding=(0, 1),
        )
    )
