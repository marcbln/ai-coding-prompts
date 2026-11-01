---
name: improve-ruleman
description: Turn durable corrections from the current conversation into rules in the canonical ruleman corpus, then refresh the bound project's conventions. Use when the user says "improve ruleman", "capture these corrections", "add that as a rule", "why do I keep correcting you", or when the agent notices a reusable correction at the end of a task.
---

# Improve Ruleman

Convert corrections the user made during this conversation into durable rules in
the canonical corpus at `~/devel/ruleman`, then refresh the consuming repository
if it is bound to ruleman.

## Hard rules

- **Durable only.** A one-off fix stays a one-off. Do not promote task-specific
  instructions, retries, or facts about a single file.
- **Amend before adding.** Prefer an existing rule; add a rule to an existing
  ruleset before creating a ruleset; create a ruleset only with explicit approval.
- **No contradicting rules.** Two active rules at the same scope must not
  disagree. Surface the conflict and ask.
- **Never touch atlas copies.** Only `~/devel/ruleman/rulesets/` and
  `~/devel/ruleman/catalog/technologies.json` are canonical.
- **No auto-commit.** Commit only when the user asks in this conversation.
- **Inspect with the CLI.** Use `ruleman search`, `audit`, `show`, and `topics`;
  do not grep the JSON for answers the CLI already gives.

## Workflow

### 1. Resolve inputs

- Corpus: `$RULEMAN_RULES_DIR` when set, otherwise `~/devel/ruleman`.
- Invocation: `ruleman` from `PATH`; inside the ruleman repo use `uv run ruleman`.
- Consumer binding: `.ctx/ruleman.yaml` in the current repository, if present.
- Corrections: scan this conversation; merge any list the user supplies.

### 2. Collect corrections

Look for explicit redirections: "no", "not like that", "don't do X", "always",
"never", "we use X not Y", "from now on". Record each as
`{correction, trigger, evidence}` where evidence is the user's own wording.
Use the full heuristics in [references/proposal-format.md](references/proposal-format.md).

### 3. Filter to durable rules

Ask of each candidate:

1. Would this apply to another project or task?
2. Is it a convention (a repeatable decision) rather than a one-off remedy?
3. Is it still true after this task ends?

Three yeses keep it. Otherwise drop it and note the reason for the ledger.

### 4. Inspect the corpus

```bash
ruleman audit                         # dead rulesets, orphan topics
ruleman search "<keywords>" --json    # existing coverage
ruleman search "<keywords>" --tech <tech> --json  # reachable coverage
ruleman show <ruleset> --json         # assignments, includes, rules
ruleman topics                        # topic names and descriptions
```

Use the result to decide amend vs. add and to avoid duplicating a topic under a
second name. When inside a bound repository, `ruleman explain <topic>` shows the
current winner.

### 5. Classify each candidate

- **Amend** an existing rule's body.
- **Add** a rule to an existing ruleset and reuse or add its topic.
- **Project-scoped rule** when the correction only applies to one repository.
- **New ruleset** only with explicit approval, and never as a `base` assignment.

Apply the placement, precedence, and body rules in
[references/corpus-map.md](references/corpus-map.md).

### 6. Confirm before writing

Present one table, then wait for approval:

| # | Correction (user wording) | Target | Action | Precedence | Notes |
|---|---|---|---|---|---|

For each item the user may accept, skip, or amend the proposal. Ask once per
conflict, not once per rule.

### 7. Apply

- Add or amend the rule in the target `rulesets/<id>.json`.
- Add the topic to that ruleset's `topics` array when it is new.
- Keep rule ids globally unique (`<ruleset>:<topic-slug>`) and the body in the
  corpus voice: one dense imperative paragraph, concrete tools and paths.
- Add a `url`/`document` reference only when a canonical source exists.

### 8. Verify

```bash
ruleman validate
ruleman audit --json
uv run pytest -q
uv run ruff check .
uv run mypy src
```

- Update `CHANGELOG.md` under `## [Unreleased]`.
- Regenerate `_ai/conventions.md` with `ruleman export` when the corpus is the
  ruleman repository's own.
- Add or update a guard test only for a hard invariant (canonical path or flag,
  required library, banned alternative). Do not test prose.
- If the CLI surface changed, update `docs/cheatsheet-cli.md`.

### 9. Refresh the consumer

If the current repository has `.ctx/ruleman.yaml`, run `ruleman export` there
(or `uv run ruleman export` when ruleman is a project dependency), then show the
diff. Do not run `ruleman init`; it re-detects technologies and overwrites the
binding.

### 10. Record and report

- Append one row per proposal to
  `~/devel/ruleman/_ai/rule_proposals/ledger.md` using the format in
  [references/proposal-format.md](references/proposal-format.md).
- Show the corpus diff, the affected rule ids, and the gate results.
- Commit only when the user asks.

## End-of-task offer

When at least one durable correction was detected, close the task with one line:

> N correction(s) look rule-worthy — run `improve-ruleman` to fold them into the corpus?

Never run the skill automatically and never repeat the offer in the same session.

## References

- [references/corpus-map.md](references/corpus-map.md) — files, schema, scope,
  precedence, placement, CLI recipes.
- [references/proposal-format.md](references/proposal-format.md) — extraction
  heuristics, proposal table, apply checklist, guard-test rules, ledger format.
