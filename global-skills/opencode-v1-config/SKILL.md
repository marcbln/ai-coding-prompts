---
name: opencode-v1-config
description: Specialized rules for writing OpenCode v1 global and project configurations (opencode.json, tui.json, AGENTS.md).
---

# OpenCode v1 Configuration Standard

## File Locations
- **Global Config:** `~/.config/opencode/opencode.json(c)`
- **Global TUI:** `~/.config/opencode/tui.json(c)`
- **Project Config:** `<project-root>/opencode.json(c)` or `<project-root>/.opencode/opencode.json(c)`
- **Instructions:** `<project-root>/AGENTS.md` and paths in `instructions` array.

## Core Schema Structure
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-3-7-sonnet",
  "small_model": "anthropic/claude-3-5-haiku",
  
  "mcp": {
    "<server-name>": {
      "command": "<executable>",
      "args": ["arg1", "arg2"],
      "env": {
        "ENV_KEY": "value"
      }
    }
  },

  "formatter": {
    "<name>": {
      "command": "<cmd> $FILE",
      "extensions": [".ext"]
    }
  },

  "instructions": [
    "AGENTS.md",
    ".opencode/rules.md"
  ],

  "permission": {
    "bash": "ask",
    "edit": "allow"
  }
}
```

## TUI Config (`tui.jsonc`)
```jsonc
{
  "theme": "tokyonight",
  "keybindings": {
    "submit": ["enter"],
    "newline": ["shift+enter"]
  }
}
```
