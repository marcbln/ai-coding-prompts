# Ruler Adapter

Connect every prompt, convention, and skill in this library to **any** AI coding
assistant that [Ruler](https://github.com/intellectronica/ruler) supports
(GitHub Copilot, Claude Code, Cursor, Windsurf, Aider, and many more) — from
one central configuration.

## Prerequisites

```bash
npm install -g @intellectronica/ruler   # requires Node.js ≥ 20.19
```

## 1 – Distribute rules to all agents

```bash
# From the repository root
ruler apply
```

Ruler reads `.ruler/AGENTS.md` (and any other `.md` files in `.ruler/`) and
writes the appropriate config file for every enabled agent:

| Agent | Generated file |
|-------|---------------|
| GitHub Copilot | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `AGENTS.md` |
| Windsurf | `AGENTS.md` |
| Aider | `AGENTS.md`, `.aider.conf.yml` |
| … and [many more](https://github.com/intellectronica/ruler#supported-ai-agents) | |

Target only specific agents when needed:

```bash
ruler apply --agents claude,cursor
```

## 2 – Connect the skills library

The `windsurf-global-skills/` directory contains skills in the universal
[`SKILL.md`](https://agentskills.io) format.  Because Ruler uses the same
format when distributing skills to agents (`.claude/skills/`, `.cursor/skills/`,
etc.), these skills work with **every** ruler-supported agent — not just
Windsurf.

### Option A – symlink as a workspace skill directory (recommended)

Create a symlink so Ruler picks up the skills automatically for any project in
this repo:

```bash
# From the repository root (Mac / Linux)
ln -s "$(pwd)/windsurf-global-skills" .ruler/skills
```

```cmd
REM Windows (as Administrator) — from the repository root
mklink /D ".ruler\skills" "%CD%\windsurf-global-skills"
```

Then apply rules with skills enabled (the default):

```bash
ruler apply --skills
```

Ruler will copy / link the skills into each agent's own skills directory
(`.claude/skills/`, `.cursor/skills/`, etc.).

### Option B – point each agent directly at the skills folder (Windsurf only)

If you only use Windsurf and prefer to keep the existing symlink approach:

```bash
# Mac / Linux
ln -s "$(pwd)/windsurf-global-skills" ~/.codeium/windsurf-next/skills
```

```cmd
REM Windows (as Administrator)
mklink /D "%APPDATA%\Codeium\Windsurf\global_skills" "%CD%\windsurf-global-skills"
```

## 3 – Distribute global workflows (Windsurf)

```bash
# Mac / Linux
ln -s "$(pwd)/windsurf-global-workflows" ~/.codeium/windsurf-next/global_workflows
```

```cmd
REM Windows (as Administrator)
mklink /D "%APPDATA%\Codeium\Windsurf\global_workflows" "%CD%\windsurf-global-workflows"
```

Restart Windsurf after creating the symlink.

## Configuration reference

The default Ruler config lives in `.ruler/ruler.toml`.  The `ruler.toml` in
this folder (`adapters/ruler/ruler.toml`) is a drop-in alternative that enables
all agents at once — useful when cloning this library into a new project:

```bash
ruler apply --config adapters/ruler/ruler.toml
```
