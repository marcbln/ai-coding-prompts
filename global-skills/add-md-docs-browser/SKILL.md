---
name: add-md-docs-browser
description: Integrate the shared md-docs-toolkit themed Markdown docs browser into a host Python project (Typer CLI). Use when a project that does NOT yet depend on md-docs-toolkit needs an interactive, themed "docs" command that browses and renders its Markdown docs in the terminal — e.g. "add a themed docs browser", "add a docs command", "wire up md-docs", "integrate the themed docs TUI". Covers adding the dependency, the thin adapter (DocsSettings + SettingsReader), flag wiring, and validation.
---

# Add the Themed MD-Docs Browser to a Host Project

## The mental model — you are writing a thin adapter

The `md-docs-toolkit` package (`md_docs`) is a **config-agnostic, host-agnostic
core** that owns ALL docs logic: tree discovery, slug mapping, Rich themed
rendering, InquirerPy interactive browsing, and `--list` / `--list-themes`
output. It deliberately contains **no Typer** and no host configuration.

**Your job in the host is only three things:**
1. Add the dependency.
2. Tell the core where the docs live and what theme keys map to what.
3. Register a CLI command that forwards the standard flags to
   `md_docs.cli.run_docs`.

All browser/theme/rendering logic lives in the core — do NOT reimplement any of
it in the host. Mirror the canonical `workspace-manager` integration
(`src/workspace_manager/commands/docs_cmd.py`).

## 1. Add the dependency

The package is installed from GitHub (tagged releases):

```toml
# pyproject.toml — use uv
"md-docs-toolkit @ git+https://github.com/topdata-software-gmbh/md-docs-toolkit.git@v0.1.0"
```

```bash
uv add "md-docs-toolkit @ git+https://github.com/topdata-software-gmbh/md-docs-toolkit.git@v0.1.0"
```

## 2. The three core entry points (reference)

All imports come from `md_docs.cli`:

- `DocsSettings` — frozen dataclass the host fills in:
  `docs_dir: Path`, `theme: str | None`, `pygments: str | None`,
  `default_theme: str = "monokai"`, `prefix: str = "md-docs"`.
- `SettingsReader = Callable[[str], str | None]` — a callable that maps a
  dotted host config key (e.g. `"ui.theme"`) to a string, or `None` if unset.
- `run_docs(settings, settings_reader=None, *, slug, docs_dir, theme, pygments,
  list_docs, list_themes)` — the one function you call.

**Resolution precedence** (per option): explicit CLI argument > injected
`settings_reader` config > `DocsSettings` field / `default_theme`.

**Command precedence inside `run_docs`:** `list_themes` > `list_docs` > `slug` >
interactive (TTY only; non-TTY prints the slug list).

## 3. Create the command module

Below is the full canonical adapter, adapted from `workspace-manager`. Keep the
structure; substitute your host's config loader and prefix.

```python
"""``<host> docs`` — themed Markdown docs browser (shared md-docs-toolkit core).

Thin adapter: resolves the docs directory and theme/pygments settings from host
config and delegates to :func:`md_docs.cli.run_docs`, which owns all
discovery/rendering/browsing logic. No docs-browser logic lives here — only the
host-side config mapping.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from md_docs.cli import DocsSettings, run_docs

# TODO: import your host's config loader, e.g.:
# from workspace_manager.config import load_global_config

#: Bundled docs folder (repo-located; browsed by default).
#: This file sits under src/<pkg>/commands/, so N parents up is repo root.
#: workspace-manager: parents[3] -> repo root. Adjust for your depth.
DOCS_DIR = Path(__file__).resolve().parents[3] / "docs"


def _settings_reader(key: str) -> str | None:
    """Read dotted config keys (``ui.theme``, ``docs.docs_dir``) from host
    config; returns ``None`` when unset/malformed."""
    cfg: dict[str, Any] = load_global_config()  # YOUR loader here
    section, _, field = key.partition(".")
    block = cfg.get(section) if isinstance(cfg.get(section), dict) else None
    if isinstance(block, dict):
        value = block.get(field)
        if isinstance(value, str):
            return value
    return None


def _resolve_docs_dir(override: Path | None) -> Path:
    if override is not None:
        return override
    configured = _settings_reader("docs.docs_dir")
    if configured:
        candidate = Path(configured).expanduser()
        if candidate.is_dir():
            return candidate
    return DOCS_DIR


def docs(
    slug: str | None = typer.Argument(None, help="Doc slug to open directly."),
    docs_dir: Path | None = typer.Option(None, "--docs-dir", help="Override docs folder."),
    theme: str | None = typer.Option(None, "--theme", help="UI theme name."),
    pygments: str | None = typer.Option(None, "--pygments-theme", help="Pygments code theme."),
    list_docs: bool = typer.Option(False, "--list", help="List available doc slugs."),
    list_themes: bool = typer.Option(False, "--list-themes", help="List UI themes."),
) -> None:
    """Browse or open <host> documentation (Markdown) in the terminal."""
    settings = DocsSettings(
        docs_dir=_resolve_docs_dir(docs_dir),
        theme=theme,
        pygments=pygments,
        default_theme="monokai",
        prefix="<host>",  # e.g. "wm", "sb", "tt" — used in warnings
    )
    run_docs(
        settings,
        _settings_reader,
        slug=slug,
        theme=theme,
        pygments=pygments,
        list_docs=list_docs,
        list_themes=list_themes,
    )
```

### Given the command framework (Typer app)

Attach `docs` to your Typer app under the same group as your other commands:

```python
app = typer.Typer(help="<host> command line tools")
app.command()(docs)
```

## 4. The `_resolve_docs_dir` / `parents[N]` path trick

`DOCS_DIR` points at the repository's `docs/` folder as a default. Because the
file lives at `src/<pkg>/commands/docs_cmd.py`, `parents[N]` climbs up to the
repo root. In workspace-manager the file is 3 levels under root:

- `docs_cmd.py` → `commands/` → `<pkg>/` → `src/` → **repo root** = `parents[3]`.

Adjust `N` to your file's depth. When in doubt, compute it explicitly:
`Path(__file__).resolve().parents[N] / "docs"`.

## 5. Prefix and theme defaults

- `prefix` is prepended to stderr warnings (e.g. `wm: theme 'x' not found`).
  Use your host's short name.
- `default_theme="monokai"` matches the toolkit's guaranteed fallback theme.
- `pygments_theme` falls back to `default_theme` when the name is unknown
  (falls back gracefully to Monokai's Pygments style).

## 6. Validation checklist

Run these in the host repo and confirm each works:

- [ ] `uv sync` succeeds — the dependency installs cleanly.
- [ ] `<cmd> docs --list` prints the sorted doc slugs under your `docs/`.
- [ ] `<cmd> docs --list-themes` prints the bundled theme names + descriptions.
- [ ] `<cmd> docs about` (or any known slug) renders the Markdown themed.
- [ ] `<cmd> docs` on a TTY opens the interactive cursor-navigable tree
      (arrow keys move, `.. (up)` climbs, `exit` quits).
- [ ] An unknown `--theme` warns on stderr and falls back to `monokai` without
      crashing.
- [ ] Non-TTY invocation (`<cmd> docs | cat`) falls back to the plain slug list
      instead of hanging on the interactive prompt.
