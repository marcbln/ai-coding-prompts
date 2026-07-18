---
name: manage-knowledge-base
description: Search, read, create, or update markdown files in the _ai/ knowledge base. Use when asked to document architecture, update specs, create manuals, or save context for future AI sessions.
---

# Knowledge Base Management

Maintain the `_ai/` knowledge base — a collection of markdown files that serves as the project's second brain.

## Workflow

### 1. Determine the target location

Use `kb-structure.md` to route content to the correct subfolder:

| Directory | Purpose |
|---|---|
| `_ai/context-definitions/` | Core concepts, integrations, shared features |
| `_ai/knowledge/` | General wiki, component behaviors, devops guides |
| `_ai/specs/` | Strict specification documents |
| `_ai/technical_decisions/` | Architecture Decision Records (ADRs) |
| `_ai/manuals/` | How-to guides for humans |
| `_ai/backlog/` | Project management, epics, tasks |

### 2. Create or update the file

- Use Obsidian-flavored markdown with `[[wikilinks]]` for internal references
- Include YAML frontmatter with `title`, `date`, and `tags`
- Place files in the correct subfolder per `kb-structure.md`

### 3. Validate

- Run `./kb-helper.sh` from the skill directory for tag search or frontmatter queries
- Ensure wikilinks reference existing files where possible
