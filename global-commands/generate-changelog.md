---
description: Analyzes git diffs to generate a semantic versioned CHANGELOG entry.
auto_execution_mode: 1
---

You are a **Release Manager**. Your task is to update `CHANGELOG.md` based on recent changes.

## Process

1. **Get Changes**: Run `git diff $(git describe --tags --abbrev=0)..HEAD` (or ask me for the commit range if no tags exist).
2. **Analyze**: Group changes into:
   - `### Added`
   - `### Changed`
   - `### Fixed`
   - `### Removed`
3. **Draft Entry**:
   - Propose a new Semantic Version (Major.Minor.Patch) based on the severity of changes.
   - Write user-focused bullet points (e.g., "Added 'Default Color' option" instead of "Updated ConfigService.php").
4. **Update**:
   - Append this entry to the top of `CHANGELOG.md`.
   - If the file doesn't exist, create it.

Ask me for the commit range to start.
