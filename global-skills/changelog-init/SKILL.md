---
name: changelog-init
description: Create a CHANGELOG.md from scratch by processing all git history. Use when a project has no changelog yet and you need to generate one from all historical commits.
---

# Changelog Init

Create a new `CHANGELOG.md` by processing the full git history of the repository.

## Process

1. **List all tags** sorted by version:
   ```bash
   git tag --sort=-version:refname
   ```

2. **If tags exist**, process commits between each consecutive tag pair, oldest to newest. For each range:
   ```bash
   git --no-pager log <older-tag>..<newer-tag> --pretty=format:"%H %s" --no-merges
   ```

3. **If no tags exist**, group all commits under `[Unreleased]`.

4. **Categorize commits** into sections using conventional commit prefixes:
   - **Added** — `feat:`, `add`
   - **Changed** — `refactor:`, `perf:`
   - **Fixed** — `fix:`
   - **Removed** — `remove:`
   - **Security** — `security:`
   - **Deprecated** — `deprecate:`
   - **Documentation** — `docs:`
   - **Chores** — `chore:`, `build:`, `ci:`

5. **Generate the file** using Keep a Changelog format with comparison URLs. Rewrite commit messages into human-readable sentences.

6. **Get the remote URL** for comparison links:
   ```bash
   git remote get-url origin
   ```
