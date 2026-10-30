---
filename: "_ai/backlog/reports/261030_2124__IMPLEMENTATION_REPORT__specs-root-migration.md"
title: "Report: spec-writer specs root migration"
createdAt: 2026-10-30 21:24
updatedAt: 2026-10-30 21:24
project: "ai-coding-prompts"
status: completed
filesCreated: 1
filesModified: 4
filesDeleted: 0
tags: [specs, speckit, spec-writer, skills, conventions]
documentType: IMPLEMENTATION_REPORT
---

# Report: spec-writer specs root migration

## Summary

The `spec-writer` skill now writes specifications to `<repo>/specs/` instead of
`<repo>/_ai/specs/`, following the GitHub Spec Kit default.

## Changes

- `global-skills/spec-writer/SKILL.md` — directory convention, ID glob,
  grounding command, and frontmatter `filename` all use `specs/`.
- `global-skills/spec-writer/assets/SPEC_TEMPLATE.md` — frontmatter filename.
- `global-skills/manage-knowledge-base/SKILL.md` and `kb-structure.md` — the
  knowledge-base map points specs at the repository-root `specs/`.

## Validation

- `rg "_ai/specs"` across the repository — no matches.
- Skills are documentation/asset changes; no test suite. The symlinked
  `~/.config/opencode/skills/spec-writer` reads the canonical source edited here.
