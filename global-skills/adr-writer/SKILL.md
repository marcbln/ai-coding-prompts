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

2. **Assign the next ID.** ADRs are numbered per decision date: `YYMMDD-N`, where `YYMMDD`
   is the decision date and `N` is a per-day sequence number starting at 1. Use the helper:
   ```bash
   python3 scripts/next_adr_id.py <adr-directory> <yyyymmdd>
   ```
   It returns the next `N` for that date (highest existing N of the day + 1). If a
   directory does not exist yet, the next ID is `1`.

 3. **Name the file** `ADR__<YYMMDD-N>__<kebab-case-title>.md` (e.g. `ADR__260731-1__central-email-dispatch-pipeline.md`).

 4. **Copy the template** `assets/ADR_TEMPLATE.md` into the ADR directory and fill it in.
    Put the ADR number in the **filename** (step 3) and in the frontmatter `adrId:`
    key (from the template). **Never write an `id:` key** — the control plane reserves
    `id` for its own UUID primary key, so a non-UUID `id` (like `260821-1`) makes the
    doc fail to sync.

5. **Write the body** — every section is required except `Related Decisions` (omit if none):
   * `Context` — the problem and why a decision was needed.
   * `Decision` — the chosen solution; be specific and explain *how* it works.
   * `Consequences` — honest positive **and** negative outcomes / trade-offs.
   * `Alternatives Considered` — each rejected option named with the reason it was rejected.
   * `Related Decisions` — cross-references by filename (e.g. `ADR__260731-1__central-email-dispatch-pipeline.md`).

6. **Update the README index** in that directory (the `## Index` section lists ADRs per
   year). Add the new ADR under its year.

7. **To supersede** an existing ADR: set its `status` to `Superseded`, and in the new ADR's
   `Related Decisions` reference the superseded one.

## Notes

* Frontmatter order and keys (`title`, `status`, `date`, `deciders`, `tags`, `adrId`) must be preserved.
* The `id` frontmatter key is reserved by the control plane for its UUID primary key. Do not add `id:` to an ADR — the ADR number belongs in `adrId:` (and the filename).
* `date` uses `YYYY-MM-DD`; `status` is one of `Accepted | Deprecated | Superseded`.
* Keep ADRs factual and concise (target ~30-50 lines). Prefer listing over prose.
