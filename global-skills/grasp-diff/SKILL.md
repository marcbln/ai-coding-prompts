---
name: grasp-diff
description: Turns a git diff into a structured educational guide with a comprehension quiz, so you build a real mental model of AI-generated changes instead of cognitive debt. Use when reviewing a diff or pull request, after AI wrote or changed code, before approving changes, or when you need to deeply understand what a change does.
argument-hint: "[diff-source] [--quiz N]"
---

# Grasp the Diff: Understand Before You Approve

## Objective

Produce an educational walkthrough of a diff that builds **understanding** (not just verification) before any code is shown. Reading it should leave you with a durable mental model of the change — and the quiz proves it.

## Step 1: Resolve the Diff Source

Determine the diff from `$ARGUMENTS` or fall back to the change in the working tree:

- **`staged`** (or `--staged`) → `git diff --cached`
- **`unstaged`** → `git diff`
- **`head`** (or `--last`) → `git diff HEAD~1`; `--last N` → `git diff HEAD~N`
- **`<branch>` or `<commit>`** → `git diff $(git merge-base <target> HEAD)...HEAD` for the full PR-style diff, or `git diff <target>^ <target>` for a single commit
- **`<pr>` / `#<n>`** → `gh pr diff <n>` (fall back to `gh pr view <n>` if the diff is empty)
- **`<path>`** → restrict the resolved diff to that path
- **No arguments** → first non-empty of: `git diff`, `git diff --cached`, `git diff HEAD~1`; if all empty, tell the user there is nothing to grasp and stop.

If the diff is empty after resolution, stop and say so.

## Step 2: Gather Context (Brief)

Read only what you need to explain *intent*, not to re-verify:
- `git log --oneline -10` and the current branch/status
- Any related commit message or PR description
- The changed files' surrounding code (imports, callers, interfaces) — skim, don't dump

## Step 3: Write the Guide (Intuition Before Details)

Generate exactly four sections in this order. **Never show code before section 3.**

### #1 Background & Context
- Underlying architecture, systems, or algorithms this change touches.
- Domain concepts or prerequisites needed to understand *why* the change exists.

### #2 Intuition & Design Rationale
- The core idea in plain English, **before any code is shown**.
- "Before vs. After" state using an ASCII diagram or step-by-step logic.
- Trade-offs and alternatives that were deliberately avoided, and why.

### #3 Literate Walkthrough
- Group the changes into **logical chunks** — do NOT list files alphabetically.
- For each chunk: purpose → key lines with inline commentary → subtle behaviors, edge cases, side effects.
- Quote only the lines that matter; elide noise with `…`.

### #4 Comprehension Quiz
- 3–5 multiple-choice questions (`--quiz N` overrides the count) testing **mechanics, architecture, and edge cases** — not syntax trivia.
- Four options (A–D) each; the correct answer and a one-paragraph explanation live inside `<details><summary>Answer & Explanation</summary>…</details>` so the reader can self-test first.
- Mark (correct answer shown) and any distractors you expect to be tempting.

## Step 4: Close the Loop

End with a 3-line summary: what changed, why it matters, what to watch out for.

Then offer, in one line each:
- **`grasp-microworld`** — build an interactive state playground of this change if it has runtime state worth playing with
- **`grasp-shared`** — draft a discussion-ready proposal if the team or non-technical stakeholders need to understand it too

Ask the user if they want to save the guide as a markdown file (default: `git diff` derived slug in the repo root or `docs/`).