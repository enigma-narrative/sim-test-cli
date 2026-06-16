"""Wrappers around GitPython and requests for remote-repo verification and cloning."""

from __future__ import annotations

from pathlib import Path

import requests
from git import Git, GitCommandError, Repo


def server_reachable(base_url: str, timeout: float = 5.0) -> bool:
    """True if an HTTP GET to base_url succeeds without a server error."""
    try:
        response = requests.get(base_url, timeout=timeout)
    except requests.RequestException:
        return False
    return response.status_code < 500


def remote_repo_exists(url: str) -> bool:
    """True if `git ls-remote <url>` succeeds, meaning the repo exists and is reachable."""
    try:
        Git().ls_remote(url)
    except GitCommandError:
        return False
    return True


def clone(url: str, dest: Path) -> Repo:
    return Repo.clone_from(url, dest)


def set_origin_url(repo: Repo, url: str) -> None:
    repo.remotes.origin.set_url(url)
