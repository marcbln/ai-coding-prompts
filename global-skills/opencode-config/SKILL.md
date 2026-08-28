---
name: opencode-config
description: Expert guide for creating, updating, and migrating OpenCode configuration files across OpenCode v1 and v2 (global and project-local).
---

# OpenCode Configuration Expert (v1 & v2)

This skill guides you on writing valid OpenCode configuration files (`opencode.json`, `opencode.jsonc`, `tui.json`, `cli.json`, `AGENTS.md`, and `auth.json`).

---

## 1. File Locations & Precedence

| Scope | Path | Purpose |
| :--- | :--- | :--- |
| **Global Config** | `~/.config/opencode/opencode.json(c)` | User-wide defaults, custom providers, base MCP servers |
| **Global UI (v1)** | `~/.config/opencode/tui.json(c)` | Terminal keybindings, color themes, display settings |
| **Global UI (v2)** | `~/.config/opencode/cli.json` | Consolidated CLI & terminal UI settings |
| **Global Auth** | `~/.local/share/opencode/auth.json` | Stored credentials & provider tokens (do not commit) |
| **Project Config** | `<root>/opencode.json(c)` or `<root>/.opencode/opencode.json(c)` | Project-specific models, MCP servers, permissions |
| **Project Rules** | `<root>/AGENTS.md` or `<dir>/AGENTS.md` | Workspace instructions (traversed hierarchically) |

**Precedence Order:**  
`Remote (.well-known)` < `Global (~/.config/opencode)` < `Environment Variables` < `Project Local (.opencode/)`

---

## 2. Key Differences: v1 vs v2

| Feature | OpenCode v1 (Current Standard) | OpenCode v2 |
| :--- | :--- | :--- |
| **Binary** | `opencode` | `opencode2` (or `opencode` in v2 releases) |
| **UI Config** | `tui.json(c)` (supports cascading) | Consolidated `cli.json` |
| **MCP Servers** | Direct `mcp` object with stdio commands | Extended `mcp.servers` supporting stdio & streamable HTTP |
| **Instructions** | `instructions` array in JSON + basic AGENTS.md | Native recursive `AGENTS.md` hierarchy + config rules |
| **Agent / Tools** | Flat `permission` & `agent` structure | Sub-agent definitions, specialized tool pipelines |
| **Plugins** | Legacy `@opencode-ai/plugin` interface | Rewritten event-driven plugin lifecycle |

---

## 3. Writing OpenCode v1 Configurations

### v1 Project Config (`opencode.jsonc`)
```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-3-7-sonnet",
  "small_model": "anthropic/claude-3-5-haiku",
  
  // Custom provider overrides (optional)
  "provider": {
    "openrouter": {
      "name": "OpenRouter",
      "base_url": "https://openrouter.ai/api/v1"
    }
  },

  // MCP Servers
  "mcp": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    },
    "postgres": {
      "command": "uvx",
      "args": ["mcp-server-postgres", "--conn-string", "postgresql://localhost/mydb"]
    }
  },

  // Formatting commands per file extension
  "formatter": {
    "prettier": {
      "command": "npx prettier --write $FILE",
      "extensions": [".js", ".ts", ".jsx", ".tsx", ".json", ".md"]
    }
  },

  // External instructions / documentation files
  "instructions": [
    ".opencode/coding-standards.md"
  ],

  // Permissions & safety
  "permission": {
    "bash": "ask",
    "edit": "allow"
  }
}
```

### v1 Terminal Config (`~/.config/opencode/tui.jsonc`)
```jsonc
{
  "theme": "tokyonight",
  "keybindings": {
    "submit": ["enter"],
    "newline": ["shift+enter", "alt+enter"]
  }
}
```

---

## 4. Writing OpenCode v2 Configurations

### v2 Project Config (`opencode.jsonc`)
```jsonc
{
  "$schema": "https://opencode.ai/v2/config.json",
  "model": "anthropic/claude-3-7-sonnet",
  "small_model": "anthropic/claude-3-5-haiku",

  // Modern MCP Server specification
  "mcp": {
    "servers": {
      "context-server": {
        "type": "streamable-http",
        "url": "http://127.0.0.1:8080/mcp"
      },
      "local-tools": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "custom-mcp-server"]
      }
    }
  },

  // Custom agent definitions & tool permissions
  "agents": {
    "reviewer": {
      "model": "openai/o3-mini",
      "instructions": "You focus solely on code review and security audits.",
      "tools": ["read_file", "search_directory"]
    }
  },

  "formatter": {
    "biome": {
      "command": "npx @biomejs/biome format --write $FILE",
      "extensions": [".ts", ".tsx", ".js"]
    }
  }
}
```

### v2 Terminal Config (`~/.config/opencode/cli.json`)
```json
{
  "theme": "catppuccin-mocha",
  "editor": "code",
  "auto_update": true
}
```

---

## 5. Rules for LLM Generation
1. **Always use `.jsonc` or `.json`** with valid syntax.
2. **Never expose secrets directly in `opencode.json`**; refer to environment variables (`${VAR_NAME}`) or instruct the user to store tokens in `~/.local/share/opencode/auth.json`.
3. **If targeting v1:** Never use `mcp.servers` object structure or `cli.json`.
4. **If targeting v2:** Use modern MCP schemas and consolidated `cli.json`.
