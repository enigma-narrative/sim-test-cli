"""Terminal presentation helpers: Rich tables and y/N confirmation prompts."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

console = Console()


def render_table(title: str, columns: list[str], rows: list[tuple]) -> None:
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    for row in rows:
        table.add_row(*(str(value) for value in row))
    console.print(table)


def confirm(message: str) -> bool:
    answer = input(f"{message} [y/N]: ").strip().lower()
    return answer == "y"
