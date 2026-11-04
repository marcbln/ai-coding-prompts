---
filename: "/home/marc/devel/ai-coding-prompts/_ai/backlog/reports/261104_1239__IMPLEMENTATION_REPORT__docx-to-markdown-skill.md"
title: "Report: docx-to-markdown skill with local image extraction"
createdAt: 2026-11-04 12:39
updatedAt: 2026-11-04 12:39
repoRoot: "/home/marc/devel/ai-coding-prompts"
project: "ai-coding-prompts"
status: complete
filesCreated: 2
filesModified: 0
filesDeleted: 0
tags: [skill, docx, markdown, pandoc, images, skillman]
documentType: IMPLEMENTATION_REPORT
---

# Report: docx-to-markdown skill with local image extraction

## Summary

Added the `docx-to-markdown` global skill, backed by a stdlib-only PEP 723 Python
script that converts a `.docx` to GitHub-flavored Markdown, extracts embedded media
into a sibling `<stem>.assets/` directory, rewrites pandoc's absolute/HTML image
references to relative Markdown links, and reports structural fidelity. The skill was
registered through skillman into the OpenCode and Claude skill directories.

## Prompt used

```text
@~/.config/opencode/skills/implement-plan/SKILL.md
@ /home/marc/devel/ai-coding-prompts/_ai/backlog/active/261104_1154__IMPLEMENTATION_PLAN__docx-to-markdown-skill.md
```

## Files Changed

### Created

- `/home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/SKILL.md:1` —
  trigger description, quick start, workflow contract, requirements, boundaries, and
  manual pandoc fallback.
- `/home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/scripts/docx2md.py:1` —
  pandoc-driven converter, media mapper, reference rewriter, `.docx` structure
  inspector, and fidelity report.
- `/home/marc/devel/ai-coding-prompts/_ai/backlog/reports/261104_1239__IMPLEMENTATION_REPORT__docx-to-markdown-skill.md` —
  this report (not counted in `filesCreated`).

### Modified

- None.

## Key Changes

- **Pandoc extraction:** runs `pandoc -f docx -t gfm --wrap=none --extract-media` in a
  temporary directory, then copies media into the final assets directory.
- **Reference rewrite:** converts `<img src="...">` and `![alt](...)` references to
  relative Markdown images. Angle-bracket destinations are used for paths containing
  whitespace, parentheses, `<>`, or non-ASCII characters.
- **Structure fidelity report:** inspects `word/media/`, `<w:tbl>`, and Heading-style
  `pStyle` values inside the `.docx`, compares them against the generated Markdown,
  and warns when structure was lost or no Heading styles exist.
- **Strict failure modes:** exits `2` when pandoc is missing, `1` for bad input/paths,
  and `3` when an image reference cannot be resolved. `--force` is required to
  overwrite; unrelated files in an existing assets directory are never deleted.
- **Skillman registration:** selected from source `own` and synced into
  `~/.config/opencode/skills`, `~/.opencode/skills`, and `~/.claude/skills` as
  symlinks to the canonical source.

## Deviations from Plan

- **Graceful invalid-`.docx` error.** The plan's verbatim script let
  `zipfile.BadZipFile` escape from `inspect_docx()` as a traceback when the negative
  test truncated a fixture. `convert()` now catches `BadZipFile` and reports
  `error: not a valid .docx (zip) file: ...` with exit code `1`
  (`/home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/scripts/docx2md.py:210`).
  The plan expected a clean pandoc error and no output files; this produces a clean
  error before pandoc is invoked and still writes nothing.
- **Fixture media name.** Pandoc 3.10.2 named the fixture image `rId9.png`, not
  `image1.png` as the plan's example suggested. The validation commands were adjusted
  to the actual name; the converter already handles arbitrary pandoc media names.
- **Skillman `scan` runtime.** A full scan takes roughly 4–5 minutes because the
  library currently contains ~9,000 discovered skill entries; the initial 180 s tool
  timeout was raised rather than changing skillman configuration.

## Technical Decisions

- Kept the script stdlib-only with PEP 723 metadata, so `uv run` needs no dependency
  install and `inspect_docx()` returns a plain tuple.
- Single-pass regex replacement prevents rewritten Markdown images from being
  re-scanned as unresolved references.
- Media is only copied after a successful rewrite; the mapper records desired copies
  and deduplicates by source path and final filename.
- Remote/`data:` references are left untouched and excluded from link resolution
  counts.

## Testing Notes

- `python3 -m py_compile` and `uv run ... --help` succeeded.
- Round-trip fixture (`/tmp/docx2md-check/My Fixture.docx`) produced 1 heading,
  1 table, `Links: 1/1 resolved`, a PNG in `My Fixture.assets/`, and an
  angle-bracket destination because the output path contains a space.
- Re-running without `--force` exited `1` and changed nothing; with `--force` it
  exited `0`.
- Extracted image SHA-256 matched the embedded `word/media/rId9.png`.
- The motivating document (`/topdata/fidelioo-v2/resources/Werbung bei fidelioo4.docx`)
  produced 9 images, `Links: 9/9 resolved`, 0 tables, and the expected
  "no Heading styles found" warning, matching the plan.
- Negative checks: truncated `.docx` failed cleanly with exit `1` and no output;
  masked `PATH` failed with exit `2` and the pandoc hint; a `.md` input failed with
  exit `1`.
- Skillman: `scan` reported the skill valid; `select --source own` succeeded;
  `sync --dry-run` showed three `create` entries; `sync` created all three symlinks;
  `status` shows `docx-to-markdown  own  ok`; `doctor` reported no findings for this
  skill (pre-existing invalid-frontmatter findings elsewhere); `audit --skill
  docx-to-markdown --no-usage` reported 0 findings.

## Usage Examples

```bash
uv run /home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/scripts/docx2md.py \
  "report.docx"
```

Output layout:

```text
report.docx
report.md
report.assets/image1.png
```

Override paths and overwrite:

```bash
uv run /home/marc/devel/ai-coding-prompts/global-skills/docx-to-markdown/scripts/docx2md.py \
  input.docx -o docs/input.md --media-dir docs/input.assets --force
```

Registration commands used:

```bash
skillman scan
skillman select docx-to-markdown --source own
skillman sync --dry-run
skillman sync
skillman status
skillman doctor
skillman audit --skill docx-to-markdown --no-usage
```

## Documentation Updates

- `SKILL.md` documents usage, options, boundaries against Kreuzberg/MarkItDown/AnyDoc
  and the `docx` skill, plus a manual pandoc fallback.
- No `README.md` or `CHANGELOG.md` changes: the repository documents workflows and
  does not maintain a changelog.

## Known Limitations

- Direct-formatting headings (bold paragraphs without Heading styles) remain
  undetectable as headings; the report warns about the absence of Heading styles.
- Text-box-based tables are not `<w:tbl>` elements and may not become Markdown tables.
- Embedded media not referenced by the document is copied as a warning signal but
  not linked.

## Next Steps

- Exercise the skill on a `.docx` with non-ASCII image paths and an existing
  non-empty assets directory to confirm `--force` behaviour on real-world inputs.
- Consider adding an acceptance fixture under a test directory if the repository
  ever adopts a Python test harness.
