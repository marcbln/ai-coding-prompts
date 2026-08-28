---
name: opencode-v2-config
description: Specialized rules for writing OpenCode v2 global and project configurations (opencode.json, cli.json, sub-agents, streamable MCP).
---

# OpenCode v2 Configuration Standard

## File Locations
- **Global Config:** `~/.config/opencode/opencode.json(c)`
- **Global CLI/TUI:** `~/.config/opencode/cli.json`
- **Project Config:** `<project-root>/opencode.json(c)` or `<project-root>/.opencode/opencode.json(c)`
- **Agent Instructions:** Native upward search for `AGENTS.md` in parent/child directories.

## Core Schema Structure
```jsonc
{
  "$schema": "https://opencode.ai/v2/config.json",
  "model": "anthropic/claude-3-7-sonnet",
  "small_model": "anthropic/claude-3-5-haiku",

  "mcp": {
    "servers": {
      "remote-tools": {
        "type": "streamable-http",
        "url": "http://localhost:8000/mcp"
      },
      "local-tools": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
      }
    }
  },

  "agents": {
    "coder": {
      "model": "anthropic/claude-3-7-sonnet",
      "instructions": "Dedicated code generation agent.",
      "tools": ["*"]
    },
    "reviewer": {
      "model": "openai/o3-mini",
      "instructions": "Dedicated code audit agent.",
      "tools": ["read_file", "search_directory"]
    }
  },

  "formatter": {
    "prettier": {
      "command": "npx prettier --write $FILE",
      "extensions": [".ts", ".js", ".json", ".md"]
    }
  }
}
```

## CLI Config (`cli.json`)
```json
{
  "theme": "catppuccin-mocha",
  "editor": "code",
  "notifications": true
}
```
