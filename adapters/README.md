# Adapters

This directory contains per-platform adapter configurations that bridge the
content of this library with specific AI coding tools.

## What Is an Adapter?

[Ruler](https://github.com/intellectronica/ruler) distributes a centralised set
of AI instructions (stored in `.ruler/`) to every supported AI agent.  
An *adapter* here is a self-contained folder with:

- A `ruler.toml` that enables only the agents relevant to that platform.
- A `README.md` with any extra manual setup steps (e.g. symlinking skills
  folders, configuring MCP servers).

## Available Adapters

| Adapter | Target tool(s) | Folder |
|---------|---------------|--------|
| Windsurf | Windsurf Cascade | [`windsurf/`](windsurf/) |
| Cursor | Cursor AI | [`cursor/`](cursor/) |
| Claude | Claude Code | [`claude/`](claude/) |

## Usage

```bash
# Apply rules for a specific platform
ruler apply --config adapters/windsurf/ruler.toml

# Apply rules for all default agents (configured in .ruler/ruler.toml)
ruler apply
```

## Adding a New Adapter

1. Create a new sub-directory: `adapters/<platform>/`
2. Add a `ruler.toml` that sets `default_agents` to the relevant agent(s).
3. Add a `README.md` with any manual setup instructions.
4. List the new adapter in the table above.
