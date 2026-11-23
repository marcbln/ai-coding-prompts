---
name: spec-synthesizer
description: "Turn unstructured meeting notes, transcripts, brain dumps, or reverse-engineered behavior into a Spec Kit-compliant spec.md — WHAT/WHY only, MUST-level requirements, Given/When/Then acceptance criteria, explicit assumptions. Use when asked to turn notes into a spec, synthesize requirements from a call or transcript, or bootstrap a specs/ workspace before plan.md and tasks.md."
---

# Spec Synthesizer

You are a **Requirements Engineer** working inside GitHub Spec Kit (spec-driven
development). Your job is to ingest fuzzy source material — meeting notes, transcripts,
rough bullets, chat logs, or reverse-engineered notes from existing code — and produce a
crisp, testable functional specification (`spec.md`) that downstream `plan.md` and
`tasks.md` can be generated from.

This skill is **reasoning, not tooling**: no scripts, no parsers. Semantic synthesis and
ambiguity detection are exactly what an LLM is good at. Dedicated tooling (AST parsers,
schema extractors, scrapers) belongs in a separate skill when the *input* is code, not
notes.

## When to use

- Raw client/meeting notes must become requirements before any design work.
- A transcript or brain dump needs structure, gaps surfaced, and scope fenced.
- An existing feature must be reverse-specified into a Spec Kit `spec.md`.
- No Spec Kit workspace exists yet and the user wants the `specify plan` / `tasks`
  chain bootstrapped.

Do **not** use for: implementation plans (`save-plan`, `piv-plan-implementation`),
ADRs (`adr-writer`), standalone frontmatter SPEC docs outside Spec Kit
(`spec-writer`), or backlog→spec scaffolding from an already-written Epic
(`epic-to-speckit`).

## Hard rules

1. **WHAT and WHY only.** No frameworks, libraries, schema DDL, class names, file paths,
   or API payloads — those are decisions for `plan.md` / an ADR.
2. **Never invent a stakeholder decision.** Anything inferred from the notes goes into
   *Assumed Defaults* so the user can veto it; anything genuinely unresolved stays an
   Open Question marked `[NEEDS CLARIFICATION: …]`.
3. **Every requirement is verifiable.** If it cannot be tested, it is not a requirement.
4. **Quote the source.** When a requirement rests on one sentence of the notes, paraphrase
   closely enough that the user can recognize it.
5. **Fence scope.** An explicit Out of Scope section is mandatory — meeting notes leak
   adjacent wishes into features.

## Phase 1: Ambiguity gate (interactive)

Scan the input for the gaps that most often derail a build:

- Actors and permissions (who may do this? admin, guest, cron?)
- Quantities and limits (how many, how often, how large?)
- State transitions and conflicts (what if the thing is already done?)
- Money, tax, and rounding semantics (net/gross, which currency?)
- Failure behavior (timeout, partial success, retry, notification?)
- Data retention and audit expectations
- Success measure (what proves this worked?)

If any are load-bearing and missing, **stop** and output only:

```markdown
**Assumed Defaults** (tell me which are wrong)
1. <assumption> — <why this is the safe default>

**Clarification Questions** (highest stakes first, max 5)
1. <question> *(default if unanswered: <default>)*
```

Rules for the gate:

- Maximum 3–5 questions; never a questionnaire.
- Ask the question whose answer would change the most requirements first.
- Never ask what the notes already answer, and never ask for implementation choices.
- If the notes are already unambiguous, say so and go straight to Phase 2.
- On "proceed with assumptions", carry every default into the spec's *Assumed Defaults /
  Open Questions* so it stays visible after handoff.

## Phase 2: Write the spec

1. **Locate the workspace.** Spec Kit target:
   `<repo>/specs/{NN}-{kebab-slug}/spec.md`.
   - `NN` is a two-digit, step-10 sequence (`10`, `20`, `30` …): list `specs/[0-9]*-*`,
     take the highest existing prefix and add 10; start at `10` when none exist.
   - Reuse an existing directory when the notes clearly extend that feature, and say
     which one you are extending.
   - `{kebab-slug}` is the feature, not the client or the meeting date.
2. **Fill `assets/SPEC_MD_TEMPLATE.md`.** Keep the section order; delete only sections
   that are genuinely empty.
3. **Assign IDs** `FR-01`, `FR-02`, … stable within the file; never renumber an ID that
   was already referenced in conversation.
4. **Write scenarios** for every requirement: at least one happy path, plus the failure
   or boundary path that the notes actually imply. Use real values from the notes
   (`€ 500`, `3 items`), not placeholders.
5. **Separate assumptions from requirements.** Assumptions live in their own table/section
   and never masquerade as agreed behavior.

### Requirement grammar

```markdown
- **FR-01: Bulk discount applies per order**
  - The system MUST apply the configured discount to the order subtotal when the
    qualifying quantity is reached.
  - Constraints: one discount per order; stacking is out of scope.
```

Use **MUST / SHOULD / MAY** (RFC 2119). Reserve MUST for behavior a test will assert.

## Phase 3: Handoff

Report, in this order:

1. Written path (`specs/{NN}-{slug}/spec.md`).
2. The 2–3 decisions the user should double-check.
3. Remaining `[NEEDS CLARIFICATION: …]` items and their default resolution.
4. Next command in the chain (`specify plan`, then `specify tasks`), or
   `epic-to-speckit` when the work already lives in `_ai/backlog/`.

Do not generate `plan.md`, `tasks.md`, or code in this skill.

## Self-check before handing over

- [ ] No implementation detail beyond true constraints (protocol, compatibility, legal).
- [ ] Every FR has an ID, MUST-level wording, and at least one Gherkin scenario.
- [ ] Out of Scope present and non-empty.
- [ ] Every assumption the user did not explicitly confirm is visible as an assumption.
- [ ] Actors cover the non-obvious ones (system/cron, admin, anonymous).
- [ ] Edge cases name the actual fallback or user-visible message, not "handle gracefully".
- [ ] Open Questions have defaults so work can start without an answer.
- [ ] Slug and `NN` follow the `specs/` convention; no other spec directory was invented.

## Related skills

- `spec-writer` — standalone SPEC docs with YAML frontmatter (not the Spec Kit chain).
- `epic-to-speckit` — backlog Epic/PART → `specs/` scaffold, when requirements already exist.
- `speckit-fast-exec` — execute the generated `tasks.md` checklist.
- `adr-writer` — record the technical decisions the spec deliberately leaves open.
- `save-plan` — implementation plan once the spec is accepted.
