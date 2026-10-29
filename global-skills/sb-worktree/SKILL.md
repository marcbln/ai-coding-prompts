---
name: sb-worktree
description: Work on a second task in an isolated git worktree while the primary checkout keeps its WIP. Use when asked to fix a bug or make a change in parallel without disturbing uncommitted work, or when an agent should run in its own worktree via `sb git worktree`.
---

# sb worktree

Use `sb git worktree` for any task that must not share the primary checkout
with another agent or with uncommitted work.

## When to use

- A second agent must fix a bug while the first keeps editing the primary tree.
- You need a clean base branch without stashing or committing the primary's WIP.
- You want the worktree removed and the branch merged/deleted in one reviewed
  step afterwards.

Do **not** create worktrees with raw `git worktree add` in this environment:
the ignored-file copy, base resolution, path convention and safe cleanup live in
`sb git worktree`.

## Workflow

1. In the repository (primary checkout), scaffold the config once:

   ```bash
   sb git worktree init
   # commit .ctx/sb.yaml so every clone/agent shares base + copy
   ```

2. Create the worktree and enter it:

   ```bash
   WORKTREE=$(sb git worktree new fix/<short-slug>)
   cd "$WORKTREE"
   ```

   `stdout` is only the path; if the command fails, nothing was created (except
   a worktree whose configured copy failed — the error lists the files).

3. Work and commit normally inside the worktree. Never touch the primary
   checkout from there.

4. Finish from the **primary** checkout (never from inside the worktree):

   ```bash
   sb git worktree finish fix/<short-slug>          # merge into main + cleanup
   sb git worktree finish fix/<short-slug> --pr     # push + open a PR, keep tree
   ```

5. Abandon instead of finishing:

   ```bash
   sb git worktree rm fix/<short-slug> --delete-branch
   # dirty or unmerged? inspect first; --force discards
   ```

## Rules

- The primary checkout is read-only from the worktree's perspective. Do not
  commit, checkout or merge there while another agent works.
- Commit before `finish`; `finish` refuses a dirty primary only for unexpected
  changes and merge-branch aborts on conflicts before pushing.
- `finish` merges into `main`/`master` and pushes the target. Use `--pr` when
  review is required.
- After `finish --pr` reports a merged PR, it removes the worktree and deletes
  the local branch; run `git pull` in the primary to update `main`.
- Worktrees live under `/var/tmp/sb-worktrees/<repo>/<slug>`; they are scratch
  data, not backups.
- Never copy secrets into a tracked file; `worktree.copy` paths stay untracked.

## Inspect

```bash
sb git worktree ls
sb git worktree ls --json | jq '.[] | select(.dirty)'
```
