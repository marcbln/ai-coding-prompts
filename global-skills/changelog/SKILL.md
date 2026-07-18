---
name: changelog
description: Create or update a CHANGELOG.md from git history. Delegates to changelog-init or changelog-update depending on whether the file already exists. Use when asked to generate, update, or maintain a changelog.
---

# Changelog (Meta-Skill)

Check if `CHANGELOG.md` exists in the project root:

- **If it exists** → load and run the `changelog-update` skill
- **If it doesn't exist** → load and run the `changelog-init` skill
