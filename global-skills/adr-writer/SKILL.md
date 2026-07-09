---
name: adr-writer
description: Write Architecture Decision Records (ADRs) in the TradeGuard-style format (YAML frontmatter, Context/Decision/Consequences/Alternatives/Related sections). Use when a user asks to create, draft, or document an architectural decision, create an "ADR", record a significant technical decision, or choose a design pattern/framework/integration. Also use to update or supersede an existing ADR.
---

# ADR Writer

Write Architecture Decision Records (ADRs) that document significant, hard-to-reverse
technical decisions. The format follows the TradeGuard `_ai/technical_decisions` convention.

## When to use

Trigger when the user wants to capture a decision about: adding a framework, changing a core
pattern, introducing a major integration, choosing a design strategy, or recording a
trade-off. Also when asked to create/update/supersede an "ADR".

## Workflow

1. **Locate the ADR directory.** Common location: `<repo>/_ai/technical_decisions/`.
   If unsure, ask the user or search for an existing `ADR__*.md` file.

2. **Pick the category** and assign the next free ID. Use the helper:
   ```bash
   python3 scripts/next_adr_id.py <adr-directory> <category>
   ```
   Categories and number ranges:
   * `architecture`  (1000-1999) — Architecture & Infrastructure
   * `backend`       (2000-2999) — Backend Core & Data Logic
   * `frontend`      (3000-3999) — Frontend & UI
   * `integrations`  (4000-4999) — External Integrations
   * `devops`        (5000-5999) — DevOps & Workflows

   IDs step by 10 (e.g. 1000, 1005, 1015) to leave room for inserts; never reuse an ID.

3. **Name the file** `ADR__<ID>-<kebab-case-title>.md` (e.g. `ADR__1070-server-driven-entity-refresh.md`).

4. **Copy the template** `assets/ADR_TEMPLATE.md` into the ADR directory and fill it in.

5. **Write the body** — every section is required except `Related Decisions` (omit if none):
   * `Context` — the problem and why a decision was needed.
   * `Decision` — the chosen solution; be specific and explain *how* it works.
   * `Consequences` — honest positive **and** negative outcomes / trade-offs.
   * `Alternatives Considered` — each rejected option named with the reason it was rejected.
   * `Related Decisions` — cross-references by ID (e.g. `1015-legacy-tenant-isolation-sso.md`).

6. **Update the README index** in that directory (the `## Index` section lists files per
   category). Add the new ADR under its category and keep the `## Taxonomy` ranges in sync.

7. **To supersede** an existing ADR: set its `status` to `Superseded`, and in the new ADR's
   `Related Decisions` reference the superseded one.

## Notes

* Frontmatter order and keys (`title`, `status`, `date`, `deciders`, `tags`) must be preserved.
* `date` uses `YYYY-MM-DD`; `status` is one of `Accepted | Deprecated | Superseded`.
* Keep ADRs factual and concise (target ~30-50 lines). Prefer listing over prose.
