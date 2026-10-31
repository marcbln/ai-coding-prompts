---
name: comment-shell-commands
description: Enforces adding clear, descriptive '#' comments directly above every bash/shell command before executing it. Use whenever running terminal commands, scripts, or automated tools.
---

# Comment Shell Commands

## Purpose
Ensure all commands executed via the shell or terminal tool are self-documenting and immediately clear to human observers.

## Rule
Whenever you execute a command using the `bash` or terminal tool:
1. **Always prepend a `# comment`** on the first line inside the command payload.
2. The comment must concisely summarize **what** the command does and **why** it is being executed.
3. For multi-step commands or piped one-liners, add a comment before the main block or major sections.

## Examples

### ❌ Bad:
```bash
for i in $(seq 1 24); do txt=$(agent-browser eval 'document.body.innerText.slice(0,80)' 2>/dev/null); ...
```

### ✅ Good:
```bash
# Poll browser page until 'Look again' appears (up to 6m), then inspect repository cache
for i in $(seq 1 24); do txt=$(agent-browser eval 'document.body.innerText.slice(0,80)' 2>/dev/null); ...
```

### ✅ Good (multi-step):
```bash
# Set light theme in local storage, open app, and capture screenshot
agent-browser eval 'localStorage.setItem("topdata.theme.v1","light")' >/dev/null \
  && agent-browser open http://localhost:5183 \
  && sleep 2 \
  && agent-browser screenshot /tmp/opencode/rm-cached.png
```
