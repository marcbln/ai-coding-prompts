---
filename: "_ai/backlog/archive/261021_1200__IMPLEMENTATION_PLAN__brainstorming-handoff-optional.md"
title: "Make the design handoff optional after brainstorming"
createdAt: 2026-10-21 12:00
updatedAt: 2026-10-22 15:06
status: completed
completedAt: 2026-10-22 15:07
priority: medium
tags: [skills, brainstorming, prompts, workflow, handoff, adr]
estimatedComplexity: moderate
documentRevision: 1
sourceSpec: ""
sourceHandoff: ""
sourceAdrs: []
documentType: IMPLEMENTATION_PLAN
---

# Make the design handoff optional after brainstorming

## 1. Problem

`brainstorming` always writes a `DESIGN_HANDOFF` file, even when the plan is created
immediately afterwards in the same conversation. The handoff is then not read by the
user, duplicates decisions that are already in the thread, and drifts from the plan
(e.g. the 2FA card handoff listed four snippet keys while the plan added several
more). At the same time, the plan does not preserve the one thing that is genuinely
useful to later agents: the rejected alternatives. The result is one redundant
document and one missing section.

## 2. Executive Summary

Make the handoff conditional. `brainstorming` still promotes durable decisions to
ADRs, then asks one question: will the spec/plan be produced in this conversation,
or is the design being handed off?

- **Same conversation:** write no handoff. The plan/spec prompt reads the
  conversation directly, inherits constraining ADRs, and records a compact
  `Design Decisions & Rejected Alternatives` section in the plan.
- **Handoff:** write the handoff exactly as today.

The plan prompt and the spec prompt learn the new "same conversation" input source,
a missing-input guard, and ADR inheritance. The spec's quality gate stops requiring
a handoff. `sourceAdrs: []` is added to the plan frontmatter. The skill no longer
tells the agent to commit.

## 3. Design Decisions & Rejected Alternatives

Decisions carried from the validated design conversation (2026-10-21):

| # | Decision | Rationale |
|---|---|---|
| D1 | ADRs are always written when a durable decision exists; the handoff is conditional. | ADRs constrain future work; the handoff only matters as a transfer artifact. |
| D2 | Ask exactly one question at the end of brainstorming: same conversation or handoff. | The skill cannot know where the next artifact will be produced, and guessing wrong either creates a redundant file or loses the design. |
| D3 | Same-conversation plans read the conversation and constraining ADRs. | The thread already contains the validated decisions; asking the user to repeat them is waste. |
| D4 | The plan gets a `Design Decisions & Rejected Alternatives` section. | The plan is the artifact that survives into implementation; rejections must live there, not only in the chat. |
| D5 | Durable rows link the ADR instead of restating it. | Prevents the ADR/plan drift seen in the 2FA card documents. |
| D6 | Add `sourceAdrs: []` to the plan frontmatter. | Records which ADRs the plan inherited. |
| D7 | `create-spec` gets the same input-resolution change and a "design source" quality gate. | It consumes handoffs too; otherwise same-conversation specs fail the gate. |
| D8 | Remove the unconditional `Commit the document to git` line. | The agent must not commit unless the user asks. |

Rejected alternatives:

- **Slim mandatory handoff** (only rejections, open questions, scope): still an
  unread document and still duplicated by the plan.
- **ADRs only, no handoff at all**: page-level rejected alternatives have no home,
  and `create-spec` in a fresh session loses its input.
- **Skill-only change**: without the prompt changes, the plan would lose the
  rejections and could not distinguish "no input" from "plan from a vague request".
- **Process ADR for this workflow change**: declined by the user; the skill text and
  this plan are the record.
- **`save-plan` / `piv-plan-implementation` updates**: those are separate plan
  generators and are out of scope.

## 4. Project Environment

- **Skill repo:** `/home/marc/devel/ai-coding-prompts` (git). The canonical skill is
  `global-skills/brainstorming/SKILL.md`. `~/.opencode/skills` is a symlink to
  `global-skills`, so edit the canonical path only.
- **Prompt repo:** `/home/marc/devel/ai-prompt-manager` (git). Snippets are Markdown
  with YAML frontmatter, rendered with Jinja2. The two files are
  `snippets/project-specific/_default/create-implementation-plan.md` and
  `snippets/project-specific/_default/create-spec.md`.
- **No application code, no database, no build artifacts.** The "source" is Markdown
  prose and prompt templates.
- **Prompt rendering:** `/home/marc/devel/ai-prompt-manager/.venv/bin/pm render <name>
  -p sw6.7-plugin -o <dir>` (or the user's `pm` wrapper). Rendering is the closest
  thing to a compile check; a Jinja error means the prompt is broken.
- **Skill reload:** OpenCode loads skills at startup. A new session (or restart) is
  required before a dry run of the updated skill.
- **Git:** work on the current branch. Do not create branches, open PRs, or commit
  unless the user asks.
- **No test suite covers Markdown skills or prompt wording.** Validation is
  `git diff --check`, prompt rendering, and the manual dry run in Phase 4.

## 5. Source & Spec Alignment

**Sources used:** the validated design conversation of 2026-10-21 and the current
contents of the three files listed above. There is no `*__FEATURE_SPEC__*.md` and no
`*__DESIGN_HANDOFF__*.md` for this change; the plan was written from the
same-conversation design discussion, which is the behavior this change introduces.
Therefore `sourceSpec` and `sourceHandoff` are empty and `sourceAdrs` is `[]`.

The plan below is self-contained: each phase names the file and includes the exact
replacement text.

## 6. Phases

### Phase 1 — Brainstorming skill: conditional handoff

**Goal:** make ADRs unconditional, ask the same-conversation/handoff question, and
remove the automatic commit instruction.

**File:** `[MODIFY] /home/marc/devel/ai-coding-prompts/global-skills/brainstorming/SKILL.md`

**Edit 1 — Overview (currently line 14).** Replace the single paragraph with:

````markdown
**This skill ends at the design record. It does not write a plan, a spec, or code.**
It promotes durable decisions to ADRs. It writes a design handoff only when the
next artifact will be produced outside this conversation; in the same conversation,
the conversation is the source and the plan/spec carries the decisions forward.
````

**Edit 2 — "Promote durable decisions" paragraph (currently lines 41-47).** Replace
the two paragraphs with:

````markdown
A decision becomes an ADR when it **constrains future work beyond this feature** — a
chosen pattern, a dependency rule, a boundary, a convention future changes must
respect. Everything else stays in the conversation; when a plan is written, the
plan's `Design Decisions & Rejected Alternatives` section records it. It goes into
a handoff only when one is written.

For each such decision write `_ai/technical_decisions/{YYMMDD_HHmm}__ADR__{topic}.md`.
Do not promote decisions that only matter here; they belong in the plan's design
record (or the handoff, when one is written), and duplicating them in both the ADR
and the plan guarantees they drift.
````

**Edit 3 — replace the old steps 2 and 3 (currently lines 49-95)** with the
following four steps. Keep the YAML block and the body-section list verbatim inside
step 3.

````markdown
### 2. Ask where the next artifact will be produced

Ask exactly one question before writing anything:

> Will the spec/plan be created in this conversation, or are you handing the design off?

- **Same conversation** — do not write a handoff. The conversation is the source;
  the plan/spec prompt reads it directly. Tell the user in one line: "No handoff
  written — this design lives only in this conversation. If you switch sessions,
  ask for a handoff explicitly."
- **Handoff** — continue with step 3.

### 3. Write the design handoff (handoff branch only)

Write the conversation's durable output to
`_ai/backlog/active/{YYMMDD_HHmm}__DESIGN_HANDOFF__{kebab-case-topic}.md`:

```yaml
---
filename: "_ai/backlog/active/{YYMMDD_HHmm}__DESIGN_HANDOFF__{kebab-case-topic}.md"
title: "Design Handoff: {topic}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
status: completed
completedAt: 2026-10-22 15:07
tags: [tag1, tag2]
documentType: DESIGN_HANDOFF
---
```

Body sections, in this order:

- **Context** — what was being designed and where the discussion started.
- **Decisions** — one entry per decision: the decision, the rationale, and what it
  rules out.
- **Rejected Alternatives** — what was considered and dropped, and why. This is the
  most valuable section in the file: without it the same options get re-proposed
  later.
- **Constraints Discovered** — facts about the codebase or project surfaced during
  the discussion that any implementation must respect.
- **Open Questions** — unresolved items, each with a named owner.
- **Scope Boundary** — explicitly in, explicitly out.

Keep it a record of decisions, not a narrative of the conversation and not a
specification. It describes intent and constraints; it does not enumerate
requirements.

### 4. Recommend the next artifact, then stop

Close with one line naming what should come next and why. Do not start it:

- New capability, or anything still uncertain about behavior → run the
  `create-spec` prompt
- Well-understood change, or mostly mechanical work → run the
  `create-implementation-plan` prompt
- Large effort that needs slicing first → use the `create-epic` skill
- Genuinely nothing to build yet → stop

Do not commit unless the user asks.
````

**Verification (Phase 1):**

```bash
cd /home/marc/devel/ai-coding-prompts
git diff --check

# The old unconditional wording must be gone.
rg -n "This skill ends at a design handoff|Commit the document to git|Do not branch on the" \
  global-skills/brainstorming/SKILL.md || true

# The new branch must be present.
rg -n "Ask where the next artifact|Same conversation|handoff branch only|Do not commit unless" \
  global-skills/brainstorming/SKILL.md
```

Manual read: confirm the skill still says it does not write a plan/spec/code, and
that step 4 does not start the next artifact.

---

### Phase 2 — Plan prompt: conversation source, ADRs, new plan section

**Goal:** make `create-implementation-plan` work without a handoff, inherit ADRs,
refuse to invent missing input, and require the decisions/rejections section.

**File:** `[MODIFY] /home/marc/devel/ai-prompt-manager/snippets/project-specific/_default/create-implementation-plan.md`

**Edit 1 — frontmatter `updatedAt` (line 6).** Set it to the implementation date.

**Edit 2 — `sourceAdrs` in the frontmatter example (after line 65).** Add:

```yaml
sourceAdrs: []
```

**Edit 3 — the explanation below the frontmatter (lines 70-72).** Replace with:

````markdown
`sourceSpec` and `sourceHandoff` hold the paths of the `*__FEATURE_SPEC__*.md` and
`*__DESIGN_HANDOFF__*.md` files this plan was derived from, or empty strings when
the plan was written without them. `sourceAdrs` lists the ADR files or ids this
plan inherited; use `[]` when none apply.
````

**Edit 4 — input resolution (lines 15-26).** Replace with:

````markdown
1. **Feature Spec** — if a `*__FEATURE_SPEC__*.md` is named in the request, or the
   most recent one in `_ai/backlog/active/` clearly covers this work, read it. This
   is the primary input when present.
2. **Design Handoff** — likewise for a `*__DESIGN_HANDOFF__*.md`. Supplies the
   decisions, rejected alternatives, and constraints discovered.
3. **Same conversation** — if neither file exists and the design discussion is in
   this conversation, use it as the design source. Do not ask the user to repeat
   decisions that are already in the thread.
4. **Request text** — if the design is not in this conversation either, plan from
   the request and the codebase.

**Missing-input guard.** If there is no spec, no handoff, no design discussion in
this conversation, and the request is only "create the plan", stop and ask for the
design input. Do not invent decisions or rejected alternatives.

**ADRs.** Read `_ai/technical_decisions/*.md` and inherit every decision that
constrains this work (match by topic, tags, or an explicit mention). If an ADR
conflicts with the request or the spec, list it under Open Questions; do not
silently override it.

State in one line which sources you used. When a spec exists, its **Chosen
Approach & Constraints** section is binding on this plan: the phases must implement
those constraints rather than silently choosing something else. If a constraint is
unworkable, say so explicitly instead of quietly overriding it.
````

**Edit 5 — no-handoff paragraph (after line 45).** Add:

````markdown
**When no handoff is available**, leave `sourceHandoff` empty and take the
decisions and rejected alternatives from the conversation and the ADRs. Do not
fabricate a handoff file.
````

**Edit 6 — new plan section (currently line 78).** Replace the line

```markdown
- The third section contains project environment details:
```

with:

````markdown
- The next section is **Design Decisions & Rejected Alternatives**. Keep it
  compact — a table or bullets, at most about ten entries. Include only decisions
  that constrain the implementation (with a one-line rationale) and alternatives
  that were seriously considered (with why they were dropped). Link a durable
  decision to its ADR (`adrId`) instead of restating it. Do not paste the handoff
  or the conversation. Source it from the handoff when present, otherwise from the
  conversation and the ADRs.

- The next section contains project environment details:
````

**Verification (Phase 2):**

```bash
cd /home/marc/devel/ai-prompt-manager
git diff --check

rg -n "Same conversation|Missing-input guard|sourceAdrs|Design Decisions & Rejected Alternatives|When no handoff" \
  snippets/project-specific/_default/create-implementation-plan.md

# Jinja render check (must succeed, no undefined-variable errors)
mkdir -p /tmp/opencode/rendered-prompts
.venv/bin/pm render create-implementation-plan -p sw6.7-plugin \
  -o /tmp/opencode/rendered-prompts --force
rg -n "sourceAdrs|Design Decisions|Same conversation|Missing-input guard" \
  /tmp/opencode/rendered-prompts
```

---

### Phase 3 — Spec prompt: conversation source, ADRs, design-source gate

**Goal:** keep `create-spec` working when the design lives only in the conversation,
and stop its quality gate from requiring a handoff.

**File:** `[MODIFY] /home/marc/devel/ai-prompt-manager/snippets/project-specific/_default/create-spec.md`

**Edit 1 — frontmatter description (line 3) and `updatedAt` (line 6).** Replace the
description with:

```yaml
description: "Turns a brainstorming design discussion or handoff (or a raw feature request) into a behavior-first Feature Spec: what the system must do, how it is observed, and how it is proven done. Contains no implementation design."
```

Set `updatedAt` to the implementation date.

**Edit 2 — input resolution (lines 40-55).** Replace with:

````markdown
1. **Design handoff** — if the conversation or request names a
   `*__DESIGN_HANDOFF__*.md` file (typically under `_ai/backlog/active/`), read it.
   Treat its **Decisions**, **Rejected Alternatives**, **Constraints Discovered**,
   and **Open Questions** sections as authoritative input. Do not re-litigate a
   decision that is already recorded there.
2. **Same conversation** — if no handoff exists and the design discussion is in
   this conversation, use it. Do not re-litigate a decision that was already
   validated in the thread.
3. **Explicit request** — if the user described the feature in this conversation
   but there was no design discussion, use that description.
4. **Codebase** — if none of the above is sufficient, inspect the project
   (existing behavior, adjacent specs, conventions, tests) before writing.

**Missing-input guard.** If there is no handoff, no design discussion in this
conversation, and no explicit request describing the feature, stop and ask for the
input. Do not invent behavior.

**ADRs.** Read `_ai/technical_decisions/*.md` and treat decisions that constrain
the feature's behavior as binding constraints. State in one line which ADRs you
used. If an ADR conflicts with the request, raise it in Open Questions.

State in one line which sources you used. If you had to guess at something material,
it belongs in Open Questions, not silently in the body.

If a design handoff exists or the design is in this conversation, also collect the
**Rejected Alternatives** — those are the highest-value content in this document
and must survive into *Chosen Approach & Constraints*.
````

**Edit 3 — quality gate item 8 (lines 317-318).** Replace with:

````markdown
8. **Fidelity to the design source.** Every decision in the handoff (or in the
   design conversation when no handoff exists) appears in **5.3**, and every
   rejected alternative is recorded there.
````

**Verification (Phase 3):**

```bash
cd /home/marc/devel/ai-prompt-manager
git diff --check

rg -n "Same conversation|Missing-input guard|Fidelity to the design source|design conversation when no handoff" \
  snippets/project-specific/_default/create-spec.md

.venv/bin/pm render create-spec -p sw6.7-plugin \
  -o /tmp/opencode/rendered-prompts --force
rg -n "Same conversation|Fidelity to the design source" \
  /tmp/opencode/rendered-prompts
```

---

### Phase 4 — Behavioral dry run

**Goal:** prove both branches and the missing-input guard actually work, not just
that the prose reads well.

**No files change in this phase.** Run these checks in a scratch directory, not in
the real repos:

```bash
rm -rf /tmp/opencode/skill-dryrun
mkdir -p /tmp/opencode/skill-dryrun/_ai/technical_decisions \
         /tmp/opencode/skill-dryrun/_ai/backlog/active
```

**Check 1 — same-conversation branch.**

1. Start a new OpenCode session with the updated skill loaded.
2. Brainstorm a trivial feature in `/tmp/opencode/skill-dryrun` and validate the
   design in sections.
3. Answer **same conversation** to the closing question.

Expected:
- an ADR exists in `_ai/technical_decisions/` if a durable decision was made;
- no `*__DESIGN_HANDOFF__*.md` exists;
- the closing line says the design lives only in this conversation and names the
  next prompt;
- no commit was made.

**Check 2 — handoff branch.**

Repeat with a second trivial feature and answer **handoff**.

Expected: the handoff file exists with the documented frontmatter and sections; no
plan was started.

**Check 3 — same-session plan.**

In the Check 1 session, run the updated `create-implementation-plan` prompt.

Expected:
- the plan states its sources as the conversation and any ADR;
- `sourceHandoff: ""` and `sourceAdrs` populated (or `[]`);
- a `Design Decisions & Rejected Alternatives` section exists, includes the
  rejected option from the conversation, and links the ADR instead of restating it;
- no handoff file was fabricated.

**Check 4 — missing-input guard.**

In a fresh session with no spec, no handoff, and no design discussion, run the plan
prompt with only "create the plan".

Expected: the agent asks for the design input and does not write a plan.

**Check 5 — same-session spec.**

In a third scratch session, run the design conversation and then `create-spec`.

Expected: `5.3 Chosen Approach & Constraints` contains the rejected alternatives;
quality gate item 8 reads "Fidelity to the design source"; no handoff is required.

Record each result in the implementation report.

---

### Phase 5 — Documentation, housekeeping, report

**Goal:** leave both repos clean and write the report.

**Files:**

- `[MODIFY] _ai/backlog/active/261021_1200__IMPLEMENTATION_PLAN__brainstorming-handoff-optional.md`
  — set `status: completed` and `updatedAt` to the implementation time.
- `[NEW FILE] _ai/backlog/reports/261021_1200__IMPLEMENTATION_REPORT__brainstorming-handoff-optional.md`

**Housekeeping:**

- `.gitignore`: no change; no new file types or build artifacts.
- `README.md`: no change in either repo; the skill and prompt files are the
  documentation, and the snippet descriptions are unchanged except `create-spec`.
- `CHANGELOG.md`: neither repo has one; no change.
- `composer.json` / package versions: not applicable to Markdown-only changes.
- Do not commit. Leave both working trees with the changes for the user to review.

**Report frontmatter:**

```yaml
---
filename: "_ai/backlog/reports/261021_1200__IMPLEMENTATION_REPORT__brainstorming-handoff-optional.md"
title: "Report: Make the design handoff optional after brainstorming"
createdAt: <implementation time>
updatedAt: <implementation time>
planFile: "_ai/backlog/active/261021_1200__IMPLEMENTATION_PLAN__brainstorming-handoff-optional.md"
specFile: ""
project: "ai-coding-prompts + ai-prompt-manager"
status: completed
completedAt: 2026-10-22 15:07
filesCreated: 1
filesModified: 4
filesDeleted: 0
tags: [skills, brainstorming, prompts, workflow, handoff, adr]
documentType: IMPLEMENTATION_REPORT
---
```

Report sections: Summary, Files Changed (grouped by repo), Key Changes, Deviations
from Plan, Technical Decisions, Testing Notes (the five dry-run checks and the two
`pm render` results), Usage Examples (the new closing question and the plan
section), Documentation Updates, Next Steps.

**Verification (Phase 5):**

```bash
cd /home/marc/devel/ai-coding-prompts && git status --short && git diff --check
cd /home/marc/devel/ai-prompt-manager && git status --short && git diff --check
```

Expected: the three source files plus this plan and the report are modified/added;
no generated artifacts; no commits.

## 7. Traceability

No spec or handoff exists; the mapping is to the design decisions in §3.

| Phase | Decisions |
|---|---|
| 1 | D1, D2, D8 |
| 2 | D3, D4, D5, D6 |
| 3 | D7 |
| 4 | D2, D3, D4, D7 (behavioral proof) |
| 5 | D1–D8 (record and close) |

## 8. Risks and Rollback

| Risk | Mitigation |
|---|---|
| The skill still writes a handoff in the same-conversation branch, or starts the plan. | Explicit "do not write a handoff" and "do not start it"; Phase 4 Check 1. |
| The plan omits rejections when there is no handoff. | Mandatory `Design Decisions & Rejected Alternatives` section; Phase 4 Check 3. |
| A fresh session with only "create the plan" invents decisions. | Missing-input guard; Phase 4 Check 4. |
| The spec quality gate still demands a handoff. | Phase 3 Edit 3; Phase 4 Check 5. |
| Added prose accidentally uses Jinja syntax (`{{`, `{%`) and breaks rendering. | Keep the new text free of Jinja delimiters; `pm render` in Phases 2 and 3. |
| Old plans lack `sourceAdrs`. | The field is additive and optional; no migration. |
| Other generators (`save-plan`, `piv-plan-implementation`) still assume handoffs. | Explicitly out of scope; note in the report for a follow-up. |
| The skill is cached from the old version at startup. | Start a new session before Phase 4. |

**Rollback:** restore the three files with `git checkout -- <path>` in each repo and
delete the report. No data, migration, or generated artifact is involved.

## 9. Definition of Done

- [ ] `brainstorming` asks the same-conversation/handoff question and does not write
      a handoff in the same-conversation branch.
- [ ] ADRs are still written whenever a durable decision exists.
- [ ] The skill no longer instructs an unconditional commit.
- [ ] `create-implementation-plan` supports the conversation source, ADRs, the
      missing-input guard, and `sourceAdrs`.
- [ ] Plans generated by the updated prompt contain `Design Decisions & Rejected
      Alternatives`, with durable rows linked to ADRs.
- [ ] `create-spec` supports the conversation source and its quality gate says
      "design source".
- [ ] Both prompts render without Jinja errors.
- [ ] The five dry-run checks pass.
- [ ] The implementation report exists; this plan is marked completed.
- [ ] No commit was made.
