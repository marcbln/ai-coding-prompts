---
name: grasp-quiz
description: Builds a self-contained interactive HTML quiz that teaches a concept in existing code — plain-English explainer plus annotated real-code snippets in Learn mode, then code-anchored multiple-choice questions with instant feedback and scoring in Quiz mode. Use when you want to actually learn a codebase, class, or feature you don't fully understand yet (e.g. "I want to understand this plugin") — the standalone entry point of the grasp-* family.
argument-hint: "[code-path] [concept] [--questions N] [--no-open]"
---

# Grasp the Quiz: Learning Code by Self-Testing

## Objective

Produce a single-file interactive HTML quiz that turns **existing code you want to understand** into an active learning session: *Learn mode* teaches each concept with plain-English explanation and annotated real code, *Quiz mode* proves you understood it via code-anchored multiple-choice questions. The artifact is disposable teaching material, never production code.

## Step 1: Resolve the Target and Propose Concepts

Determine the code to learn, in priority order:

- **`<code-path>`** — a file, class, directory, or plugin root to analyze
- **`<concept>`** — optionally narrow the focus to one concept (e.g. `synonym-expansion`); skip the proposal step and cover it directly
- **Nothing given** — inspect the working tree and propose the most instructive files

Then explore the code *for understanding* (entry points, data flow, callers, interfaces) and propose **3–5 candidate concepts** — the pieces someone must understand to truly know this code (e.g. for a search plugin: "query-building pipeline", "storefront overlay JS", "synonym expansion", "result ranking"). Present them as a numbered list, each with a one-liner, and let the user pick which to include (or "all"). If a single concept was passed, use it.

## Step 2: Write Teach-then-Test Content

For each selected concept produce exactly two parts:

### Teach block (Learn mode)
- 150–250 words of plain-English explanation: **intuition first**, then mechanics, then edge cases.
- One annotated real-code snippet (or 2–3 short ones) — key lines quoted, noise elided with `…`, every reference as `file:line`.

### Quiz block (Quiz mode)
- 4 multiple-choice questions by default (`--questions N` overrides) testing **mechanics, architecture, and edge cases** — not syntax trivia.
- **Every question is code-anchored:** show a short snippet or an exact `file:line` reference as the question's context.
- Four options (A–D) each; correct answer + one-paragraph explanation (stored in the HTML data, revealed only after answering).

## Step 3: Build the HTML

Single self-contained `.html` — **vanilla JS/CSS only, no CDN, no external deps**, works offline. Requirements:

1. **Two modes via tabs:** `Learn` (all teach blocks, in selected order) and `Quiz` (all questions).
2. **Quiz mechanics:** click an answer → instant right/wrong highlight, explanation revealed, progress indicator, running score, final score screen with retry button.
3. **Code anchoring:** every snippet shows its `file:line`; make them collapsible/expandable where long.
4. Clean, readable styling consistent with the grasp-* family of artifacts; dark-friendly.
5. Title: `Quiz: <topic slug>`; a short intro line stating what codebase/concepts it covers.

## Step 4: Output and Hand Off

- Write to `/home/marc/devel/ai-generated-quizzes/<topic-slug>/<topic-slug>-quiz.html` (create the folder if missing) — a sibling folder of `ai-generated-visualizations`, mirroring its one-folder-per-topic convention.
- Open it with `xdg-open` unless `--no-open` was passed.
- Re-read the artifact once against the real code and correct any wrong facts or `file:line` references.
- Confirm the path, then offer, in one line each:
  - **`grasp-diff`** — structured markdown walkthrough if you also want prose deep-dive
  - **`grasp-microworld`** — interactive state playground of the trickiest piece
  - **`grasp-shared`** — discussion-ready proposal for team understanding
