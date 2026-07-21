#!/usr/bin/env python3
"""Sync vendored One Dark Pro Enhanced themes and regenerate blur variants."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from generate_themes import SOURCE_FILES, main as generate_themes


ROOT = Path(__file__).resolve().parent
UPSTREAM_REPOSITORY = "hadez8877/one-dark-pro-enhanced"
UPSTREAM_BRANCH = "main"
COMMIT_FILE = ROOT / "upstream" / "one-dark-pro-enhanced.commit"
THEME_DIR = ROOT / "upstream" / "themes"


def request(url: str) -> bytes:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "one-dark-pro-blur-sync",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with urllib.request.urlopen(
        urllib.request.Request(url, headers=headers), timeout=30
    ) as response:
        return response.read()


def latest_commit() -> str:
    url = (
        f"https://api.github.com/repos/{UPSTREAM_REPOSITORY}/commits/"
        f"{UPSTREAM_BRANCH}"
    )
    payload = json.loads(request(url))
    return payload["sha"]


def download_theme(commit: str, filename: str) -> bytes:
    url = (
        f"https://raw.githubusercontent.com/{UPSTREAM_REPOSITORY}/"
        f"{commit}/themes/{filename}"
    )
    content = request(url)
    theme = json.loads(content)
    if not isinstance(theme.get("themes"), list) or not theme["themes"]:
        raise ValueError(f"Upstream theme file is invalid: {filename}")
    return content


def main() -> None:
    commit = latest_commit()
    THEME_DIR.mkdir(parents=True, exist_ok=True)

    for filename in SOURCE_FILES:
        content = download_theme(commit, filename)
        (THEME_DIR / filename).write_bytes(content)
        print(f"Synced {filename}")

    COMMIT_FILE.write_text(commit + "\n", encoding="utf-8")
    generate_themes()
    print(f"Synced One Dark Pro Enhanced at {commit}")


if __name__ == "__main__":
    main()
