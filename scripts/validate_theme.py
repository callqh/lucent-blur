#!/usr/bin/env python3
"""Validate the generated theme against Zed's schema and project invariants."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
THEME_FILES = (
    ROOT / "themes" / "one-dark-pro-blur.json",
    ROOT / "themes" / "quiet-light-blur.json",
)
MANIFEST_FILE = ROOT / "extension.toml"
EXPECTED_THEME_COUNTS = {
    "one-dark-pro-blur.json": 15,
    "quiet-light-blur.json": 3,
}


def main() -> None:
    schema_url = "https://zed.dev/schema/themes/v0.2.0.json"
    request = urllib.request.Request(
        schema_url,
        headers={"User-Agent": "one-dark-pro-blur-validator"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        schema = json.load(response)

    all_names = []
    total = 0
    for theme_file in THEME_FILES:
        theme = json.loads(theme_file.read_text(encoding="utf-8"))
        jsonschema.validate(instance=theme, schema=schema)

        themes = theme["themes"]
        expected_count = EXPECTED_THEME_COUNTS[theme_file.name]
        if len(themes) != expected_count:
            raise ValueError(
                f"Expected {expected_count} themes in {theme_file.name}, "
                f"got {len(themes)}"
            )
        if not all(
            item["style"].get("background.appearance") == "blurred"
            for item in themes
        ):
            raise ValueError(
                f"Every generated theme in {theme_file.name} must use "
                "blurred appearance"
            )

        names = [item["name"] for item in themes]
        all_names.extend(names)
        total += len(themes)

    if len(all_names) != len(set(all_names)):
        raise ValueError("Generated theme names must be unique")

    manifest = MANIFEST_FILE.read_text(encoding="utf-8")
    if not re.search(r'(?m)^version = "\d+\.\d+\.\d+"$', manifest):
        raise ValueError("extension.toml must contain a semantic x.y.z version")

    print(f"Validated {total} themes against {schema_url}")


if __name__ == "__main__":
    main()
