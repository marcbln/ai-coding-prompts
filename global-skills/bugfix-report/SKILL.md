---
name: bugfix-report
description: Standard structure and format for defect repair reports. Use when a bug has been diagnosed and fixed or mitigated and the work needs documenting — root cause, evidence, reproduction, verification, deployment/rollback, blast radius. Use for bugfixes and incidents, NOT for feature work (use implementation-report) or investigation-only work (use analysis-report).
---

# Bugfix Report Guidelines

<!--
Overview: Defines the structure for reports about repairing a defect.
Purpose: Prove a cause, show the fix, and state exactly where it was verified.
An implementation report tracks plan deviations; a bugfix report proves a cause.
This is a distinct documentType, not an IMPLEMENTATION_REPORT.
-->

When you have fixed or mitigated a defect, write a bugfix report.

Use this skill when:
- a bug was diagnosed and repaired (or mitigated) and needs a report;
- a production incident was resolved and needs evidence and a rollback path.

Do **not** use it for:
- feature / migration / docs work → `implementation-report`;
- investigation with no applied fix → `analysis-report`.

## File and frontmatter

Save to `_ai/backlog/reports/{YYMMDD_HHmm}__BUGFIX_REPORT__{kebab-name}.md`.

`severity` and `impact` are **required**. Do not skip them for "small" fixes —
that is exactly where impact gets forgotten.

```yaml
---
filename: "_ai/backlog/reports/{YYMMDD_HHmm}__BUGFIX_REPORT__{kebab-name}.md"
title: "Bugfix: {short title}"
createdAt: YYYY-MM-DD HH:mm
updatedAt: YYYY-MM-DD HH:mm
project: "{project-name}"

severity: critical | high | medium | low
impact: "{who/what was affected, one line}"
status: draft | complete

fixState: implemented | verified | deployed | rolled-back | superseded
environments:
  local: verified | not-run
  staging: pending | verified | failed | n/a
  production: not-deployed | deployed-unverified | verified | rolled-back | n/a

fixType: root-cause | mitigation | data-repair | config | workaround
regressionTest: true | false
deployTarget: "{host, path, or pipeline}"
incident: false            # true enables Appendix A

filesCreated: 0
filesModified: 0
filesDeleted: 0
tags: [bugfix, {tag}, {tag}]
documentType: BUGFIX_REPORT

relatedBugReport: "_ai/backlog/reports/{...}__BUG_REPORT__{...}.md"
relatedAnalysis: "_ai/backlog/reports/{...}__ANALYSIS_REPORT__{...}.md"
relatedPlan: "_ai/backlog/active/{...}__IMPLEMENTATION_PLAN__{...}.md"
---
```

Field rules:

- `status` is **authoring state only**. Never put deployment state in it
  (no `implemented-pending-production`).
- `fixState` describes the fix; `environments` describes where it was proven.
  A fix validated locally is `fixState: verified`, `production: not-deployed`.
- `fixType: mitigation | workaround` signals the cause is still live.
- `relatedAnalysis` / `relatedPlan` are optional links, never duplicated content.

## Cross-cutting rules

- `impact` (frontmatter) is **backward-looking**: who/what the bug already hurt.
- Blast radius (body, section 10) is **forward-looking**: what the fix could break.
  Never restate `impact` under Blast radius.
- Evidence lives inline (section 5); the full investigation lives in the linked
  ANALYSIS_REPORT.
- If a BUG_REPORT exists, link it in `relatedBugReport` and point its
  reproduction / expected-vs-actual instead of duplicating them here. The bug
  report owns intake; this report owns the conclusion.
- Root cause is the defect. The fix is not the root cause — do not blend them.

## Report sections

1. **Summary** — Symptom → where/when → one-clause cause → one-clause fix →
   current state (3-4 sentences). Include the failing artifact inline
   (URL, command, error).
   *Guard:* no evidence tables, no code walkthrough.

2. **Prompt / trigger** — The verbatim prompt, alert, or ticket line that started
   the work.
   *Guard:* do not paraphrase.

3. **Reproduction** — Environment (host, runtime, DB, commit); the smallest exact
   steps/command/URL; **Expected vs Actual**; deterministic or intermittent.
   *Guard:* minimal repro, not the whole local setup ritual.

4. **Root cause** — The defect at `file:line`, the mechanism, and why it produces
   the symptom. Then **Why it escaped**: missing test, skipped step, wrong
   assumption.
   *Guard:* do not describe the patch here.

5. **Evidence** — Log excerpt, row counts, HTTP responses, `file:line` references,
   before/after artifacts. Use a table for comparisons.
   *Guard:* link the ANALYSIS_REPORT instead of re-pasting an investigation.

6. **Fix** — What changed and why this approach; state `fixType` and whether the
   cause or only the symptom was addressed. If mitigation/workaround, say what is
   still live.
   *Guard:* file-by-file detail belongs in section 7.

7. **Files changed** — Created / modified / deleted with one-liners, matching the
   frontmatter counts. Flag production files changed outside the repo.

8. **Verification** — Table: `check | before | after | evidence`. List commands,
   test names, and linters. Explicitly state **what was not verified**.
   *Guard:* "works locally" is not a row — name the check.

9. **Deployment & rollback** — Approval/preconditions, target, commands (dry-run
   first), post-deploy check. **Rollback:** the exact undo — code revert, data
   restore, feature flag. Must mirror the frontmatter `environments`.
   *Guard:* never claim deployed when only validated locally.

10. **Blast radius** — Entry points/paths that share the changed code; other
    products/tenants/versions; what the fix could plausibly break and how that was
    bounded.
    *Guard:* forward-looking regression surface only — do not restate `impact`.

11. **Prevention / follow-ups** — Actionable and owned: regression test added or
    missing, alert, doc reconciliation, guard.
    *Guard:* this is an action list, not a risk list.

12. **Residual risks & explicitly not changed** — Risks remaining after the fix,
    then the scope fence: adjacent changes considered and deliberately left alone
    ("did not patch core").
    *Guard:* "not changed" items are decisions, not apologies.

13. **Links** — `relatedBugReport`, `relatedAnalysis`, `relatedPlan`, upstream
    issue/PR, docs touched.

### Appendix A — Incident timeline (only when `incident: true`)

Table: `timestamp | event | actor/source`, from detected → escalated → mitigated →
fixed → verified. Omit entirely for ordinary fixes.
