---
name: git-commit
description: Create git commits with conventional commit messages (split into logical commits, or one atomic commit of everything), or draft a commit message without committing. Use when work is ready to be committed, when the user asks to "commit", "summarize changes", "what did I change", or "write a commit message".
---

# Git Commit

Inspect uncommitted changes and either create conventional commits or draft message(s) only — always with non-interactive commands.

## Modes

| Mode | When to use | Behavior |
|------|-------------|----------|
| **smart** (default) | User asks to commit, no constraints given | Split into multiple logical commits when warranted |
| **single** | Workflow requires exactly one commit per ticket/branch (e.g. PIV), or user says "one commit" / "single commit" | All uncommitted changes in exactly one commit |
| **draft** | User asks to "summarize changes", "what did I change", "write a commit message" | Generate message(s) only; never stage or commit |

## Process

1. Inspect changes with `git status` and `git --no-pager diff HEAD` (`git --no-pager diff --staged` if staged changes exist and nothing else).
2. Decide the commit plan:
   - **smart**: one concern per commit. Split when changes touch unrelated parts of the codebase, mix work types (feature/fix/refactor/docs/tests/chore), mix code vs docs, or the diff is large enough to review better in steps.
   - **single**: everything in one commit, no splitting.
   - **draft**: skip all staging/committing below; just present the proposed message(s).
3. For each planned commit:
   - Stage only the relevant files with `git add ...`.
   - Review the staged diff (`git --no-pager diff --cached`) to confirm what's included.
   - Commit with `git commit -m "…"`.
4. Return the created commits (or draft messages) to the user.

## Message Format

- Subject: `type(scope): description`, or `type: description` if scope is unclear.
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `chore`, `perf`, `revert`.
- Imperative mood, under 72 characters, no trailing period, no emojis.
- Body (required in draft mode, recommended otherwise): blank line after subject, then one bullet per logical change group, each starting with a past-tense verb (Added, Fixed, Refactored…).
- The message must accurately reflect the diff.

## Examples

- `feat(auth): add user authentication system`
- `fix(parser): handle null input gracefully`

  ```
  fix(parser): handle null input gracefully

  - Added early return when input is null
  - Prevented panic on empty edge case
  ```

## Post-Commit Output (single mode)

After the commit succeeds, print two clearly labelled summaries:

### What Changed
One short paragraph (3–6 sentences) describing the feature/fix/refactor that was committed — what problem it solves and what files were the key touch points. Write for a developer skimming the git log.

### AI Layer Changes
Only include this section if any files under `_ai/` were modified or added (AGENTS.md, `_ai/backlog/`, `_ai/technical_decisions/`, `_ai/lessons_learned/`, etc.).

List each changed AI-layer file with a one-line note on what evolved and why. If nothing in `_ai/` changed, omit this section entirely.
