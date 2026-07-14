---
name: git-commit
description: Create atomic commits with conventional commit messages
---

# Commit

Create atomic commits with conventional commit messages using only non-interactive commands.

## Process

- Inspect current changes with `git status` and `git --no-pager diff HEAD`.
- Decide whether the changes should be one commit or several logical commits.
- If multiple logical changes exist, plan and split them into separate commits.
- For each commit:
  - Stage only the relevant changes with `git add ...`.
  - Review the staged diff (e.g. `git --no-pager diff --cached`) to confirm what’s included.
  - Commit with a message (`git commit -m "…"`) following the style below.
- Return the commits to the user.

## Style

- **Atomic**: One concern per commit.
- **Split big changes**: Separate features, fixes, refactors, docs, etc. when they are independent.
- **Subject line**:
  - Format: `type(scope): description` or `type: description` if scope is unclear.
  - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `style`, `chore`, `perf`, `revert`.
  - Imperative, present tense (e.g. "Add…", "Fix…").
  - Under 72 characters.
  - No trailing period.
- Always ensure the commit message accurately reflects the diff.

## Splitting Commits

Split into multiple commits when:

- Changes touch unrelated parts of the codebase.
- Different types of work are mixed (feature, fix, refactor, docs, tests, chore).
- Different file types are mixed in a way that’s easier to review separately (e.g. code vs docs).
- The diff is very large and can be broken into smaller, easier-to-review steps.

## Examples

- `feat(auth): add user authentication system`
- `fix(render): resolve memory leak in rendering process`
- `docs(api): update API documentation with new endpoints`
- `refactor(parser): simplify error handling logic`
- `style(components): reorganize component structure`
- `chore: remove deprecated legacy code`
- `ci: resolve failing CI pipeline tests`
- `fix(a11y): improve form accessibility for screen readers`
