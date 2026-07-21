#!/usr/bin/env python3
"""Bump the extension manifest's semantic version and print the new version."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "extension.toml"
VERSION_PATTERN = re.compile(r'(?m)^version = "(\d+)\.(\d+)\.(\d+)"$')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bump", choices=("patch", "minor", "major"))
    args = parser.parse_args()

    content = MANIFEST.read_text(encoding="utf-8")
    match = VERSION_PATTERN.search(content)
    if not match:
        raise ValueError("extension.toml must contain a semantic x.y.z version")

    major, minor, patch = map(int, match.groups())
    if args.bump == "patch":
        patch += 1
    elif args.bump == "minor":
        minor, patch = minor + 1, 0
    else:
        major, minor, patch = major + 1, 0, 0

    version = f"{major}.{minor}.{patch}"
    updated = VERSION_PATTERN.sub(f'version = "{version}"', content, count=1)
    MANIFEST.write_text(updated, encoding="utf-8")
    print(version)


if __name__ == "__main__":
    main()
