---
name: git-commit-summary
description: Analyze unstaged/staged changes and generate concise commit messages summarizing what changed. Use when the user asks you to "summarize changes", "generate a commit message", "what did I change", "write a commit message for me", or any request to describe or summarize recent git changes into a commit message.
---

# Git Commit Summary

Generate concise, descriptive commit messages from recent git changes.

## Process

1. **Inspect changes** with `git status` and `git --no-pager diff --staged` (staged) or `git --no-pager diff` (unstaged). Prefer staged changes if present, otherwise use unstaged.
2. **Analyze** what files changed and why — group related changes into logical concerns.
3. **Generate** a commit message with:
   - A short subject line (under 72 chars, imperative mood, no trailing period)
   - A blank line followed by a bullet-list body summarizing each logical change

## Rules

- **Scope detection**: Look at file paths to determine scope (e.g., `src/api/` → scope: `api`). Include scope in parentheses when clear.
- **Format**: `type(scope): description` or just `type: description` if scope is unclear.
- **Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `chore`, `perf`, `revert`
- **Body**: One bullet per logical change group. Each bullet starts with a verb in past tense (Added, Fixed, Refactored, etc.).
- **No emojis**: Unlike the git-commit skill, this generates conventional commit format.
- **Present the message** to the user rather than committing automatically.

## Examples

**Input**: `git diff --staged` shows `src/parser.rs` changed to add null checking.

**Output**:
```
fix(parser): handle null input gracefully

- Added early return when input is null
- Prevented panic on empty edge case
```

**Input**: `git diff` shows new API endpoint and updated tests.

**Output**:
```
feat(api): add user registration endpoint

- Added POST /api/v1/users endpoint
- Created registration request/response types
- Added validation for email and password fields
- Wrote unit tests for registration flow
```
