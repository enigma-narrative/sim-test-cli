"""Top-level argparse dispatch for the mct CLI."""

from __future__ import annotations

import argparse

from mct.commands import add, init, ls, new, rm, set as set_cmd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mct", description="Manage and clone git template repositories")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init.add_parser(subparsers)
    ls.add_parser(subparsers)
    add.add_parser(subparsers)
    rm.add_parser(subparsers)
    new.add_parser(subparsers)
    set_cmd.add_parser(subparsers)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
