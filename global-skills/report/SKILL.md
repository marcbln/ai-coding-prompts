---
name: report
description: Generate the right AI report for this session and open it in docdeck. Routes to bug-report, bugfix-report, analysis-report, or implementation-report based on what happened, then prints a short coverage summary. Use when asked to write a report, summarise what the AI did, or run /report. Force a type with /report impl|bug|fix|analysis.
---

# Report (Router)

One entry point that picks the correct report skill, writes the report, tells the
human what is thin, and opens it in docdeck.

Use it when:
- the human says "write a report", "summarize what you did", or runs `/report`;
- a session is ending and its outcome must be captured as a report.

Do **not** use it for a formal report with no desktop (CI, subagents): load the
leaf skill directly.

## 1. Pick the type

First match wins:

1. `bugfix-report` — a cause is proven and a fix/mitigation was applied.
2. `bug-report` — a defect is characterized but not fixed (intake/handoff).
3. `implementation-report` — feature/refactor/migration/docs delivered, no defect.
4. `analysis-report` — investigation/options/audit/research, nothing delivered.

An explicit token in `$ARGUMENTS` overrides inference:

| token | skill |
| --- | --- |
| `impl` | `implementation-report` |
| `bug` | `bug-report` |
| `fix` | `bugfix-report` |
| `analysis` | `analysis-report` |

If the forced type's prerequisites are not met (e.g. `/report fix` with no proven
cause), do not write a hollow report: state what is missing, propose the fallback,
and wait for the human.

Mixed session: write the highest-precedence report and link the rest in its Links
section. Never write several documents for one `/report`.

## 2. Reuse scan

Search `_ai/backlog/reports/` for a report belonging to this work (same topic, same
session date, or referenced in the conversation).

- Never create a second report of the same type for the same work — update the
  existing one and bump `updatedAt`.
- A `BUG_REPORT` exists and a fix was applied: write the `BUGFIX_REPORT` with
  `relatedBugReport`, then set the bug report's `relatedFix`, `resolution`,
  `closedAt`, and `status: closed`.

## 3. Write

Load the chosen leaf skill and obey it exactly: path, frontmatter, required
fields, sections, and guards.

- Do not weaken a guard to fill a section.
- Do not invent evidence, verification, severity, or impact.
- Omit an optional section only when it has no material, and say why in the
  feedback block.

## 4. Feedback (chat only)

Print a compact block after writing. Never embed it in the report file — it is the
few words said while handing over the paperwork.

```text
report: <path>  (type: <type>, inferred|forced)
filled:   <frontmatter derived here: timestamps, project, files* counts, cross-links>
inferred: <judged values to eyeball: severity, impact, why this type>
missing:  <expected material absent from the session: verification, evidence, rollback, test>
omitted:  <optional sections skipped, with reason>
open:     <unanswered questions and who must answer>
```

Rules:

- `missing` is honest, not an error. Never fabricate to clear a line.
- Compute `files*` from git when available; otherwise mark the counts as missing.
- Omit an empty line; keep the whole block to a handful of lines.

## 5. Open

Follow the `docdeck` skill: confirm the file exists, resolve its absolute path, run
`docdeck <abs path>`, and treat exit status 0 as success. Do not background, poll,
or read the document back.

Order: infer → reuse scan → load leaf → write → feedback → docdeck.
