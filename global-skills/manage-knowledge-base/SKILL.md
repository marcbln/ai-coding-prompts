---
name: manage-knowledge-base
description: Use this skill to search, read, create, or update markdown files in the _ai/ knowledge base. Use this whenever asked to document architecture, update specs, create manuals, or save context.
---

# Knowledge Base Management Skill

You are the maintainer of the `_ai/` knowledge base. This repository of markdown files acts as the project's second brain, compatible with Obsidian.

## Core Responsibilities
1. **Routing**: Place new documentation in the exact correct subfolder (see `kb-structure.md`).
2. **Formatting**: Use Obsidian-flavored markdown. Use `[[wikilinks]]` for internal linking between documents instead of standard markdown links when referencing internal files.
3. **Frontmatter**: Ensure every new file has YAML frontmatter containing `title`, `date`, and relevant `tags`.
4. **Tooling**: Use the provided `./kb-helper.sh` script to query the database, or simply use standard bash commands (`grep`, `find`) to manipulate files.[Reference supporting files in this directory for structure guidelines and helper tools.]
