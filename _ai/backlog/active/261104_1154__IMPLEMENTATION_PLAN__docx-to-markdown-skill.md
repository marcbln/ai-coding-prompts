---
filename: "_ai/backlog/active/261104_1154__IMPLEMENTATION_PLAN__docx-to-markdown-skill.md"
title: "Add a docx-to-markdown skill with local image extraction"
createdAt: 2026-11-04 11:54
updatedAt: 2026-11-04 11:54
status: draft
priority: medium
tags: [skill, docx, markdown, pandoc, images, skillman]
estimatedComplexity: moderate
documentRevision: 1
sourceSpec: ""
sourceHandoff: ""
sourceAdrs: []
documentType: IMPLEMENTATION_PLAN
---

# Add a `docx-to-markdown` skill with local image extraction

**Sources used:** same-conversation design (no feature spec or design handoff exists for this work); no applicable ADRs in `ai-coding-prompts` (the skillman ADRs govern curation, not this converter).

## Problem

Converting a `.docx` to Markdown is a recurring task, but no current skill covers it. The
tools disagree in ways that silently lose data:

- Pandoc extracts embedded media, but emits absolute paths and HTML `<img>` tags that do
  not survive a move and are not valid portable Markdown.
- The Kreuzberg MCP tool returns text only — `images[].data` is empty. Only its CLI can
  return image bytes, and it does so inside a very large JSON payload.
- MarkItDown needs the optional `docx` extras and does not write image files.
- anydoc explicitly reduces embedded images to alt text.

The result is repeated manual work: run pandoc, move media, rewrite every reference,
and check that nothing broke. This plan captures that workflow in one deterministic,
reusable skill.

## Executive summary

Add a global skill `docx-to-markdown` in the canonical skill source
`~/devel/ai-coding-prompts/global-skills/`. It ships a single stdlib-only PEP 723
Python script that:

1. Runs `pandoc` for `.docx` → GitHub-flavored Markdown with `--extract-media` into a
   temporary directory.
2. Moves extracted media to a sibling `<stem>.assets/` directory.
3. Rewrites pandoc's absolute/HTML image references into relative Markdown links,
   including paths with spaces and non-ASCII characters.
4. Reports headings, tables, and image link resolution, warning when source structure
   (`word/media/`, `<w:tbl>`, Heading styles) was not preserved.

The skill is then registered through skillman (`scan` → `select` → `sync` → `doctor`),
not by hand-creating symlinks.

## Design Decisions & Rejected Alternatives

| Decision | Rationale |
| --- | --- |
| Scope is `.docx` only | Image extraction is the differentiator; PDF/PPTX/XLSX overlap with `markdown-converter` and `pdf`, increasing duplicate-skill risk. |
| Pandoc is the extraction engine | Best docx structure (headings, links, lists, tables), writes media files directly, ubiquitous and already required by the `docx` skill. |
| A script is bundled | The reference rewrite and validation are deterministic and were hand-written twice during discovery; encoding them removes drift. |
| Output is sibling `<stem>.md` + `<stem>.assets/` | Self-contained, collision-free per document; no shared asset folder bookkeeping. |
| Keep pandoc image filenames | Idempotent and predictable; descriptive names require fragile inference. |
| Always validate and report fidelity | The motivating document uses direct bold formatting instead of Heading styles, so its structure vanished silently in both pandoc and Kreuzberg; a visible warning is better. |
| Stdlib-only Python with PEP 723 | No dependency install step; `uv run` works on any machine with pandoc and Python ≥3.12. |
| Register through skillman | Local sources are not vendored (ADR `261025-1`); per-skill symlinks are owned by skillman (ADR `261025-3`). Hand-copying would drift. |

**Rejected alternatives**

- **Kreuzberg CLI as the default.** Emits `![](image_N.png)` at the right positions,
  but requires parsing a 100 MB JSON for a 3.6 MB document, and its headings/tables are
  worse than pandoc's.
- **MarkItDown.** Needs `markitdown[all]` and produces alt text instead of image files.
- **AnyDoc.** Documented to turn embedded images into alt text.
- **`soffice --convert-to`.** Produces PDF, not Markdown; no benefit here.
- **Curating the upstream `markdown-converter` skill instead.** Its engine cannot emit
  image files, so it does not solve the actual problem.

## Project environment

| Item | Value |
| --- | --- |
| Skill source repo | `/home/marc/devel/ai-coding-prompts` |
| Skill directory | `global-skills/docx-to-markdown/` |
| Plan directory | `_ai/backlog/active/` |
| Report directory | `_ai/backlog/reports/` |
| Pandoc | `3.10.2` at `/usr/bin/pandoc` |
| Python | `3.14.7` (`python3`), PEP 723 requires `>=3.12` |
| uv | `0.12.10` |
| skillman CLI | `/home/marc/.local/bin/skillman` |
| Git workflow | No `AGENTS.md` or branch convention in this repo; history commits directly on `main` with conventional commits. Do not create branches or PRs; commit only when explicitly asked. |
| Tooling | No `pyproject.toml`, ruff, mypy, or pytest in this repo. Validate with `python3 -m py_compile` and scripted round-trip fixtures. |

## Phase 1 — Author the skill documentation

**Goal:** Define trigger conditions, the workflow contract, and boundaries against
neighbouring skills.

**Files:**
- [NEW FILE] `global-skills/docx-to-markdown/SKILL.md`

**Steps:**

1. Create the directory.
2. Add the following `SKILL.md` verbatim.

````markdown
---
name: docx-to-markdown
description: Convert a Word .docx document to Markdown and extract its embedded images as local files with relative references. Use when asked to convert a .docx to Markdown, create a Markdown version of a Word file, extract images from a Word document, or read a .docx as text in a repository while keeping its visuals.
---

# DOCX to Markdown

## Overview

Convert one `.docx` into a sibling `.md` file plus a `<stem>.assets/` directory whose
images are referenced through relative Markdown links. Pandoc performs extraction; the
bundled script repairs pandoc's absolute and HTML image references and reports whether
document structure survived the conversion.

## Quick start

```bash
uv run scripts/docx2md.py "report.docx"
```

Output:

```text
report.docx
report.md
report.assets/image1.png
report.assets/image2.png
```

Options:

```text
-o, --out PATH        Markdown output path (default: sibling <stem>.md)
    --media-dir PATH  Image directory (default: <stem>.assets beside the output)
    --force           Overwrite an existing Markdown or image directory
```

## Workflow

1. Run the script on the `.docx`. Do not pre-create the output path.
2. Read the printed report:
   - `Links: N/N resolved` means every image reference points at a real file.
   - Warnings about heading or table counts mean structure may have been lost.
3. If the source uses direct formatting instead of Word Heading styles, expect sparse
   Markdown headings. If headings, tables, or reading order matter, review the affected
   sections and rewrite them by hand before presenting the result.
4. Report the output paths and any fidelity warnings to the user. Never discard the
   warnings silently.

## What the script does

1. Requires `pandoc` on `PATH` and a `.docx` input.
2. Runs pandoc with `--extract-media` into a temporary directory.
3. Copies extracted media into `<stem>.assets/`, keeping pandoc's filenames.
4. Converts `<img src="...">` and `![](...)` references to relative Markdown links,
   using angle-bracket destinations for paths containing spaces or non-ASCII characters.
5. Inspects `word/media/`, `<w:tbl>` and Heading-style paragraphs inside the `.docx` and
   compares them with the generated Markdown.
6. Exits non-zero when a local image reference cannot be resolved.

## Requirements

- `pandoc` 3.x or newer (`pandoc --version`).
- Python 3.12+; the script declares its own PEP 723 metadata, so `uv run` is enough.

If pandoc is missing, stop and tell the user which package to install. Do not switch to
a text-only converter as a silent fallback.

## Boundaries and pitfalls

- **Kreuzberg MCP is text-only.** `kreuzberg_extract_file` returns `images[].data` as an
  empty array. Its CLI can extract bytes, but its JSON is huge and its document structure
  is poorer than pandoc's. Use this skill instead.
- **MarkItDown** needs `markitdown[all]` for `.docx` and does not emit image files.
- **AnyDoc** documents that embedded images become alt text.
- **Do not use the `docx` skill for conversion.** It covers creation, editing, tracked
  changes, and comments. Use this skill when the deliverable is Markdown plus images.
- **Tables and headings can still be lossy.** A `.docx` may lay out content with text
  boxes or direct bold formatting rather than Heading styles and table objects. The
  fidelity report surfaces this; it cannot reconstruct intent.

## Manual fallback

If the script cannot run, the underlying command is:

```bash
pandoc input.docx -f docx -t gfm --wrap=none \
  --extract-media=/tmp/docx-media -o input.md
```

Pandoc writes `<img>` tags with absolute `/tmp/docx-media/...` paths; they must be
rewritten to relative links before the Markdown is usable.
````

**Validation:**
- `uv run --no-project python -c "import pathlib,re; t=pathlib.Path('global-skills/docx-to-markdown/SKILL.md').read_text(); print(t.split('---')[1])"` prints valid-looking frontmatter.
- `name` equals the folder name and the description is under 1024 characters.

## Phase 2 — Implement the converter script

**Goal:** Provide the deterministic conversion, rewrite, validation, and reporting.

**Files:**
- [NEW FILE] `global-skills/docx-to-markdown/scripts/docx2md.py`

**Steps:**

1. Create `scripts/`.
2. Add the following file verbatim.

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""Convert a .docx to Markdown and extract its images beside the output."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

IMAGE_RE = re.compile(r"<img\b[^>]*>|!\[([^\]]*)\]\(([^)]+)\)", re.IGNORECASE)
SRC_ATTR_RE = re.compile(r'\bsrc="([^"]+)"', re.IGNORECASE)
ALT_ATTR_RE = re.compile(r'\balt="([^"]*)"', re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
TABLE_SEP_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", re.MULTILINE
)
REMOTE_RE = re.compile(r"^(?:https?:|data:|mailto:)", re.IGNORECASE)


@dataclass
class Report:
    """Collected fidelity signals for the conversion report."""

    source_images: int = 0
    source_tables: int = 0
    source_headings: int = 0
    images: int = 0
    headings: int = 0
    tables: int = 0
    links: int = 0
    resolved: int = 0
    missing: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def fail(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def require_pandoc() -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        fail(
            "pandoc is not installed or not on PATH (try: sudo apt install pandoc).",
            2,
        )
    return pandoc


def inspect_docx(path: Path) -> tuple[int, int, int]:
    """Return (media files, table elements, Heading-style paragraphs)."""
    images = 0
    tables = 0
    headings = 0
    with zipfile.ZipFile(path) as archive:
        images = sum(
            1
            for name in archive.namelist()
            if name.startswith("word/media/") and not name.endswith("/")
        )
        try:
            with archive.open("word/document.xml") as handle:
                root = ET.parse(handle).getroot()
        except KeyError:
            return images, 0, 0
        for element in root.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            if tag == "tbl":
                tables += 1
            elif tag == "pStyle":
                style = next(
                    (value for key, value in element.attrib.items() if key.endswith("}val")),
                    "",
                ).lower()
                if style.startswith(("heading", "berschrift", "überschrift")):
                    headings += 1
    return images, tables, headings


def render_destination(relative: str) -> str:
    """Wrap destinations that Markdown parsers split on whitespace."""
    if re.search(r"[\s<>()]", relative) or not relative.isascii():
        return f"<{relative}>"
    return relative


class MediaMapper:
    """Map images under pandoc's temporary media root to final asset names."""

    def __init__(self, media_root: Path, media_dir: Path, output_dir: Path) -> None:
        self.media_root = media_root.resolve()
        self.media_dir = media_dir
        self.output_dir = output_dir
        self.by_source: dict[Path, str] = {}
        self.copies: list[tuple[Path, Path]] = []
        self.used: dict[str, Path] = {}

    def _path(self, source: str) -> Path:
        raw = source.strip()
        if raw.startswith("<") and raw.endswith(">"):
            raw = raw[1:-1]
        if raw.startswith("file://"):
            raw = urlparse(raw).path
        raw = unquote(raw)
        path = Path(raw)
        if not path.is_absolute():
            path = self.output_dir / path
        return path

    def _unique_name(self, path: Path) -> str:
        name = path.name
        if name not in self.used:
            self.used[name] = path
            return name
        stem, suffix = path.stem, path.suffix
        index = 2
        while f"{stem}-{index}{suffix}" in self.used:
            index += 1
        name = f"{stem}-{index}{suffix}"
        self.used[name] = path
        return name

    def lookup(self, source: str) -> str | None:
        if REMOTE_RE.match(source.strip()):
            return None
        try:
            resolved = self._path(source).resolve()
        except OSError:
            return None
        try:
            resolved.relative_to(self.media_root)
        except ValueError:
            return None
        if resolved in self.by_source:
            return self.by_source[resolved]
        name = self._unique_name(resolved)
        destination = self.media_dir / name
        relative = os.path.relpath(destination, start=self.output_dir)
        relative = Path(relative).as_posix()
        self.by_source[resolved] = relative
        self.copies.append((resolved, destination))
        return relative


def rewrite_references(
    text: str, mapper: MediaMapper, report: Report
) -> str:
    """Replace pandoc media references with relative Markdown images."""

    def lookup(source: str) -> str | None:
        relative = mapper.lookup(source)
        if relative is not None:
            report.links += 1
            report.resolved += 1
            return relative
        if not REMOTE_RE.match(source.strip()):
            report.links += 1
            report.missing.append(source.strip())
        return None

    def replace_image(match: re.Match[str]) -> str:
        token = match.group(0)
        if token[:4].lower() == "<img":
            src_match = SRC_ATTR_RE.search(token)
            if src_match is None:
                return token
            relative = lookup(src_match.group(1))
            if relative is None:
                return token
            alt_match = ALT_ATTR_RE.search(token)
            alt = alt_match.group(1) if alt_match else ""
        else:
            alt = match.group(1) or ""
            relative = lookup(match.group(2))
            if relative is None:
                return token
        alt = alt.replace("]", r"\]")
        return f"![{alt}]({render_destination(relative)})"

    # Single pass: replacements are not rescanned, so a rewritten Markdown image
    # cannot be mistaken for a second unresolved reference.
    return IMAGE_RE.sub(replace_image, text)


def count_structure(text: str) -> tuple[int, int]:
    headings = len(HEADING_RE.findall(text))
    tables = len(TABLE_SEP_RE.findall(text))
    return headings, tables


def convert(
    input_path: Path,
    output_path: Path,
    media_dir: Path,
) -> Report:
    pandoc = require_pandoc()
    source_counts = inspect_docx(input_path)
    report = Report(
        source_images=source_counts[0],
        source_tables=source_counts[1],
        source_headings=source_counts[2],
    )

    with tempfile.TemporaryDirectory(prefix="docx2md-") as temp:
        temp_dir = Path(temp)
        temp_markdown = temp_dir / "output.md"
        temp_media = temp_dir / "media"

        command = [
            pandoc,
            str(input_path),
            "-f",
            "docx",
            "-t",
            "gfm",
            "--wrap=none",
            f"--extract-media={temp_media}",
            "-o",
            str(temp_markdown),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
            fail(f"pandoc failed: {detail}")

        text = temp_markdown.read_text(encoding="utf-8")
        mapper = MediaMapper(temp_media, media_dir, output_path.parent)
        text = rewrite_references(text, mapper, report)

        if mapper.copies:
            media_dir.mkdir(parents=True, exist_ok=True)
            for source, destination in mapper.copies:
                if not source.is_file():
                    report.missing.append(str(source))
                    continue
                shutil.copy2(source, destination)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")

    report.images = len(mapper.by_source)
    report.headings, report.tables = count_structure(text)

    if report.source_images > report.images:
        report.warnings.append(
            f"source contains {report.source_images} media file(s); "
            f"{report.images} image(s) are referenced in the Markdown"
        )
    if report.source_tables and not report.tables:
        report.warnings.append(
            f"source has {report.source_tables} table(s) but no Markdown table was detected"
        )
    if report.source_headings and not report.headings:
        report.warnings.append(
            f"source has {report.source_headings} Heading-style paragraph(s) "
            "but no Markdown heading was detected"
        )
    if not report.source_headings:
        report.warnings.append(
            "no Heading styles found in the source; headings may use direct formatting"
        )

    return report


def print_report(
    input_path: Path,
    output_path: Path,
    media_dir: Path,
    report: Report,
) -> None:
    print(f"Converted: {input_path} -> {output_path}")
    print(f"Images:    {report.images} file(s) -> {media_dir}")
    print(
        "Structure: "
        f"{report.headings} heading(s), {report.tables} table(s); "
        f"source: {report.source_headings} heading style(s), "
        f"{report.source_tables} table(s)"
    )
    print(f"Links:     {report.resolved}/{report.links} resolved")
    for warning in report.warnings:
        print(f"warning: {warning}")
    for missing in report.missing:
        print(f"missing: {missing}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a .docx to Markdown and extract its images."
    )
    parser.add_argument("input", type=Path, help="Word .docx file to convert")
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        help="Markdown output path (default: sibling <stem>.md)",
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        help="Image directory (default: <stem>.assets beside the output)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing Markdown file or image directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input
    if not input_path.is_file():
        fail(f"input file not found: {input_path}")
    if input_path.suffix.lower() != ".docx":
        fail(f"expected a .docx file, got: {input_path.suffix or 'no suffix'}", 1)

    output_path = args.out or input_path.with_suffix(".md")
    media_dir = args.media_dir or output_path.with_name(output_path.stem + ".assets")

    if output_path.resolve() == input_path.resolve():
        fail("output path must differ from the input path")
    if not args.force:
        if output_path.exists():
            fail(f"{output_path} already exists (use --force to overwrite)")
        if media_dir.exists():
            fail(f"{media_dir} already exists (use --force to overwrite)")

    report = convert(input_path, output_path, media_dir)
    print_report(input_path, output_path, media_dir, report)
    if report.missing:
        fail(f"{len(report.missing)} image reference(s) could not be resolved", 3)


if __name__ == "__main__":
    main()
```

**Validation:**
- `python3 -m py_compile global-skills/docx-to-markdown/scripts/docx2md.py`
- `uv run global-skills/docx-to-markdown/scripts/docx2md.py --help` lists the three options.
- The script exits `2` when `PATH` is masked (`PATH=/usr/bin:/bin` still has pandoc; use a temporary directory without pandoc) and exits `1` for a non-`.docx` input.

**Implementation note:** `--force` overwrites files but never deletes unrelated files in
an existing media directory. `inspect_docx()` returns a plain tuple so the script keeps
its stdlib-only footprint; do not introduce dataclasses for internal counts.

## Phase 3 — Verify with round-trip fixtures and the motivating document

**Goal:** Prove the script preserves text, structure, images, and unusual paths, and
proves the fidelity report catches loss.

**Files:** none committed; fixtures live under `/tmp`.

**Steps:**

1. Create a fixture with a heading, table, bold text, and an embedded PNG:

   ```bash
   mkdir -p /tmp/docx2md-check
   cd /tmp/docx2md-check
   magick -size 60x30 xc:red sample.png
   printf '# Fixture Title\n\nA paragraph with **bold** text.\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\n![sample](sample.png)\n' > fixture.md
   pandoc fixture.md --resource-path=. -o "My Fixture.docx"
   ```

2. Run the converter and assert:

   ```bash
   uv run /home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/scripts/docx2md.py "My Fixture.docx"
   test -f "My Fixture.md"
   test -n "$(find "My Fixture.assets" -name '*.png' -print -quit)"
   grep -q 'Fixture Title' "My Fixture.md"
   grep -q 'My Fixture.assets/.*\.png' "My Fixture.md"
   grep -q '^# ' "My Fixture.md"
   grep -q '^| A *| B *|' "My Fixture.md"
   ```

   Expected report: `Links: 1/1 resolved`, 1 heading, 1 table. The output path contains
   a space, so the image link must use an angle-bracket destination such as
   `<My Fixture.assets/rId9.png>` (pandoc names docx media by relationship id, not
   always `image1.png`).

3. Re-run without `--force`; it must exit non-zero and leave files untouched.

4. Re-run with `--force`; it must succeed.

5. Convert the motivating document and confirm the report flags its known loss:

   ```bash
   uv run /home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/scripts/docx2md.py \
     "/topdata/fidelioo-v2/resources/Werbung bei fidelioo4.docx" \
     -o /tmp/docx2md-check/werbung.md --force
   # expect: Images 9, Links 9/9 resolved, 0 tables in source and Markdown,
   # and the warning "no Heading styles found in the source"
   ```

6. Negative checks:
   - `cp "My Fixture.docx" broken.docx` then truncate it; the script must fail with a
     pandoc error and no output files.
   - Simulate a missing pandoc with
     `PATH=/tmp/emptybin /usr/bin/python3 scripts/docx2md.py "My Fixture.docx" --force`
     (absolute interpreter, because masking `PATH` also hides `uv`); it must exit `2`
     with the pandoc hint.

7. Confirm generated image hashes match the source media:

   ```bash
   unzip -p "My Fixture.docx" word/media/image1.png | sha256sum
   sha256sum "My Fixture.assets/image1.png"
   ```

## Phase 4 — Register and validate through skillman

**Goal:** Make the skill visible to OpenCode/Claude without hand-created symlinks.

**Files:** changes in `~/.config/skillman/config.yaml` and the target skill directories
(managed by skillman; not edited directly).

**Steps:**

1. `skillman scan` — the new skill must appear as valid, not invalid.
2. `skillman select docx-to-markdown --source own`.
3. `skillman sync --dry-run` — confirm a create plan for the three targets; then
   `skillman sync`.
4. `skillman status` — `docx-to-markdown` must be `ok`.
5. `skillman doctor` — no new findings.
6. `skillman audit --skill docx-to-markdown` — review findings; confirm it does not
   cluster with `markdown-converter` or `docx` (different names, but check similarity).
7. Verify the symlink points at the canonical source:
   `readlink -f ~/.config/opencode/skills/docx-to-markdown`.

**Validation:** the skill appears in the OpenCode skill list and the symlink target is
`/home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown`.

## Phase 5 — Housekeeping, documentation, and implementation report

**Goal:** Close out the work with accurate project bookkeeping.

**Files:**
- [NEW FILE] `_ai/backlog/reports/261104_1154__IMPLEMENTATION_REPORT__docx-to-markdown-skill.md`
- [MODIFY] none expected

**Steps:**

1. `.gitignore`: no change. The skill adds only `.md` and `.py` files; `__pycache__` is
   already ignored, and no build artifacts are produced.
2. `README.md`: no change. It documents workflows, not individual skills; skills are
   discovered from `global-skills/` by skillman.
3. `CHANGELOG.md`: no file exists in this repository; do not create one (skill authoring
   guidance forbids auxiliary docs).
4. Run a final `git -C /home/marc/devel/ai-coding-prompts status --short` and confirm only
   the new skill files changed. Do not commit unless asked.
5. Write the implementation report with the frontmatter required by the report contract,
   including:
   - Summary of the skill and script.
   - Files created.
   - Verification results (fixture and real document).
   - Deviations: any pandoc quirks discovered (e.g. image syntax differences between
     pandoc versions) and how the regex handled them.
   - Known limitations: direct-formatting headings, text-box tables, unreferenced media.
   - Usage example and the skillman registration commands.

## Traceability

| Requirement (from design discussion) | Phase |
| --- | --- |
| DOCX-only scope | 1 (SKILL.md boundaries), 2 (suffix check) |
| Pandoc as the engine | 2 |
| Sibling `<stem>.md` + `<stem>.assets/` | 2 |
| Keep pandoc image names | 2 |
| Validate links and report fidelity | 2, 3 |
| SKILL.md + stdlib Python (PEP 723) | 1, 2 |
| No duplicate/conflicting skill | 4 |
| Housekeeping and report | 5 |

## Rollback

The change is additive and isolated: delete `global-skills/docx-to-markdown/`, run
`skillman deselect docx-to-markdown`, then `skillman sync`. No existing skill or config is
modified.
