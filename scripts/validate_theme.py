#!/usr/bin/env python3
"""Validate the generated theme against Zed's schema and project invariants."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
THEME_FILE = ROOT / "themes" / "one-dark-pro-blur.json"
MANIFEST_FILE = ROOT / "extension.toml"
EXPECTED_THEME_COUNT = 15


def main() -> None:
    theme = json.loads(THEME_FILE.read_text(encoding="utf-8"))
    schema_url = theme["$schema"]
    request = urllib.request.Request(
        schema_url,
        headers={"User-Agent": "one-dark-pro-blur-validator"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        schema = json.load(response)

    jsonschema.validate(instance=theme, schema=schema)

    themes = theme["themes"]
    names = [item["name"] for item in themes]
    if len(themes) != EXPECTED_THEME_COUNT:
        raise ValueError(f"Expected {EXPECTED_THEME_COUNT} themes, got {len(themes)}")
    if len(names) != len(set(names)):
        raise ValueError("Generated theme names must be unique")
    if not all(
        item["style"].get("background.appearance") == "blurred" for item in themes
    ):
        raise ValueError("Every generated theme must use blurred appearance")

    manifest = MANIFEST_FILE.read_text(encoding="utf-8")
    if not re.search(r'(?m)^version = "\d+\.\d+\.\d+"$', manifest):
        raise ValueError("extension.toml must contain a semantic x.y.z version")

    print(f"Validated {len(themes)} themes against {schema_url}")


if __name__ == "__main__":
    main()
