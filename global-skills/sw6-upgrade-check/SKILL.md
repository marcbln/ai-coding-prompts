---
name: sw6-upgrade-check
description: "Check a Topdata Shopware 6 plugin against newer Shopware releases, or upgrade it to a new 6.x line, using a local shopware/shopware clone. Use when asked whether a plugin is compatible with a Shopware version, to verify or check a plugin against new Shopware releases, to upgrade a plugin (e.g. 6.6 to 6.7), or for the recurring per-release compatibility check. Maintains .topdata/shopware.yaml (anchor and verified history) and writes reports under .topdata/upgrades/."
---

# Shopware 6 Plugin Upgrade Check

## Overview

Verify or upgrade one Topdata plugin against Shopware releases. Two modes over one workflow:

- **maintenance** — same release line (e.g. 6.7.9.1 → 6.7.15.1): small diffs, most runs end "no impact".
- **line-upgrade** — move to a new minor line (e.g. 6.6.x → 6.7.x): large diffs; UPGRADE guides and targeted symbol diffs are mandatory.

The Shopware clone is the source of truth; the plugin's `.topdata/shopware.yaml` is the memory (anchor + verified history). Run everything from the plugin repository; resolve this skill's scripts relative to the skill base directory given at load time.

## Inputs

- `SW6_REPO` — full clone of `shopware/shopware`; default `/home/marc/devel/git-digest/repos/shopware-shopware`.
- Target tag (e.g. `6.7.15.1`) and mode — ask the user if not given.
- `.topdata/shopware.yaml` in the plugin repo (see `assets/shopware.yaml.example`).
- Scripts: `scripts/inventory.sh`, `scripts/upgrade_sections.sh`.

## Step 0 — Preflight

1. Read the plugin's own docs first: `AGENTS.md`, `_ai/SPEC.md`, `_ai/lessons-learned.md`, `TEST-CHECKLIST.md`, `README.md`. They carry the architecture map used later for impact analysis.
2. If tags may be stale: `git -C "$SW6_REPO" fetch --tags --quiet` (network).
3. Resolve the anchor: newest `verified` entry per release line in `.topdata/shopware.yaml`.
4. Confirm target + mode with the user if ambiguous. Sensible proposal: newest patch of the current line for maintenance; newest release of the next line for a line-upgrade.

### Bootstrap (no `.topdata/shopware.yaml` yet)

Never silently assume the anchor.

1. Generate candidates: composer.json `require.shopware/core` floor (e.g. `~6.7.0` → `6.7.0.0`), plus any version hints in `CHANGELOG.md` or git history of `composer.json`.
2. Present the candidates and ask the user to confirm the tag the plugin is actually known-good on.
3. Write the entry with `result: assumed` (no `level`): it is a baseline, not a verification.

## Step 1 — Detect releases in range

```bash
git -C "$SW6_REPO" tag -l 'v6.*' --sort=version:refname
```

- maintenance: same-line tags strictly after the anchor.
- line-upgrade: all tags after the anchor up to the target (both lines matter in the range).

The set of intervening releases is the check range: anchor (exclusive) → target (inclusive).

## Step 2 — Curated context first

```bash
scripts/upgrade_sections.sh "$SW6_REPO" <anchor> <target>
git -C "$SW6_REPO" diff --name-status <anchor> <target> -- changelog/
```

- Read the UPGRADE sections fully — curated and small; this is where breaking changes are named explicitly.
- Changelog filenames are slugs (e.g. `2024-06-11-add-storage-name-to-entity-attributes.md`). Shortlist by area/slug first, then read only the shortlisted files: `git -C "$SW6_REPO" show <target>:<path>`.
- Repo layout, trust levels and measured diff budgets: `references/shopware-repo-anatomy.md`.

## Step 3 — Plugin inventory

```bash
scripts/inventory.sh .
```

Emits FQCNs, decorated/referenced services, event subscribers, routes, Twig targets/blocks/shadowed templates, and JS registrations. Match against Step 2 candidates using `references/inventory-and-matching.md`; corroborate with the plugin docs from Step 0. Prefer symbol + area evidence over keyword-only matches.

## Step 4 — Triage gate

No plausible affected items → go to Step 6 at the highest achievable level, record `pass`, done. Most maintenance checks end here; that is the point of the anchor.

## Step 5 — Investigate & fix

- Read only targeted diffs: `git -C "$SW6_REPO" diff <anchor> <target> -- <path>` (add `-W` for function context).
- Respect the diff budget in `references/shopware-repo-anatomy.md`; for patch releases the full diff is usually small enough.
- Behavioral changes (event timing, payloads, defaults, template blocks) can affect the plugin even when no symbol matches. Check UPGRADE prose for features the plugin uses.
- Make the smallest core-compatible change; do not refactor beyond compatibility.
- If a finding needs code changes, keep them reviewable: one concern per commit.

## Step 6 — Verify (be honest about the level)

| Level | Means |
|---|---|
| `static` | context review only (symbols, changelog, UPGRADE) |
| `smoke` | plugin installs + activates on the target version |
| `tests` | the plugin's test suite passes on the target |
| `qa` | critical user paths exercised |

Use the plugin's documented test path (`AGENTS.md`, `TEST-CHECKLIST.md`, focus Docker setup). If none exists, cap at `static` and record that gap. Never claim a level that was not run.

## Step 7 — Record

1. `.topdata/shopware.yaml`: append a `verified` entry (see `assets/shopware.yaml.example`); update `supported` only as far as actually verified.
2. Report: copy `assets/upgrade-report-template.md` to `.topdata/upgrades/<YYYY-MM-DD>__<target>.md` and fill it.
3. `composer.json`: bump `require.shopware/core` no further than what was verified.
4. `CHANGELOG.md`: note the Shopware compatibility.
5. Hand off: summarize findings + changes; commit/PR via the repo's usual flow (`git-commit`, `piv-create-pr`). Never push without explicit confirmation.

## Guardrails

- Never dump full diffs at scale; never search the clone without narrowing paths.
- Never bump the anchor or `supported` past what was verified; `assumed` entries are not verification.
- Do not touch `.topdata/meta.yaml` (owned by sw6-motion) or `_ai/` docs.
- Uncertain risk → list it under follow-ups in the report; do not guess and do not silently skip.

## Integration into a plugin repo

Add one line to the plugin's `AGENTS.md` so agents know this procedure exists:

> For Shopware release checks/upgrades, load the `sw6-upgrade-check` skill.
