# Proposal format

## 1. Correction extraction

Scan the conversation for these signals:

| Signal | Example |
| --- | --- |
| Explicit rejection | "no, that's wrong", "not like that" |
| Redirection | "use X instead", "we use X, not Y" |
| Permanence | "always", "never", "from now on", "don't do that again" |
| Explanation of intent | "the reason is ...", "this project requires ..." |
| Repeated correction | the user fixed the same mistake twice |

Record each candidate as:

```text
correction: <one sentence in the user's intent>
trigger:    <when it applies>
evidence:   <short quote from the user>
```

Ignore agent self-corrections the user did not confirm, and ignore facts that
only describe the current file or ticket.

## 2. Durability test

Keep a candidate only when all three answers are yes:

1. **Reusable** — it would apply to another project, file, or task.
2. **Conventional** — it is a repeatable decision, not a one-off remedy.
3. **Durable** — it will still be true after this task ends.

If it fails only because it is repository-specific, propose a project-scoped
rule instead of dropping it.

## 3. Proposal table

Present exactly one table and wait for a decision:

| # | Correction | Target | Action | Precedence | Guard test | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Use one shared Rich theme | `python`, topic `python:cli-presentation` | add rule | 70 | no | new topic |

Rules for the table:

- `Target` names the ruleset, the topic, and the existing rule id when amending.
- `Action` is one of `amend`, `add rule`, `project rule`, `new ruleset`.
- `Precedence` stays inside the host's band and is higher than a rule it refines.
- `Guard test` is `yes` only for a hard invariant (see section 5).
- `Notes` names a conflict, a missing catalog technology, or an approval need.

The user may accept, skip, or amend each row. Apply only the accepted rows.

## 4. Conflicts

Before writing, compare the candidate with the current winner:

```bash
ruleman search "<keywords>" --json
ruleman explain <topic> --json   # when a project binding exists
```

If the candidate contradicts an existing active rule at the same scope, stop and
offer three choices: amend the existing rule, add a narrower tech/project-scoped
override, or skip. Never write both.

## 5. Guard tests

Add or update a test only when the rule encodes an invariant a regression could
break:

- a canonical path, flag, or command spelling,
- a required or banned library/tool,
- an assignment or include that must exist.

Reuse the existing guard file for that area (for example
`tests/test_flag_vocabulary.py`, `tests/test_cli_cheatsheet.py`). Do not assert
prose wording; that makes every edit brittle.

## 6. Apply checklist

1. Edit `rulesets/<id>.json` (and `catalog/technologies.json` only when the user
   approved a new technology).
2. Add the topic entry when the topic is new.
3. Update `CHANGELOG.md` under `## [Unreleased]`.
4. Regenerate `_ai/conventions.md` in the ruleman repo with `ruleman export`.
5. Update `docs/cheatsheet-cli.md` only when the CLI surface changed.
6. Run `ruleman validate`, `ruleman audit --json`, `uv run pytest -q`,
   `uv run ruff check .`, and `uv run mypy src`.
7. In the consumer repository, run `ruleman export` and show the diff.
8. Commit only when the user asked.

## 7. Ledger

Path: `~/devel/ruleman/_ai/rule_proposals/ledger.md`.

| Date | Source | Correction | Target | Disposition | Reason |
| --- | --- | --- | --- | --- | --- |
| 2026-11-01 | ruleman | Prefer a shared Rich theme | `python:cli-presentation` | accepted | reusable across CLIs |
| 2026-11-01 | shopware-x | Rename this one class | — | rejected | one-off, not a convention |

- `Disposition`: `accepted`, `amended`, `rejected`, or `skipped`.
- `Source`: repository or session name the correction came from.
- Keep reasons to one short clause.
- Read the ledger before proposing: a rejected row stays rejected unless the user
  reverses the decision.
