"""`mct init` — create an .mctrc file in the current directory."""

from __future__ import annotations

import argparse
from pathlib import Path

from mct import config, ui


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("init", help="Create an .mctrc file in the current directory")
    parser.add_argument(
        "--template_site_path",
        default=config.DEFAULT_TEMPLATE_SITE_PATH,
        help=f"Base URL of the git hosting site (default: {config.DEFAULT_TEMPLATE_SITE_PATH})",
    )
    parser.add_argument("--username", required=True, help="Your username on the git hosting site")
    parser.add_argument("templates", nargs="*", help="Template repository names")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    rc_path = Path.cwd() / config.MCTRC_FILENAME
    if rc_path.is_file():
        if not ui.confirm(f"{rc_path} already exists. Overwrite it?"):
            print("Aborted.")
            return

    templates = list(args.templates)
    data = {
        "template_site_path": args.template_site_path,
        "username": args.username,
        "templates": templates,
    }
    if templates:
        data["default_template"] = templates[0]
    config.save(rc_path, data)
    print(f"Created {rc_path}")
