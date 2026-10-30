---
name: spec-writer
description: "Write a feature/capability specification as a standalone SPEC document in the repo's specs/ directory — one file per spec plus an index.md (ADR-style), YAML frontmatter with documentType of SPEC, and an OpenSpec-compatible Requirement/Scenario body. Use when asked to write/create/draft a spec, spec out a feature, write requirements, or capture what a system SHALL do before implementation planning."
---

# Spec Writer

Write **specifications** — precise, testable descriptions of *what* a system must do — as
single SPEC documents in `specs/`, indexed like ADRs. A spec is the contract that an
implementation plan and its tests are verified against.

## When to use

Trigger when the user wants to specify behavior before implementation: a new feature or
capability, rework with changed external behavior, an API/interface contract, or a part of
an epic ("spec-first" workflow). Do **not** use for bug fixes that restore documented
behavior, typos, or refactors with no observable change — those need no spec.

## Locations and naming

- Directory: `<repo>/specs/`. Create it (plus `index.md` from
  `assets/INDEX_TEMPLATE.md`) if missing. If the repo already uses that path for
  something else (e.g. an OpenSpec root with `changes/` and `definitions/`), place
  standalone SPEC docs at its top level, next to those subfolders.
- ID: specs are numbered per date like ADRs: `YYMMDD-N`, where `N` is a per-day sequence
  number starting at 1. Glob `specs/SPEC__<YYMMDD>-*__*.md` and take the highest
  existing `N` of that day plus 1; if none exists, `N` is `1`.
- Filename: `SPEC__<YYMMDD-N>__<kebab-case-title>.md`,
  e.g. `SPEC__261016-1__vsf-browser-api.md`.
- One file per spec. Do not combine unrelated capabilities; if the title needs "and", split it.

## Workflow

1. **Ground the spec.** Read existing specs (`rg -n "Requirement:" specs`), the
   relevant code (Glob/Grep/Task), related ADRs in `_ai/technical_decisions/`, and open
   plans in `_ai/backlog/active/`. Prefer extending an existing spec over creating a duplicate.
2. **Resolve ambiguity before writing.** Interview the user (one question at a time) about
   anything unspecified. Never silently guess — unresolved items go into Open Questions as
   `[NEEDS CLARIFICATION: <question>]`, not into requirements.
3. **Assign the ID**, copy `assets/SPEC_TEMPLATE.md` into the directory, and fill the
   frontmatter per the rules below.
4. **Write the body** (see Spec Format).
5. **Update `index.md`**: add the new spec under its year (create the file from
   `assets/INDEX_TEMPLATE.md` if missing).
6. **Self-check** against the checklist below, then report the file path and ask the user
   to review. Keep `status: Draft` until the user approves; only then set `Accepted`.

## Frontmatter rules

```yaml
---
filename: "specs/SPEC__<YYMMDD-N>__<kebab-case-title>.md"
title: "[Short Human Readable Title]"
specId: [YYMMDD-N, e.g. 261016-1]
status: [Draft | Accepted | Implemented | Deprecated | Superseded]
date: [YYYY-MM-DD]
createdAt: [YYYY-MM-DD HH:mm]
updatedAt: [YYYY-MM-DD HH:mm]
priority: [low | medium | high | critical]
estimatedComplexity: [simple | moderate | complex]
tags: [comma, separated, tags]
documentType: SPEC
---
```

- **Never write an `id:` key** — the control plane reserves `id` for its own UUID primary
  key; a non-UUID `id` makes the doc fail to sync. The spec number belongs in `specId:`
  and in the filename.
- Preserve the frontmatter key order; update `updatedAt` on every edit.
- Status lifecycle: `Draft` → `Accepted` (user approved) → `Implemented` (built) →
  `Superseded`/`Deprecated`. When superseding a spec, mark the old one `Superseded` and
  cross-reference both directions in References.

## Spec format (the body)

Sections in order — omit `Non-goals`, `Edge Cases`, or `Open Questions` only if truly empty:

1. `## Objective` — why and what, in 1–3 sentences.
2. `## Scope` — bullet list of what is in.
3. `## Non-goals` — explicit exclusions (YAGNI; prevents scope creep).
4. `## Requirements` — the normative core (grammar below).
5. `## Edge Cases` — boundary and error behavior worth specifying.
6. `## Success Criteria` — measurable, technology-agnostic outcomes
   (e.g. "user completes X in under 2 minutes", "re-run produces 0 duplicate rows").
7. `## Open Questions` — unresolved `[NEEDS CLARIFICATION: …]` items.
8. `## References` — code paths (`file.ts:42`), related ADRs/specs/plans by filename.

### Requirement grammar

```markdown
### Requirement: User Authentication
The system SHALL authenticate users via email/password and SHALL return a JWT on success.

#### Scenario: Successful login
- **WHEN** valid credentials are provided
- **THEN** a JWT token is returned
- **AND** the login is logged

#### Scenario: Invalid credentials
- **WHEN** an unknown email or a wrong password is provided
- **THEN** a generic error is returned
```

Rules (this grammar is OpenSpec-parseable, so spec text can later be lifted into change deltas):

- One `### Requirement: <Name>` per requirement; descriptive name, no numbering needed.
- Normative statements use **SHALL** / **MUST** (avoid should/may unless intentionally
  non-normative). Every "SHALL" should imply a test.
- Every requirement has **at least one** `#### Scenario:` (exactly four `#`). Scenarios use
  `- **WHEN** … / - **THEN** … / - **AND** …` bullets. Never format a scenario as a plain
  bullet, bold line, or `###` header — parsers silently drop it.
- Scenarios describe observable behavior (inputs → outcomes), not implementation.
- Keep implementation choices out of requirements unless they are real constraints
  (protocol, compatibility, deployment). Architectural decisions belong in an ADR
  (`adr-writer`), not in the spec.
- Requirement names are unique within the spec; apply the 10-minute-understandability rule —
  if a capability needs "and", split it.

## Updating an existing spec

- Never silently drop requirement text: revise it and bump `updatedAt`.
- Keep traceability when replacing a requirement (state the change, or add
  `Superseded by …` in References) and update the index entry if the title changed.

## Self-check before handing over

- [ ] Frontmatter complete, `documentType: SPEC`, no `id:` key, `updatedAt` current.
- [ ] Every requirement has ≥1 correctly formatted scenario; wording is SHALL/MUST and testable.
- [ ] Scope and Non-goals present and non-overlapping.
- [ ] Success criteria are measurable and technology-agnostic.
- [ ] No implementation details beyond true constraints; decisions that emerged point to an ADR.
- [ ] `index.md` updated; related specs/ADRs cross-referenced in References.

## Related skills

- `adr-writer` — when the spec forces a technical decision, record it in `_ai/technical_decisions/`.
- `save-plan` — to turn an accepted spec into `_ai/backlog/active/{YYMMDD_HHmm}__IMPLEMENTATION_PLAN__….md`.
