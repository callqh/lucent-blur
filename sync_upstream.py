#!/usr/bin/env python3
"""Sync vendored upstream themes and regenerate blur variants."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

from generate_themes import SOURCE_FILES, main as generate_themes


ROOT = Path(__file__).resolve().parent
UPSTREAMS = (
    {
        "name": "One Dark Pro Enhanced",
        "repository": "hadez8877/one-dark-pro-enhanced",
        "branch": "main",
        "commit_file": ROOT / "upstream" / "one-dark-pro-enhanced.commit",
        "files": tuple(
            (f"themes/{filename}", ROOT / "upstream" / "themes" / filename)
            for filename in SOURCE_FILES
        ),
    },
    {
        "name": "Quiet Light for Zed",
        "repository": "biaqat/quiet-light-theme-zed",
        "branch": "main",
        "commit_file": ROOT / "upstream" / "quiet-light" / "quiet-light.commit",
        "files": (
            (
                "themes/quiet-light.json",
                ROOT / "upstream" / "quiet-light" / "quiet-light.json",
            ),
        ),
    },
)


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


def latest_commit(repository: str, branch: str) -> str:
    url = (
        f"https://api.github.com/repos/{repository}/commits/"
        f"{branch}"
    )
    payload = json.loads(request(url))
    return payload["sha"]


def download_theme(repository: str, commit: str, source_path: str) -> bytes:
    url = (
        f"https://raw.githubusercontent.com/{repository}/"
        f"{commit}/{source_path}"
    )
    content = request(url)
    theme = json.loads(content)
    if not isinstance(theme.get("themes"), list) or not theme["themes"]:
        raise ValueError(f"Upstream theme file is invalid: {source_path}")
    return content


def main() -> None:
    for upstream in UPSTREAMS:
        repository = upstream["repository"]
        commit = latest_commit(repository, upstream["branch"])
        for source_path, destination in upstream["files"]:
            content = download_theme(repository, commit, source_path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
            print(f"Synced {upstream['name']}: {source_path}")

        commit_file = upstream["commit_file"]
        commit_file.parent.mkdir(parents=True, exist_ok=True)
        commit_file.write_text(commit + "\n", encoding="utf-8")
        print(f"Synced {upstream['name']} at {commit}")

    generate_themes()


if __name__ == "__main__":
    main()
