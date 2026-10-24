---
name: docdeck
description: Open Markdown documents and folders in docdeck, the local tabbed, live-reloading Markdown viewer. Use whenever the user says "open with docdeck", "docdeck it", "show it in docdeck", or asks to open/preview a plan, report, log, status file, or other Markdown document on the desktop. Handles one file, several files, or a folder as a session watch, and forwards the request to an already running docdeck window.
---

# Open documents with docdeck

docdeck is a Linux-only GUI Markdown viewer. It is read-only, watches open files
for changes, and runs as a single instance: `docdeck <path>` forwards the path to
the running window and exits immediately.

## Workflow

1. Confirm the target exists and resolve an absolute path:

   ```bash
   test -f report.md && realpath report.md
   ```

2. Open it:

   ```bash
   docdeck /absolute/path/report.md
   ```

3. Treat success as exit status 0. The release binary detaches with
   `fork` + `setsid`, so do not wait for output, poll the process, or wrap it in
   `nohup ... &`.

## Commands

| Goal | Command |
| --- | --- |
| Open one document | `docdeck /abs/file.md` |
| Open several documents | `docdeck /abs/plan.md /abs/status.md` |
| Add a folder as a session watch | `docdeck /abs/folder` |
| Forward to the running window | Same command; no special flag |

A folder argument adds a session-only watch and lists its Markdown files in the
Inbox. It does not open a tab. Explicit file arguments open before the config
scan starts.

## Rules

- Do **not** run `docdeck --help`; it is a GUI app and prints no usage.
- Do **not** kill, restart, or background an existing docdeck process. The
  single-instance plugin forwards CLI arguments to the running window.
- Do **not** edit `~/.config/docdeck/config.toml` just to open a file. The config
  is read once at startup and only controls persistent watches and excludes.
- Do **not** use docdeck to edit content. It renders Markdown only.
- Use absolute paths when the working directory may change. Relative paths
  resolve against the caller's current directory.
- If no desktop display is available (`DISPLAY` unset), report that the file
  cannot be shown and offer the path instead of launching it.

## Verification

Only verify when the user asks whether it opened:

```bash
pgrep -a docdeck
wmctrl -l | grep -i docdeck    # if wmctrl is installed
```

An exit status of 0 with a running `docdeck` process is sufficient. Do not read
the document back from the GUI.

## Troubleshooting

- **`docdeck: command not found`** — the binary is expected at
  `~/.local/bin/docdeck` (or elsewhere on `PATH`). Report this rather than
  building or installing the app.
- **Window opens blank** — the machine is likely on the NVIDIA proprietary
  driver. Do not change flags by default; the binary already disables DMA-BUF.
  Only use `docdeck --accelerated <file>` when the user confirms it works.
- **Command blocks** — the user or environment set `DOCDECK_FOREGROUND=1`.
  Unset it for detached launches.
- **Config edits are ignored** — restart docdeck; the config is loaded once.

## Examples

```bash
# User: "open MIGRATION_STATUS.md with docdeck"
docdeck /topdata/shop-hotfixes/MIGRATION_STATUS.md

# User: "show the plan and the report in docdeck"
docdeck /abs/plan.md /abs/report.md

# User: "watch the backlog folder in docdeck"
docdeck /topdata/shop-hotfixes/_ai/backlog

# User: "open it, but stay in the foreground so I can debug"
DOCDECK_FOREGROUND=1 docdeck /abs/file.md
```

Source and full behavior reference: `/home/marc/devel/docdeck/README.md`.
