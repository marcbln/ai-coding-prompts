---
name: init-goals
description: "Establish or refresh a repo's `_ai/goals.md` — a short, agent-facing statement of what the project is primarily for, its primary goals, non-goals, and how success is judged — then link it from `AGENTS.md`. Use when asked to init goals, create or define project goals, write `_ai/goals.md`, state what a project is for, or refresh existing goals. For a full project charter with ranked trade-offs and invariants, use `init-vision` instead."
license: Apache-2.0
metadata:
  version: "1.0.0"
  standard: "agentskills.io"
---

# init-goals

Establish or refresh a repo's **`_ai/goals.md`**: a short, agent-facing statement
of what the project is primarily for, what it is not for, and how success is
judged. Then make sure `AGENTS.md` points at it.

The point is not documentation for its own sake. Agents infer intent from code
every session; a goals file records intent once, so scope decisions resolve
against a stated purpose instead of being re-argued.

## When to use

- The user asks to create, define, or refresh project goals.
- A repo has an `AGENTS.md` but no `_ai/goals.md`.
- The user asks "what is this project for?" and wants it written down.
- A goals doc exists but no longer matches the repo.

## When not to use

- The user wants a full charter with ranked trade-offs, invariants, and
  decision heuristics. Use `init-vision` (`VISION.md`) instead; the two can
  coexist.
- The user wants requirements or a roadmap. Use `spec-writer`, `create-epic`, or
  `create-masterplan`.
- A one-off explanation is enough and no file is wanted.

## Core principle

Goals must be **specific and checkable**. Reject corporate platitudes such as
"clean code", "scalable", or "fast". A non-goal must name something a
contributor might plausibly propose and that this skill should reject. Never
invent facts: anything inferred from the repo is shown to the user for approval.

---

## Workflow

### 1. Gather evidence

Read, in this order, whatever exists:

1. `README.md` — purpose, audience, quick start.
2. Manifests — `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.
3. Top-level layout and entry points — what the product actually is.
4. `specs/`, `_ai/`, ADRs, and recent commits — stated intent and constraints.

Note the stack, who the project serves, what it does, and what it plainly is not.
If the repo reveals nothing, that is the signal to ask rather than guess.

### 2. Check existing state

- **No `_ai/goals.md`** → create mode.
- **Existing `_ai/goals.md`** → update mode: read it first, keep wording that is
  still true, and propose targeted edits. Never wholesale-replace a curated doc.
  Show the proposed diff before writing.

### 3. Draft the document

Start from `assets/goals.template.md` (next to this file).

**Required sections**

- *What this project is for*
- *Primary goals*
- *Non-goals*
- *How we judge success*

**Optional sections** — include only when the repo supports real content; drop
them otherwise rather than leaving empty headings:

- *Who it is for*
- *Constraints and simplicity*
- *Platform support*

Section guidance:

- *What this is for*: one or two short paragraphs. Name the job and the tool or
  workflow it replaces.
- *Primary goals*: three to five numbered, concrete goals. Each should be
  visible in the repo or stated by the user.
- *Non-goals*: three to five bullet points naming likely-but-rejected scope,
  each with a short reason or the tool that handles it instead.
- *How we judge success*: short, observable bullets — what a user can do, not
  internal metrics invented from nothing.

### 4. Ask only for gaps

If purpose or non-goals cannot be inferred, ask focused questions — one at a
time — covering only what is missing:

1. What does this replace, and what is frustrating about the old tool?
2. Who is it for?
3. What should it deliberately never do?
4. Which platforms or environments must it support?

Do not interview when the repo already answers these.

### 5. Get explicit approval

Show the full draft (create mode) or the proposed diff (update mode). Wait for
an explicit yes. Revise on feedback; never fall back to writing anyway.

### 6. Write the file

Create `_ai/` if needed and write `_ai/goals.md` in plain language, present
tense, short paragraphs. Do not add a changelog or dated update sections.

### 7. Wire `AGENTS.md`

- **No `AGENTS.md`** → create a minimal one with a `## Read first` section that
  links the goals doc.
- **Existing `AGENTS.md`** → ensure it has a `## Read first` section and add one
  line pointing at `_ai/goals.md` with a one-line summary. Preserve everything
  else; do not reorder or rewrite unrelated content.
- **Already linked** → leave it alone; do not duplicate the link.
- **Generated file** (contains a "generated"/"do not edit" banner) → edit the
  source that generates it if it is obvious; otherwise report the needed change
  instead of editing the generated file.

Never edit `README.md` or other agent-instruction files (`CLAUDE.md`,
`.cursorrules`, etc.). Those stay under their owners' control.

### 8. Report

One short summary: the file written, whether this was create or update, whether
`AGENTS.md` was created or changed, and any assumptions the user should correct.

---

## Quality bar

- Concrete over corporate; every goal checkable against the repo.
- Non-goals name real temptations, not strawmen.
- No invented facts, metrics, or roadmap.
- Plain language, present tense, no marketing tone.
- The doc stays short: it is a baseline agents read quickly, not a charter.

## Failure handling

- Purpose undetectable → stop and ask; do not fabricate one.
- User rejects the draft → revise and re-present.
- Update mode reveals contradictions with reality → surface them and let the user
  decide what the project *should* be, rather than silently "fixing" intent.
- Cannot write `AGENTS.md` safely → still write `_ai/goals.md` and report the
  link that must be added.

## Files

- `assets/goals.template.md` — the section skeleton to copy.
