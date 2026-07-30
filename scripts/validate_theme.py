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
    "Lucent Blur Mix [Light]",
    "Lucent Blur Mix [Blur]",
    "Lucent Blur Mix [Heavy]",
    "Lucent Blur Flat [Light]",
    "Lucent Blur Flat [Blur]",
    "Lucent Blur Flat [Heavy]",
    "Lucent Blur Light [Light]",
    "Lucent Blur Light [Blur]",
    "Lucent Blur Light [Heavy]",
}
EXPECTED_ALPHA_BY_LEVEL = {
    "Light": {
        "background": "99",
        "surface.background": "8c",
        "status_bar.background": "99",
        "title_bar.background": "99",
        "tab.active_background": "30",
        "editor.active_line.background": "14",
    },
    "Blur": {
        "background": "d7",
        "surface.background": "d0",
        "status_bar.background": "d7",
        "title_bar.background": "d7",
        "tab.active_background": "40",
        "editor.active_line.background": "20",
    },
    "Heavy": {
        "background": "e0",
        "surface.background": "db",
        "status_bar.background": "e0",
        "title_bar.background": "e0",
        "tab.active_background": "50",
        "editor.active_line.background": "2c",
    },
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
    for item in themes:
        level = item["name"].rsplit("[", 1)[-1].rstrip("]")
        for key, expected_alpha in EXPECTED_ALPHA_BY_LEVEL[level].items():
            actual_alpha = item["style"][key][-2:].lower()
            if actual_alpha != expected_alpha:
                raise ValueError(
                    f"{item['name']} {key} must use alpha "
                    f"{expected_alpha}, got {actual_alpha}"
                )

    manifest = MANIFEST_FILE.read_text(encoding="utf-8")
    if not re.search(r'(?m)^version = "\d+\.\d+\.\d+"$', manifest):
        raise ValueError("extension.toml must contain a semantic x.y.z version")

    print(f"Validated {len(themes)} themes against {schema_url}")


if __name__ == "__main__":
    main()
