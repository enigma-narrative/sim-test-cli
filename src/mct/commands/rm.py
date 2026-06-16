"""`mct rm` — remove template names from the active .mctrc, after confirmation."""

from __future__ import annotations

import argparse
from pathlib import Path

from mct import config, ui


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("rm", help="Remove templates from .mctrc")
    parser.add_argument("templates", nargs="+", help="Template repository names to remove")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    rc_path = config.require_rc(Path.cwd())
    data = config.load(rc_path)
    existing = data.get("templates", [])

    existing_set = set(existing)
    requested_set = set(args.templates)
    union = sorted(existing_set | requested_set)

    rows = []
    for name in union:
        if name in existing_set and name in requested_set:
            status = "DELETE"
        elif name in existing_set:
            status = "KEEP"
        else:
            status = "NO EXIST"
        rows.append((name, status))

    ui.render_table("Templates", ["Template", "Status"], rows)
    if not ui.confirm("Remove DELETE-marked templates?"):
        print("Aborted.")
        return

    data["templates"] = [name for name in existing if name not in requested_set]
    config.save(rc_path, data)
    print(f"Updated {rc_path}")
