# One Dark Pro Blur for Zed

> [!NOTE]
> Blur is rendered by Zed and the operating system. Its appearance may differ
> between macOS, Linux, Windows, and individual window compositors.

<!-- Separate consecutive GitHub admonitions. -->

> [!IMPORTANT]
> This is an independent blur adaptation of
> [One Dark Pro Enhanced](https://github.com/hadez8877/one-dark-pro-enhanced).
> It is not an official One Dark Pro project.

A translucent, blurred take on the familiar One Dark Pro and Quiet Light
palettes for [Zed](https://zed.dev). It preserves the original syntax and
terminal colors while giving the editor, panels, tabs, and terminal a native
blurred backdrop.

## Features

- Five One Dark Pro color variants and one Quiet Light variant
- Three transparency levels for every variant
- Native Zed `blurred` window appearance
- Transparent editor, panel, tab bar, terminal, toolbar, and gutter layers
- Refined active tabs and active-line highlights for translucent backgrounds
- Reproducible theme generation from vendored upstream files

## Theme variants

Each color variant is available in Light, balanced, and Heavy opacity levels.

| Color variant | Available themes |
| --- | --- |
| One Dark Pro | Light, balanced, Heavy |
| One Dark Pro Darker | Light, balanced, Heavy |
| One Dark Pro Flat | Light, balanced, Heavy |
| One Dark Pro Mix | Light, balanced, Heavy |
| One Dark Pro Night Flat | Light, balanced, Heavy |
| Quiet Light | Light, balanced, Heavy |

Opacity naming refers to the strength of the window background:

- `[Light]`: most transparent, approximately 60% window opacity
- No suffix: balanced, approximately 84% window opacity
- `[Heavy]`: least transparent, approximately 88% window opacity

For most dark setups, start with `One Dark Pro (Blur)`. For a bright,
translucent workspace, select `Quiet Light (Blur)`.

## Installation

Clone the repository:

```sh
git clone https://github.com/callqh/one-dark-pro-blur.git
```

Then install it as a local Zed extension:

1. Open Zed.
2. Open the Extensions page.
3. Select **Install Dev Extension**.
4. Choose the cloned `one-dark-pro-blur` directory.
5. Open the theme selector and select a theme containing `(Blur)`.

You can also run `zed: install dev extension` from the command palette.

After changing theme files locally, run `zed: rebuild dev extension` to reload
the installed development extension.

## Recommended settings

Disable project-panel sticky scroll to prevent its overlay from interrupting
the transparent panel surface:

```json
{
  "project_panel": {
    "sticky_scroll": false
  }
}
```

You can select the balanced theme directly in Zed settings:

```json
{
  "theme": "One Dark Pro (Blur)"
}
```

## Compatibility

The theme controls color and transparency, but Zed and the operating system
provide the final blur effect. Systems without supported window composition may
show transparency without blur or render an opaque fallback.

If the theme loads but does not blur, verify your OS transparency settings and
check the [Zed issue tracker](https://github.com/zed-industries/zed/issues).

## Development

### Generating themes

The generated themes contain 18 variants: five One Dark Pro palettes and one
Quiet Light palette, each multiplied by three opacity levels.

Run the generator after changing blur values or replacing upstream themes:

```sh
python3 generate_themes.py
```

The generator:

1. Reads One Dark Pro Enhanced and Quiet Light themes from `upstream`.
2. Preserves their syntax, terminal, text, and semantic colors.
3. Applies blur-specific transparency and surface overrides.
4. Writes the results to `themes/one-dark-pro-blur.json` and
   `themes/quiet-light-blur.json`.

> [!WARNING]
> Do not edit files in `themes/` directly. They are generated and will be
> overwritten the next time `generate_themes.py` runs.

### Customizing blur levels

Edit `BLUR_LEVELS` in `generate_themes.py` to tune window, surface, active-tab,
and active-line opacity. Edit `TRANSPARENT_LAYERS` to change which Zed surfaces
allow the window backdrop to show through.

Tracked upstream revisions are recorded in
`upstream/one-dark-pro-enhanced.commit` and
`upstream/quiet-light/quiet-light.commit`. Run `python3 sync_upstream.py` to
fetch the latest themes and regenerate all blur variants.

### Automated releases

GitHub Actions validate every change, check the upstream themes for updates,
create versioned GitHub Releases, and open Zed extension store update pull
requests.

See [Releasing One Dark Pro Blur](docs/RELEASING.md) for repository settings,
the required `COMMITTER_TOKEN`, initial store publication, and release steps.

## License

This project retains the Apache License 2.0 used by One Dark Pro Enhanced.
Quiet Light is used under the MIT License. See [LICENSE](LICENSE),
[NOTICE](NOTICE), and the vendored upstream license files for terms,
attribution, and a summary of modifications.

## Credits

- [One Dark Pro](https://github.com/Binaryify/OneDark-Pro) by Binaryify for the
  original One Dark Pro theme.
- [One Dark Pro Enhanced](https://github.com/hadez8877/one-dark-pro-enhanced) by
  Hadez for the Zed color themes used as this project's foundation.
- [Quiet Light for Zed](https://github.com/biaqat/quiet-light-theme-zed) by
  blaqat for the Quiet Light palette and syntax colors.
- [Zed](https://github.com/zed-industries/zed) for native transparent and blurred
  theme support.

Special thanks to [Jens Lystad](https://github.com/jenslys) and
[Catppuccin Blur for Zed](https://github.com/jenslys/zed-catppuccin-blur).
Its thoughtful approach to blurred Zed surfaces, recommended settings, and
upstream-driven generation directly inspired this project.

---

Built with appreciation for the One Dark Pro, Catppuccin, and Zed communities.
