---
name: bug-report
description: Standard structure and format for bug reports (intake). Use when a bug is found or reported and must be characterized before it is fixed — symptom, expected vs actual, reproduction, impact, acceptance criteria, append-only updates log and changelog. A living document created by the investigating agent; conclusions are later promoted to bugfix-report (or analysis-report). NOT for the fix itself (use bugfix-report) or deep analysis (use analysis-report).
---

# Bug Report Guidelines

<!--
Overview: Defines the structure for the intake document about a defect.
Purpose: Capture what is observed, reproducibly, before anyone fixes it.
A bug report is not an analysis and not a fix report: it owns what is observed,
the fix report owns what is concluded. Root cause and fix never appear here as truth.
-->

When you find or receive a defect and need to characterize it before fixing,
write a bug report.

Use this skill when:
- a customer, support, monitoring, or QA reports behavior that is wrong;
- you reproduce a bug and need a durable record of how, before touching code;
- the bug cannot be fixed immediately and must survive a handoff.

Do **not** use it for:
- the fix itself → `bugfix-report`;
- investigation that weighs options / proves a cause → `analysis-report`.

Skip it for obvious bugs fixed within minutes — the `bugfix-report` alone is enough.

## File and frontmatter

Save to `_ai/backlog/reports/{YYMMDD_HHmm}__BUG_REPORT__{kebab-name}.md`.

`severity` and `impact` are **required** — that is exactly where small bugs
silently skip triage.

```yaml
---
filename: "_ai/backlog/reports/{YYMMDD_HHmm}__BUG_REPORT__{kebab-name}.md"
title: "Bug: {short title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
project: "{project-name}"
component: "{module/area}"

reportedBy: "{customer / support / monitoring}"
source: customer | internal | monitoring | qa
customerRef: "{ticket or email ref}"
createdBy: ai-agent | human

severity: critical | high | medium | low
impact: "{who/what is affected, one line}"
status: new | confirmed | investigating | fixed | closed | wontfix | duplicate
resolution: null | fixed | wontfix | duplicate | not-a-bug | deferred
affectedEnvironments: [production]
affectedVersions: "{versions/commits}"
workaround: yes | no | unknown

duplicateOf: "_ai/backlog/reports/{...}__BUG_REPORT__{...}.md"
relatedAnalysis: "_ai/backlog/reports/{...}__ANALYSIS_REPORT__{...}.md"
relatedFix: "_ai/backlog/reports/{...}__BUGFIX_REPORT__{...}.md"
closedAt: YYYY-MM-DD HH:mm

tags: [bug, {tag}, {tag}]
documentType: BUG_REPORT
---
```

Field rules:

- `reportedBy` is the origin (cannot be an agent); `createdBy` is who wrote this file.
- `status` describes the bug's lifecycle; `resolution` is set only when closed.
- `impact` (frontmatter) is the one-line scope; severity justification goes in §5.
- `relatedFix` is filled in at close, pointing at the `BUGFIX_REPORT`.

## Cross-cutting rules

- **No root cause and no fix as truth.** The moment a cause is written as fact this
  is an ANALYSIS_REPORT; once fixed it is a BUGFIX_REPORT.
- Hypotheses are allowed only in the Updates log, each labelled *hypothesis*.
- The core (§1–9) is **mutable** — it always reflects current understanding.
  Every edit to it is recorded in the Changelog (§11).
- The Updates log and Changelog are **append-only**. Never rewrite earlier entries.
- At close, promote conclusions out: cause/options → `analysis-report` if needed,
  applied fix → `bugfix-report`. Then set `relatedFix`, `resolution`, `closedAt`.
- Do not duplicate the fix report's evidence: the fix report links back here
  (`relatedBugReport`) for reproduction and expected/actual.

## Report sections

1. **Summary (internal)** — What is wrong, in one paragraph. Include the failing
   artifact inline (URL, command, request, error).
   *Guard:* no investigation narrative.

2. **Customer-facing description** — Plain-language 2-3 sentences describing the
   user-visible effect, paste-ready for the reply email. No jargon, no file paths.
   *Guard:* it must describe the symptom, never speculate about the cause.

3. **Expected vs Actual** — Table: `aspect | expected | actual`. This is the core
   of the report.
   *Guard:* be concrete — "returns 500" not "doesn't work".

4. **Steps to reproduce + frequency** — Minimal numbered steps; environment and
   fixture/data needed; frequency: always / intermittent / N-of-M.
   *Guard:* minimal repro, not the whole setup ritual.

5. **Impact & severity** — Who/what is affected and how badly; justify the
   `severity` value; state whether a workaround exists.
   *Guard:* this is the bug's present damage, not the fix's regression surface.

6. **Environment / scope** — Versions/commits, hosts, tenants/customers, browsers,
   and data conditions under which it occurs.

7. **Evidence** — Logs, stack traces, screenshots, failing test, HTTP responses.
   Use a table for comparative data.
   *Guard:* link an ANALYSIS_REPORT for the full investigation instead of pasting it.

8. **Acceptance criteria** — What "fixed" must demonstrate. Concrete, checkable
   statements the fix report's verification table will reuse.

9. **Open questions** — Unknowns, and what observation would confirm or reject each.
   *Guard:* questions, not answers; answers go in the Updates log.

10. **Updates log (append-only)** — `timestamp | source | entry`. Sources:
    `customer`, `support`, `ai-investigation`, `developer`, `monitoring`. Customer
    replies, local reproduction observations, and agent notes all land here.
    *Guard:* append only; label hypotheses explicitly.

11. **Changelog (state + core edits)** — `timestamp | field | from → to | why | by`.
    Records status/severity transitions and every edit to §1–9.
    *Guard:* not for observations — those belong in the Updates log.

12. **Links** — `duplicateOf`, `relatedAnalysis`, `relatedFix`, and the customer
    thread reference.
