"""`mct add` — add template names to the active .mctrc, after confirmation."""

from __future__ import annotations

import argparse
from pathlib import Path

from mct import config, ui


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("add", help="Add templates to .mctrc")
    parser.add_argument("templates", nargs="+", help="Template repository names to add")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    rc_path = config.require_rc(Path.cwd())
    data = config.load(rc_path)
    existing = data.get("templates", [])

    ui.render_table("Templates to add", ["Template"], [(t,) for t in args.templates])
    if not ui.confirm("Add these templates?"):
        print("Aborted.")
        return

    merged = list(existing)
    for name in args.templates:
        if name not in merged:
            merged.append(name)

    data["templates"] = merged
    config.save(rc_path, data)
    print(f"Updated {rc_path}")
