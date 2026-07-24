#!/usr/bin/env python3
"""Validate the generated theme against Zed's schema and project invariants."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
THEME_FILE = ROOT / "themes" / "lucent-blur.json"
MANIFEST_FILE = ROOT / "extension.toml"
EXPECTED_THEME_NAMES = {
    "Lucent Blur Mix",
    "Lucent Blur Flat",
    "Lucent Blur Light",
}


def main() -> None:
    schema_url = "https://zed.dev/schema/themes/v0.2.0.json"
    request = urllib.request.Request(
        schema_url,
        headers={"User-Agent": "lucent-blur-validator"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        schema = json.load(response)

    theme = json.loads(THEME_FILE.read_text(encoding="utf-8"))
    jsonschema.validate(instance=theme, schema=schema)

    themes = theme["themes"]
    names = {item["name"] for item in themes}
    if names != EXPECTED_THEME_NAMES:
        raise ValueError(
            f"Expected themes {sorted(EXPECTED_THEME_NAMES)}, got {sorted(names)}"
        )
    if not all(
        item["style"].get("background.appearance") == "blurred"
        for item in themes
    ):
        raise ValueError("Every generated theme must use blurred appearance")

    manifest = MANIFEST_FILE.read_text(encoding="utf-8")
    if not re.search(r'(?m)^version = "\d+\.\d+\.\d+"$', manifest):
        raise ValueError("extension.toml must contain a semantic x.y.z version")

    print(f"Validated {len(themes)} themes against {schema_url}")


if __name__ == "__main__":
    main()
