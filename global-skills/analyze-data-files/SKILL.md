---
name: analyze-data-files
description: "Profile a folder of data files (CSV primary, xlsx optional), detect relationships between files via matching key columns, and audit data quality (missing values, duplicate rows, empty columns, outliers, join-coverage gaps). Use when the user asks to 'analyze the files in <folder>', 'profile the data in this directory', 'find relationships between these CSVs', 'check data quality of these imports', or 'audit a set of data files before upsert'."
---

# Analyze Data Files

Turn a directory of dumped/downloaded data files into an actionable map: what each
file contains, how the files relate (join keys), and where the data is dirty before
it gets imported or upserted.

## Context

Analysts and agents frequently receive a folder of related exports (supplier price
feeds, stock lists, calculation sheets, lookup tables) with no schema documentation.
Guessing the relationships by hand wastes turns and misses orphan rows. The
`quick-data` MCP tools (DuckDB-backed) profile and query these files without loading
them fully into memory, which is essential for large feeds (100 MB+).

Three distinct jobs, in order:
1. **Profile** — shape, column types, null %, distinct counts, pattern hints.
2. **Relate** — find candidate join keys across files (value overlap / containment).
3. **Audit quality** — missing data, duplicates, empty columns, outliers, join gaps.

## Tooling reference (quick-data MCP)

| Tool | Use |
|------|-----|
| `profile_source` | Raw CSV profiling (types, null %, distinct, pattern hints). Primary step. |
| `validate_quality` | Per-file quality report (missing %, duplicates, empty columns). |
| `query` | Arbitrary DuckDB SQL for join-coverage / overlap checks. |
| `describe` | Quick shape + numeric stats (pandas-based). |
| `find_relations` | *(if available)* dedicated cross-file join-key detector. Prefer over hand-written SQL when present. |
| `detect_outliers` | Numeric outliers (iqr / zscore). |

## Critical gotcha: view naming in `query`

- **One file** → the view is named `t`.
- **Multiple files** → views are `t0`, `t1`, `t2`, … in the order passed.
- Column names with **spaces or special chars** must be double-quoted: `"Preis (exkl. MWSt)"`.

A wrong view name raises `Catalog Error: Table with name t0 does not exist`.

## Workflow

### Step 1 — Profile every file
Call `profile_source` on all paths at once. Read each `column_profiles` entry:
`pattern_hint` of `identifier_or_sku` / `numeric` flags likely key columns;
`null_pct` near 100 means an empty/dead column; `distinct_count` vs `rows` reveals
PK candidates (distinct ≈ rows) or low-cardinality dimensions.

### Step 2 — Find relationships
If `find_relations` exists, call it with the file list. Otherwise do it manually with
`query` using the view-naming rule:

```sql
-- alltron-prices (t0) <-> lagerbestand (t1) on article number
SELECT
  COUNT(*)                                   AS prices_total,
  COUNT(l."Nummer 2")                        AS matched_to_stock,
  COUNT(*) - COUNT(l."Nummer 2")             AS orphans
FROM t0 p
LEFT JOIN t1 l ON p."Artikelnummer 2" = l."Nummer 2";
```

Report `matched / total` as coverage %. A near-100% match = strong join key;
a low match = the smaller side is a subset (1:N) or the key is wrong.

### Step 3 — Audit quality
Call `validate_quality` on all files. Then run targeted checks via `query`:
- **Duplicates:** `SELECT "ARTIKELNR", COUNT(*) FROM t GROUP BY 1 HAVING COUNT(*) > 1`
- **Negative / impossible values:** `WHERE "Preis (exkl. MWSt)" <= 0`
- **Outliers:** `detect_outliers` or `percentile_cont` in SQL.
Flag any column with null_pct ≈ 100% for dropping.

## Correct Patterns

```sql
-- Single file: view is 't'
SELECT COUNT(*) FROM t;

-- Multiple files: t0, t1, ... and quote spaced columns
SELECT COUNT(*) AS n,
       SUM(CASE WHEN "Lagerbestand" > 0 THEN 1 ELSE 0 END) AS in_stock
FROM t0;

-- Join coverage (the relationship signal)
SELECT COUNT(*) - COUNT(l.k) AS orphans
FROM t0 a LEFT JOIN t1 l ON a."Key A" = l."Key B";
```

```text
Report format to the user:
- Per file: rows, cols, key columns, empty/dead columns.
- Relations: "A.col ↔ B.col — coverage 99.8%, direction 1:N".
- Quality: missing %, dup rows, outliers, orphan rows vs join target.
```

## Anti-patterns (DO NOT USE)

```sql
-- WRONG: t0 when only one file was passed → "Table t0 does not exist"
SELECT * FROM t0;

-- WRONG: unquoted column with a space → parse error
SELECT Preis (exkl. MWSt) FROM t0;

-- WRONG: loading a 100 MB feed into pandas just to count nulls —
-- use profile_source / query (DuckDB) instead.
```

- Do not assume column names match across files — verify with value-overlap, not name alone.
- Do not drop duplicates or rows during analysis; only *report* them. Deletion belongs to the import/upsert step.
- Do not treat a low-distinct integer column as a join key without checking overlap — it may be a dimension id, not a foreign key.

## Optional: visualization

When ≥3 files have detected relations and the user wants a picture, delegate rendering
to the `viz-d3` skill: build a graph where nodes = files and edges = detected join keys
(labeled with coverage %), with a clickable modal per node showing column stats from
`profile_source`. Keep `analyze-data-files` focused on detection; let `viz-d3` render.
