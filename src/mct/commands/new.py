"""`mct new` — clone a template repo under a new name and rebrand its remote."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mct import config, git_ops


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("new", help="Clone a template under a new project name")
    parser.add_argument(
        "--template_site_path",
        default=None,
        help="Override the template_site_path from .mctrc for this invocation",
    )
    parser.add_argument(
        "--username",
        default=None,
        help="Override the username from .mctrc for this invocation",
    )
    parser.add_argument("--template", required=True, help="Name of the template repository to clone")
    parser.add_argument("new_name", help="Name for the new project / clone destination")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    rc_path = config.require_rc(Path.cwd())
    data = config.load(rc_path)

    template_site_path = args.template_site_path or data.get(
        "template_site_path", config.DEFAULT_TEMPLATE_SITE_PATH
    )
    username = args.username or data.get("username")
    if not username:
        print("No username available from .mctrc or --username override.", file=sys.stderr)
        raise SystemExit(1)

    base_url = template_site_path.rstrip("/") + "/" + username
    template_url = f"{base_url}/{args.template}.git"
    dest = Path.cwd() / args.new_name

    print(f"Checking that {template_site_path} is reachable...")
    if not git_ops.server_reachable(template_site_path):
        print(f"Could not reach {template_site_path}.", file=sys.stderr)
        raise SystemExit(1)

    print(f"Checking that template {args.template} exists...")
    if not git_ops.remote_repo_exists(template_url):
        print(f"Template repository not found: {template_url}", file=sys.stderr)
        raise SystemExit(1)

    if dest.exists():
        print(f"{dest} already exists in the working directory.", file=sys.stderr)
        raise SystemExit(1)

    print(f"Cloning {template_url} into {dest}...")
    repo = git_ops.clone(template_url, dest)

    new_repo_url = f"{base_url}/{args.new_name}.git"
    git_ops.set_origin_url(repo, new_repo_url)
    print(f"Remote origin set to {new_repo_url}")

    if git_ops.remote_repo_exists(new_repo_url):
        print(f"{new_repo_url} already exists. You can push to it now.")
    else:
        print(f"{new_repo_url} does not exist yet. Create it before pushing.")
