---
name: handoff-writer
description: "Write a durable handoff document when design or work state must survive a session, model, or repository switch. Covers DESIGN_HANDOFF (settled design, next artifact produced elsewhere) and SESSION_HANDOFF (work in flight, resume later). Use when asked to write a handoff, hand off a design, capture decisions before switching sessions, checkpoint in-progress work, or when a discussion must be continued by someone else. Enforces the established _ai/backlog/active frontmatter, section order, evidence rules, and a validator. NOT for completed-work reports (implementation-report), single decisions (adr-writer), or plans (save-plan)."
---

# Handoff Writer

A handoff is a **decision and state record**, not a transcript and not a spec.
It exists so the next session does not re-litigate what was already settled or
re-discover what was already learned.

## When to write one — and when not to

Write a handoff when the next artifact or the next work step will be produced
**outside this conversation** (new session, different model, another repo/agent).

Do **not** write one when:

| Situation | Use instead |
|---|---|
| The plan/spec will be written in this same conversation | Nothing — the conversation is the source. Say so in one line. |
| Work is finished and needs a record | `implementation-report` |
| The output is one durable technical decision | `adr-writer` |
| You already have an approved plan | The plan itself is the handoff |
| It is a bug being characterized | `bug-report` |

If the user asks for a handoff anyway, write it — but say which of the above
normally applies.

## Choose the type

| | `DESIGN_HANDOFF` | `SESSION_HANDOFF` |
|---|---|---|
| **Use when** | Design is settled; a plan/spec/epic will be written later, elsewhere | Work is in flight or blocked; someone must resume it |
| **Owns** | Why this shape, what was rejected, what constrains the build | What is done, what is half-done, what to do next, what will bite |
| **Does not own** | Requirements, task breakdown, code detail | Design rationale already in a handoff/ADR/plan |
| **Sections** | Context, Decisions, Rejected Alternatives, Constraints Discovered, Open Questions, Scope Boundary, Next Artifact | Objective, Current State, Decisions Made, Dead Ends, Open Questions, Next Actions, Verification, Where Things Live, Handoff Notes |
| **Status values** | `draft`, `validated`, `implemented`, `superseded` | `active`, `blocked`, `done`, `abandoned` |

Both types live in the **repo that will own the next artifact** (or the repo
where the work lives). When the design spans repos, write in the primary repo
and list the others under `relatedRepos:`. Never split one handoff across repos.

## Non-negotiables

1. **Evidence before prose.** Inspect the repo before writing: read the files,
   run the read-only command, count the rows, check the ADRs and git log. Every
   constraint cites a path, command, ADR, or measurement. A claim you did not
   verify is an open question, not a constraint.
2. **Every decision carries its rationale and what it rules out.** A decision
   without "rules out" invites the same rejected option back next week.
3. **Rejected Alternatives is never empty.** It is the most valuable section:
   it is what stops the design from looping. Include why each option lost.
4. **Constraints are discovered facts, not preferences.** Include numbers,
   file paths, limits, and existing invariants. Do not restate the design here.
5. **Open Questions each name an owner** (person, role, or repo/team). A
   question without an owner is a wish.
6. **Scope Boundary is explicit In / Out.** "Everything else" is not a boundary.
7. **Reference, do not duplicate.** Link ADRs and plans by path. Never re-decide
   a settled ADR in a handoff; record the consequence instead.
8. **Intent, not requirements.** No user stories, acceptance criteria, task
   lists, or code listings. Those belong in the spec/plan the handoff feeds.
9. **No conversation narrative.** "We discussed…", "Marc asked…" belongs only
   in Context, in one short paragraph.
10. **Fresh timestamps.** Set `updatedAt` whenever the file changes.

## Workflow

### 1. Confirm the branch

Ask exactly one question if it is not obvious:

> Will the next artifact be produced in this conversation, or am I handing it off?

Same conversation → stop, no file. Handoff → continue.

### 2. Gather evidence

Run the cheapest checks that turn claims into constraints. Typical set:

```bash
# what already exists
ls _ai/backlog/active _ai/technical_decisions 2>/dev/null
# what is already decided
grep -ril "<topic>" _ai/technical_decisions _ai/backlog/active
# what the code actually does
git log --oneline -20
rg -n "<symbol|table|config key>" --glob '!node_modules'
# current state of the thing (counts, versions, reachability)
<one read-only command that proves the claim>
```

Stop gathering when each planned constraint has a citation. Do not turn the
handoff into an audit report.

### 3. Draft from the discussion, not from imagination

- One numbered entry per **settled** decision. If it was not settled, it is an
  open question.
- Keep the decision title short and declarative; put why + rules out below it.
- List alternatives actually considered, including the tempting bad one.
- Carry forward every fact that surprised you during the discussion — those are
  the constraints the implementer will otherwise rediscover the hard way.

### 4. Write the file

Copy the matching template from `assets/` and fill it. Do not invent sections;
if a section genuinely does not apply, keep the heading and write `None.`

Filename and location:

```
_ai/backlog/active/{YYMMDD_HHmm}__{DESIGN_HANDOFF|SESSION_HANDOFF}__{kebab-case-topic}.md
```

Frontmatter (required fields, in this order):

```yaml
---
filename: "_ai/backlog/active/{YYMMDD_HHmm}__{TYPE}__{kebab-topic}.md"
title: "Design Handoff: {topic}"   # or "Session Handoff: {topic}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
status: draft | validated | implemented   # type-specific, see table
tags: [tag1, tag2]
documentType: DESIGN_HANDOFF       # or SESSION_HANDOFF
---
```

Optional: `priority`, `relatedRepos: [path, ...]`, `relatedPlan`, `branch`,
`supersedes`.

### 5. Validate

```bash
python3 <skill-dir>/scripts/validate_handoff.py \
  _ai/backlog/active/<file>.md
```

`<skill-dir>` is the installed skill, typically
`~/.config/opencode/skills/handoff-writer` (the bundled script has no
dependencies).

Fix every `ERROR`. Treat `WARN` as a prompt to check, not noise. Add
`--strict` in CI or before committing.

### 6. Recommend the next artifact, then stop

One line, no implementation:

- New capability or behavior still uncertain → `spec-writer`
- Well-understood or mostly mechanical → `save-plan`
- Large, needs slicing → `create-epic`
- Work to resume → the `SESSION_HANDOFF` itself is the entry point
- Nothing to build yet → stop

Do not commit unless the user asks.

## Quality bar

A good handoff lets a competent agent who was not in the conversation start the
next artifact without asking a single clarifying question about **intent**.
Open questions are fine — silence is not.

Signs it is not ready:

- Decisions restate the feature instead of choosing a shape.
- Rejected Alternatives has one entry, or entries without reasons.
- Constraints contain adjectives ("fast", "clean") instead of facts.
- Open Questions have no owner.
- Scope Out is shorter than Scope In and says "etc.".
- It reads like a plan with the task list removed.
- It repeats an ADR's decision instead of linking it.

## Bundled files

- `assets/TEMPLATE_DESIGN_HANDOFF.md` — fill-in skeleton with inline guidance.
- `assets/TEMPLATE_SESSION_HANDOFF.md` — fill-in skeleton with inline guidance.
- `scripts/validate_handoff.py` — stdlib-only checker for frontmatter, filename,
  section set, empty sections, stale timestamps, and missing owners.
