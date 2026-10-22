---
filename: "_ai/backlog/reports/261021_1200__IMPLEMENTATION_REPORT__brainstorming-handoff-optional.md"
title: "Report: Make the design handoff optional after brainstorming"
createdAt: 2026-10-22 15:08
updatedAt: 2026-10-22 15:08
planFile: "_ai/backlog/archive/261021_1200__IMPLEMENTATION_PLAN__brainstorming-handoff-optional.md"
specFile: ""
project: "ai-coding-prompts + ai-prompt-manager"
status: completed
filesCreated: 1
filesModified: 4
filesDeleted: 0
tags: [skills, brainstorming, prompts, workflow, handoff, adr]
documentType: IMPLEMENTATION_REPORT
---

## Summary

The design handoff is now conditional. `brainstorming` promotes durable decisions
to ADRs, asks one closing question, and writes a handoff only when the design will
be consumed outside the conversation. The plan and spec prompts accept the
conversation as an input source, inherit constraining ADRs, guard against missing
design input, and preserve decisions and rejected alternatives. The skill no
longer tells the agent to commit.

## Files Changed

### ai-coding-prompts

- `global-skills/brainstorming/SKILL.md` — modified. The skill now ends at a design
  record, explains the ADR/plan/handoff split, asks whether the next artifact is
  produced in the same conversation or handed off, writes a handoff only on the
  handoff branch, and says not to commit unless asked.
- `_ai/backlog/archive/261021_1200__IMPLEMENTATION_PLAN__brainstorming-handoff-optional.md`
  — moved from `active/` and completed. Status is `completed`; `completedAt` and
  `updatedAt` are set; `filename` points to the archive path.
- `_ai/backlog/reports/261021_1200__IMPLEMENTATION_REPORT__brainstorming-handoff-optional.md`
  — created. This report.

### ai-prompt-manager

- `snippets/project-specific/_default/create-implementation-plan.md` — modified.
  Added the same-conversation input source, a missing-input guard, ADR inheritance,
  `sourceAdrs` in the frontmatter example, a no-handoff paragraph, and the
  `Design Decisions & Rejected Alternatives` plan section. Removed the old
  "request text" fallback wording that treated the conversation as a last resort.
- `snippets/project-specific/_default/create-spec.md` — modified. Added the
  same-conversation input source, a missing-input guard, ADR inheritance, a
  design-source quality gate, and an updated description that mentions design
  discussions as well as handoffs.

## Key Changes

- The handoff decision is now explicit: same conversation means no handoff file;
  handoff means the existing six-section document is written.
- ADRs remain unconditional whenever a decision constrains work beyond the current
  feature. The skill now says where non-durable decisions live (the plan's design
  section, or the handoff when one is written).
- The plan prompt resolves input in four steps: spec, handoff, conversation,
  request. It stops rather than inventing input when none is available.
- The plan prompt reads `_ai/technical_decisions/*.md` and inherits constraining
  decisions. `sourceAdrs` records what was inherited.
- Plans now carry a compact `Design Decisions & Rejected Alternatives` section,
  with durable decisions linked to their ADRs instead of duplicated.
- The spec prompt's quality gate item 8 is now "Fidelity to the design source" and
  accepts a design conversation when no handoff exists.
- Both prompt frontmatter files have `updatedAt: 2026-10-22`.

## Deviations from Plan

- The plan's Phase 5 said "Do not commit." The changes were committed because the
  invoked `implement-plan` workflow requires it and the user explicitly asked for a
  commit and push. The plan was archived before the commit so the report and commit
  reference its final location.
- Literal new OpenCode sessions were not available for the dry run. A nested
  `opencode run` was attempted but produced no model response and timed out after
  90 seconds. The five checks were therefore run with fresh isolated general
  subagents that read the updated skill and prompt files from disk and executed the
  workflows in `/tmp/opencode/skill-dryrun`. This is a behavioral simulation rather
  than a separate OpenCode process, but each expected artifact and message was
  observed.
- The `finish-plan` script does not update the plan's `filename` frontmatter or
  `updatedAt`. `updatedAt` was set before archiving; `filename` was corrected to the
  archive path afterwards.
- Check 3 produced a durable-decision row that both links the ADR and restates the
  decision in one line. This is acceptable for readability, but if stricter
  separation is desired the prompt's "instead of restating it" wording can be
  tightened later.
- No README, `CHANGELOG.md`, `.gitignore`, or version changes were needed.

## Technical Decisions

- **Conditional handoff, unconditional ADRs.** ADRs carry decisions that constrain
  future work; the handoff is only a transfer artifact.
- **One closing question.** The skill cannot know where the next artifact will be
  produced, so it asks once rather than guessing.
- **Conversation as a first-class source.** The plan and spec prompts read the
  thread directly when no file exists, avoiding a redundant handoff.
- **Additive `sourceAdrs`.** The field is optional and does not invalidate older
  plans that lack it.
- **Design-source quality gate.** The spec gate checks fidelity to whatever design
  source was used, not specifically a handoff.
- **No process ADR.** The user declined a separate ADR for this workflow change;
  the skill text, plan, and this report are the record.

## Testing Notes

### Static validation

- `git diff --check` is clean in both repositories.
- The old skill wording is gone: no "This skill ends at a design handoff",
  "Commit the document to git", or "Do not branch on the".
- The new skill wording is present: the closing question, "Same conversation",
  "handoff branch only", and "Do not commit unless".
- Both prompts contain "Same conversation", "Missing-input guard", `sourceAdrs`,
  "Design Decisions & Rejected Alternatives", and "Fidelity to the design source".
- `pm render create-implementation-plan -p sw6.7-plugin` succeeded.
- `pm render create-spec -p sw6.7-plugin` succeeded.
- The rendered plan prompt contains `sourceAdrs`, "Design Decisions", "Same
  conversation", and "Missing-input guard". The rendered spec prompt contains
  "Same conversation" and "Fidelity to the design source".

### Behavioral dry run

Scratch root: `/tmp/opencode/skill-dryrun`.

1. **Same-conversation branch — PASS.** The run created
   `same-conversation/_ai/technical_decisions/261022_1459__ADR__console-command-ascommand-attribute.md`,
   wrote no handoff, and closed with: "No handoff written — this design lives only
   in this conversation. If you switch sessions, ask for a handoff explicitly." It
   recommended `create-implementation-plan` and did not commit.
2. **Handoff branch — PASS.** The run created
   `handoff/_ai/backlog/active/261022_1500__DESIGN_HANDOFF__goodbye-console-command.md`
   with the documented frontmatter keys and all six body sections, plus an ADR. No
   plan was started.
3. **Same-session plan — PASS.** The run created
   `same-conversation/_ai/backlog/active/261022_1504__IMPLEMENTATION_PLAN__hello-console-command.md`
   with `sourceSpec: ""`, `sourceHandoff: ""`, and `sourceAdrs` pointing at the ADR.
   Its `Design Decisions & Rejected Alternatives` section includes the rejected
   legacy `Command` alternative and links the ADR. No handoff was fabricated.
4. **Missing-input guard — PASS.** With only "create the plan" and no spec,
   handoff, or design discussion, the run created no files and replied: "I can't
   create the plan from 'create the plan' alone... Please provide the design input."
5. **Same-session spec — PASS.** The run created
   `spec/_ai/backlog/active/261022_1503__FEATURE_SPEC__hello-console-command.md`.
   Section 5.3 records the rejected legacy `Command` alternative, and quality-gate
   item 8 reads "Fidelity to the design source" with the "design conversation when
   no handoff exists" clause. No handoff was required.

## Usage Examples

The new closing question in `brainstorming`:

> Will the spec/plan be created in this conversation, or are you handing the design off?

The same-conversation response:

> No handoff written — this design lives only in this conversation. If you switch
> sessions, ask for a handoff explicitly.

The new plan frontmatter field:

```yaml
sourceAdrs: []
```

The new plan section instruction:

```markdown
- The next section is **Design Decisions & Rejected Alternatives**. Keep it
  compact — a table or bullets, at most about ten entries. Include only decisions
  that constrain the implementation (with a one-line rationale) and alternatives
  that were seriously considered (with why they were dropped). Link a durable
  decision to its ADR (`adrId`) instead of restating it. Do not paste the handoff
  or the conversation. Source it from the handoff when present, otherwise from the
  conversation and the ADRs.
```

The revised spec quality-gate item:

> 8. **Fidelity to the design source.** Every decision in the handoff (or in the
>    design conversation when no handoff exists) appears in **5.3**, and every
>    rejected alternative is recorded there.

## Documentation Updates

- `create-spec`'s frontmatter description now covers design discussions as well as
  handoffs and raw requests.
- The skill and prompt files are the documentation for this workflow; no README or
  `CHANGELOG.md` update applies.

## Next Steps

- Start a new OpenCode session so the updated `brainstorming` skill is loaded from
  disk (skills are read at startup).
- Optionally apply the same input-resolution and missing-input guard to
  `save-plan` and `piv-plan-implementation`, which are separate generators and were
  out of scope here.
- After a few real plans, review whether durable rows should link ADRs only, rather
  than linking and restating the decision in one line.
