---
name: changelog
description: Create or update a CHANGELOG.md from git history. Use when asked to generate, update, or maintain a changelog, write release notes from commits, or document changes between versions.
---

# Changelog

Create or update a `CHANGELOG.md` by analyzing the git history of the current repository.

## Process

1. **Inspect the repository**
   - Check if a `CHANGELOG.md` already exists.
   - If it does, read it to find the most recent version/tag documented so you know where to start.

2. **Gather git history**
   - List all tags sorted by version: `git tag --sort=-version:refname`
   - If updating an existing changelog, only process commits since the last documented tag.
   - If creating from scratch, process all commits (or ask the user how far back to go).
   - Use `git log` with a structured format to collect commits:
     ```
     git --no-pager log <range> --pretty=format:"%H %s" --no-merges
     ```

3. **Categorize commits**
   - Group commits into sections using conventional commit prefixes when present, otherwise infer from content:
     - **Added** – new features (`feat:`, `add`, `✨`, `🎉`)
     - **Changed** – changes to existing functionality (`refactor:`, `perf:`, `♻️`, `⚡`)
     - **Fixed** – bug fixes (`fix:`, `🐛`, `🚑`)
     - **Removed** – removed features (`remove`, `delete`, `🔥`)
     - **Security** – security fixes (`security`, `🔒`)
     - **Deprecated** – soon-to-be removed features
     - **Documentation** – docs only (`docs:`, `📝`)
     - **Chores** – build, CI, deps (`chore:`, `build:`, `ci:`, `💚`, `⬆️`)
   - Skip purely mechanical commits: merge commits, version bumps, changelog updates.

4. **Determine versions**
   - Use git tags as version boundaries.
   - For unreleased commits (between HEAD and the latest tag), use an `[Unreleased]` section.
   - If no tags exist, group all commits under `[Unreleased]`.

5. **Write the changelog**
   - Follow the [Keep a Changelog](https://keepachangelog.com) format.
   - Prepend new entries to the top of an existing file; preserve existing content.
   - Each entry should be a concise, human-readable sentence — not a raw commit subject.
     Rewrite robotic messages like "fix: null ptr in foo" → "Fixed a null pointer error in the foo module."

## Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- ...

## [1.2.0] - 2026-03-01

### Fixed
- ...

### Changed
- ...

[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/compare/v1.1.0...v1.2.0
```

## Tips

- Use `git remote get-url origin` to construct comparison URLs at the bottom of the file.
- Use `git log <tag1>..<tag2>` to get commits between two tags.
- Use `git log --date=short --pretty=format:"%ad"` to get the date of the tagged commit for the version header.
- If the user specifies a version range or a number of recent releases, respect that constraint.
- If the project uses a non-standard version scheme (e.g. date-based), adapt the format accordingly.
- Ask the user before making the changelog excessively long (e.g. hundreds of entries).
