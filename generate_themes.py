#!/usr/bin/env python3
"""Generate blurred themes from the vendored upstream themes.

The generated theme files are modified derivatives of One Dark Pro Enhanced
and Quiet Light. See NOTICE and LICENSE for attribution and licensing details.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "upstream" / "themes"
QUIET_LIGHT_SOURCE = ROOT / "upstream" / "quiet-light" / "quiet-light.json"
THEME_DIR = ROOT / "themes"

# Alpha is expressed as the final byte in Zed's #RRGGBBAA colors.
BLUR_LEVELS = {
    "light": {
        "window": "99",
        "surface": "8c",
        "active_tab": "30",
        "active_line": "14",
    },
    "medium": {
        "window": "d7",
        "surface": "d0",
        "active_tab": "40",
        "active_line": "20",
    },
    "heavy": {
        "window": "e0",
        "surface": "db",
        "active_tab": "50",
        "active_line": "2c",
    },
}

SOURCE_FILES = (
    "oneDark-Pro.json",
    "oneDark-Pro-darker.json",
    "oneDark-Pro-flat.json",
    "oneDark-Pro-mix.json",
    "oneDark-Pro-night-flat.json",
)

THEME_GROUPS = (
    {
        "name": "One Dark Pro Blur",
        "author": (
            "One Dark Pro Enhanced contributors; blur adaptation contributors"
        ),
        "sources": tuple(SOURCE_DIR / source_file for source_file in SOURCE_FILES),
        "output": THEME_DIR / "one-dark-pro-blur.json",
    },
    {
        "name": "Quiet Light Blur",
        "author": "blaqat; blur adaptation contributors",
        "sources": (QUIET_LIGHT_SOURCE,),
        "output": THEME_DIR / "quiet-light-blur.json",
    },
)

TRANSPARENT_LAYERS = (
    "editor.background",
    "editor.gutter.background",
    "panel.background",
    "tab_bar.background",
    "tab.inactive_background",
    "terminal.background",
    "toolbar.background",
    "scrollbar.track.background",
)


def with_alpha(color: str, alpha: str) -> str:
    """Return a Zed hex color with a replaced alpha channel."""
    if not isinstance(color, str) or not color.startswith("#"):
        raise ValueError(f"Expected a hex color, got {color!r}")
    if len(color) == 9:
        color = color[:7]
    if len(color) != 7:
        raise ValueError(f"Expected #RRGGBB or #RRGGBBAA, got {color!r}")
    return color + alpha


def theme_name(source_name: str, level: str) -> str:
    suffix = "" if level == "medium" else f" [{level.capitalize()}]"
    return f"{source_name} (Blur){suffix}"


def apply_blur(source_theme: dict, level: str) -> dict:
    theme = deepcopy(source_theme)
    style = theme["style"]
    alpha = BLUR_LEVELS[level]

    theme["name"] = theme_name(theme["name"], level)
    style["background.appearance"] = "blurred"

    # Keep each One Dark Pro variant's own base colors, changing opacity only.
    for key in ("background", "status_bar.background", "title_bar.background"):
        style[key] = with_alpha(style[key], alpha["window"])

    style["surface.background"] = with_alpha(
        style["surface.background"], alpha["surface"]
    )

    for key in TRANSPARENT_LAYERS:
        style[key] = "#00000000"

    # Pane tabs are shared by editor and terminal panes. Keep active tabs and
    # editor lines visible without turning them into opaque slabs over the blur.
    style["tab.active_background"] = with_alpha(
        style["tab.active_background"], alpha["active_tab"]
    )
    style["editor.active_line.background"] = with_alpha(
        style["editor.active_line.background"], alpha["active_line"]
    )

    # Popovers should stay readable, while borders remain light over the blur.
    style["panel.overlay_background"] = style["surface.background"][:7]
    for key in (
        "border",
        "border.variant",
        "border.focused",
        "border.selected",
        "border.transparent",
        "border.disabled",
    ):
        if isinstance(style.get(key), str):
            style[key] = with_alpha(style[key], "30")

    style["scrollbar.thumb.border"] = "#00000000"
    return theme


def generate_theme_group(group: dict) -> int:
    generated = {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": group["name"],
        "author": group["author"],
        "themes": [],
    }

    for source_file in group["sources"]:
        source = json.loads(source_file.read_text(encoding="utf-8"))
        for source_theme in source["themes"]:
            for level in BLUR_LEVELS:
                generated["themes"].append(apply_blur(source_theme, level))

    output_file = group["output"]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        json.dumps(generated, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    count = len(generated["themes"])
    print(f"Generated {count} themes in {output_file}")
    return count


def main() -> None:
    total = sum(generate_theme_group(group) for group in THEME_GROUPS)
    print(f"Generated {total} themes total")


if __name__ == "__main__":
    main()
