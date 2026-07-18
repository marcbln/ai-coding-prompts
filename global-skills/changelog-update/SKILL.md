---
name: changelog-update
description: Update an existing CHANGELOG.md with recent changes since the last documented version. Use before a release or when asked to add new entries to an existing changelog.
---

# Changelog Update

Update an existing `CHANGELOG.md` with changes since the last documented version.

## Process

1. **Read the existing** `CHANGELOG.md` to find the most recent version/tag documented.

2. **Get commits since that tag**:
   ```bash
   git --no-pager log <last-tag>..HEAD --pretty=format:"%H %s" --no-merges
   ```

3. **Categorize commits** into sections (same categories as `changelog-init`).

4. **Determine the next version** — bump major/minor/patch based on the changes.

5. **Prepend a new section** to the top of the existing file with the new version, date, and categorized entries. Rewrite commit messages into human-readable sentences.

6. **Add a comparison URL** for the new version at the bottom of the file.
