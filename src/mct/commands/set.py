"""`mct set default <template_name>` — set the default template in .mctrc."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mct import config


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("set", help="Set values in .mctrc")
    set_subparsers = parser.add_subparsers(dest="set_target", required=True)

    default_parser = set_subparsers.add_parser("default", help="Set the default template")
    default_parser.add_argument("template_name", help="Name of an existing template to make the default")
    default_parser.set_defaults(func=run_default)


def run_default(args: argparse.Namespace) -> None:
    rc_path = config.require_rc(Path.cwd())
    data = config.load(rc_path)
    templates = data.get("templates", [])

    if args.template_name not in templates:
        print(
            f"'{args.template_name}' is not in the templates list. Run `mct add {args.template_name}` first.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    data["default_template"] = args.template_name
    config.save(rc_path, data)
    print(f"Default template set to '{args.template_name}'")
