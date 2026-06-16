"""Discovery, loading, and saving of the .mctrc TOML config file."""

from __future__ import annotations

import sys
from pathlib import Path

import toml

MCTRC_FILENAME = ".mctrc"

DEFAULT_TEMPLATE_SITE_PATH = "https://github.com"


def discover_rc(start: Path) -> Path | None:
    """Walk upward from `start` to the drive root looking for .mctrc.

    Returns the path to the first .mctrc found, or None if none exists.
    """
    current = start.resolve()
    while True:
        candidate = current / MCTRC_FILENAME
        if candidate.is_file():
            return candidate
        if current.parent == current:
            return None
        current = current.parent


def load(path: Path) -> dict:
    return toml.load(path)


def save(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        toml.dump(data, f)


def require_rc(cwd: Path) -> Path:
    """Find the active .mctrc or exit with an error telling the user to run `mct init`."""
    rc_path = discover_rc(cwd)
    if rc_path is None:
        print("No .mctrc found. Run `mct init` first.", file=sys.stderr)
        raise SystemExit(1)
    return rc_path
