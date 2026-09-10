---
name: okf-validate
description: Validate an Open Knowledge Format (OKF) v0.1 bundle with the bundled validate.py. Enforces the three spec-mandatory rules (every concept has parseable YAML frontmatter, non-empty string `type`, reserved index.md/log.md present) plus `--strict` producer lints (missing recommended fields, broken intra-bundle links, links missing .md extension, orphan concepts). Use when the user asks to "validate an OKF bundle", "check if a bundle is conformant", or wants a CI/publish gate on a bundle.
---

# OKF validate

Runs the bundled `validate.py` against any OKF v0.1 bundle directory.

## Workflow

1. Confirm the bundle dir exists and looks like a bundle (root `index.md`).
2. Run:
   ```
   python3 <skill-dir>/validate.py [--strict] <bundle-dir>
   ```
   Exit codes: `0` conformant · `1` errors (or strict warnings) · `2` bad invocation.
3. Interpret: hard rules are always checked; `--strict` also fails on lint
   warnings. Pass the config as an inline flag; never invent an output.

## Hard rules (OKF v0.1)

- Every `*.md` concept has parseable YAML frontmatter.
- Every concept has a non-empty string `type`.
- Reserved files `index.md` + `log.md` exist at the bundle root.
- `index.md` frontmatter declares `okf_version`.

## Strict lints (`--strict`)

- Missing recommended fields (`title`, `description`).
- Broken intra-bundle `](#MD links resolve to a real file.
- Links missing the `.md` extension.
- Orphan concepts: a non-reserved concept not referenced by `index.md` or any sibling.

## Rules

- Read-only: validate.py never modifies the bundle. Fixes happen as edits, then re-run.
- The verdict is the script's exit code and output; do not paraphrase a pass/fail.
- If PyYAML is missing, validate.py falls back to a minimal frontmatter parser
  (same verdicts for our producers' files).