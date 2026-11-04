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
