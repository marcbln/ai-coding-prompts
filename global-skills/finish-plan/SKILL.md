---
name: finish-plan
description: Archive an implementation plan by marking it as completed and moving it from the active folder to the archive folder. Use when a plan has been fully implemented and needs to be finalized.
---

# Finish Plan

Mark an implementation plan as completed and move it to the archive.

## Usage

Run the bundled script with the plan filename as the argument:

```bash
scripts/archive-plan.sh <plan-filename>
```

The script resolves paths relative to the git root and will:

- Set `status: completed` in the frontmatter.
- Add a `completedAt` timestamp in `YYYY-MM-DD HH:MM` format.
- Move the file from `_ai/backlog/active/` to `_ai/backlog/archive/`.

Confirm the file was moved successfully after running.
