"""`mct ls` — list all templates recorded in the active .mctrc."""

from __future__ import annotations

import argparse
from pathlib import Path

from mct import config, ui


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("ls", help="List templates recorded in .mctrc")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    rc_path = config.require_rc(Path.cwd())
    data = config.load(rc_path)
    templates = data.get("templates", [])
    ui.render_table("Templates", ["Template"], [(t,) for t in templates])
