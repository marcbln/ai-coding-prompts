# AI Coding Prompts – Repository Guidelines

This repository is a curated library of AI coding conventions, prompt templates,
workflows, and skills for use across multiple AI coding assistants.

## Repository Structure

```
conventions/              # Language- and framework-specific coding conventions
windsurf-global-skills/   # Windsurf Cascade skills (SKILL.md format)
windsurf-global-workflows/ # Windsurf Cascade workflow prompts
iamhenry/                 # Additional AI agent modes and prompt collections
_ai/knowledge/            # Reference knowledge files for AI context
adapters/                 # Per-platform adapter configs for ruler and other tools
.ruler/                   # Ruler configuration (this directory)
```

## Conventions Files

Files in `conventions/` follow this format:
- YAML frontmatter with `name`, `description`, `tags`, and `documentType: CONVENTIONS`
- Markdown body with clear sections

When adding or editing a convention file, keep changes focused and consistent
with the style of the existing files.

## Windsurf Skills

Each skill lives in `windsurf-global-skills/<skill-name>/` and must contain:
- `SKILL.md` with YAML frontmatter (`name`, `description`)
- Any supporting resource files referenced by `SKILL.md`

## Windsurf Workflows

Workflow files in `windsurf-global-workflows/` use YAML frontmatter:
- `description`: one-line summary shown in the Windsurf UI
- `auto_execution_mode`: set to `1` for automatic execution

## Adapters

The `adapters/` directory contains per-platform configurations and instructions
for wiring the content of this library into specific AI coding tools via ruler.
See `adapters/README.md` for an overview.

## Contribution Guidelines

1. Keep prompts general and reusable – avoid project-specific details.
2. Add frontmatter to every new file.
3. Place new convention files in `conventions/`.
4. Place new Windsurf skills in `windsurf-global-skills/<skill-name>/`.
5. Place new Windsurf workflows in `windsurf-global-workflows/`.
6. Run `ruler apply` (with the appropriate adapter config) to regenerate agent
   config files after editing `.ruler/` content.
