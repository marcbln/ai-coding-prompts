# Shopware repo anatomy (for upgrade checks)

## Layout

- `changelog/release-<6-7-15-1>/<YYYY-MM-DD>-<slug>.md` — one file per change.
  - Frontmatter: `date`, `title`, `issue`, `author*`.
  - Body starts with an area heading: `# Core`, `# Administration`, `# Storefront`, sometimes others.
  - Slugs are terse; e.g. `2024-06-11-add-storage-name-to-entity-attributes.md`.
- `UPGRADE-6.<minor>.md` at repo root — curated breaking-change guidance per release line (6.3 … 6.9).
  - Sections start with a version heading `# <x.y.z.w>`.
  - Versionless `#` headings (e.g. `# Set timeout to 30 minutes`) belong to the preceding version section.
  - `UPGRADE-6.1.md`/`UPGRADE-6.2.md` have no version headings and produce no sections.
  - Sections may forward-reference future files (e.g. "migration guidance in UPGRADE-6.9.md") — keep the reference, do not chase it.
- Git tags `v<version>` — authoritative release list. Old lines (6.6.x) and current (6.7.x) get patches in parallel.
- `releases.json` — Shopware's own metadata; rarely needed, tags are preferable.

## Reading cost order

1. UPGRADE sections in range (`scripts/upgrade_sections.sh`) — always first, KBs.
2. `git diff --name-status <anchor> <target> -- changelog/` — triage slugs before opening anything.
3. Shortlisted changelog files via `git show <target>:<path>`.
4. Targeted `git diff <anchor> <target> -- <paths>`; add `-W` for function context.

## Measured diff budgets

Reference numbers from the shopware/shopware clone (2026):

| Range | Files changed | Lines |
|---|---|---|
| patch: 6.7.9.0 → 6.7.9.1 | 15 | 554 insertions |
| minor: 6.7.8.0 → 6.7.9.0 | 3,015 | ~121k |
| line-upgrade: 6.6.10.1 → 6.7.0.0 | 7,262 | ~263k |

Rule of thumb after `git diff --shortstat <anchor> <target>`: under ~50 files and ~5k insertions → full diff is acceptable; otherwise narrow by path and never read the raw diff.

## Handy commands

```bash
SW6=/home/marc/devel/git-digest/repos/shopware-shopware   # or $SW6_REPO

git -C "$SW6" fetch --tags --quiet
git -C "$SW6" tag -l 'v6.7.*' --sort=version:refname | tail
git -C "$SW6" diff --shortstat <anchor> <target>
git -C "$SW6" diff --name-status <anchor> <target> -- changelog/
git -C "$SW6" show <target>:changelog/release-6-7-15-1/2026-01-01-slug.md
git -C "$SW6" diff <anchor> <target> -- src/Core/Checkout/Customer/SalesChannel/RegisterRoute.php
git -C "$SW6" diff -W <anchor> <target> -- <path>   # function context
```

## Area headings → plugin surfaces

- `# Core` — PHP API, DAL, services, events, routing.
- `# Administration` — Vue/JS admin, admin modules.
- `# Storefront` — Twig templates, storefront JS, snippets.
- Use them to pre-filter slug lists for the plugin's inventory kinds.
