---
name: tdd-feature
description: "You are working in **strict TDD mode**. Your goal is to implement a new feature by strictly adhering to the Test-Driv..."
---

# TDD Feature Workflow (Red → Green → Refactor)

You are working in **strict TDD mode**. Your goal is to implement a new feature by strictly adhering to the Test-Driven Development cycle, building the functionality incrementally.

## Core Rules
1. **Test First:** Do NOT write new production code before writing a failing test that defines the new behavior.
2. **Incremental Design:** Build the feature in small, vertical slices. Do not try to write tests for the entire feature at once.
3. **Preserve Integrity:** Ensure your new tests and code do not break existing functionality. 
4. **No Shortcuts:** Follow the Red-Green-Refactor cycle strictly. If a test doesn't fail initially, your test is flawed or the behavior already exists.

---

## The Workflow

### Step 0 — UNDERSTAND & PLAN
- Clarify the expected behavior and acceptance criteria for the new feature.
- Break the feature down into small, logical, and testable increments (e.g., "handle empty state", "handle valid input", "handle edge cases").
- Decide on the API or interface design before writing the test.

### Step 1 — RED (Write the Test)
- Write a new test for the *first (or next) small increment* of the feature.
- Use descriptive names and follow the existing testing style (e.g., BDD style `describe`/`it` or Given-When-Then).
- **Action:** Run the test suite and confirm the new test fails for the *correct reason* (e.g., missing method, unexpected return value).

### Step 2 — GREEN (Make it Pass)
- Implement the **minimal** code changes required to make the failing test pass.
- Do not over-engineer, optimize, or build ahead of the tests. If you think of another case, add it to your plan for the next loop.
- **Action:** Run the full test suite and confirm all tests pass.

### Step 3 — REFACTOR (Make it Better)
- Improve code clarity, eliminate duplication, and integrate the new code cleanly with the existing architecture.
- Do not add new behavior during this step. 
- **Action:** Run the test suite again to ensure everything remains green.
- **Loop:** Repeat Steps 1-3 until all acceptance criteria for the feature are met.

---

## Output Format
When executing this workflow, explicitly structure your responses using these headings:

1. **[UNDERSTAND]:** Briefly state the feature increment you are tackling and your test strategy.
2. **[RED]:** Show the new failing test code and confirm the failure output.
3. **[GREEN]:** Show the minimal implementation needed to pass the test.
4. **[REFACTOR]:** Show any cleanup or structural changes (or state if none are needed).

*(Note: If the feature requires multiple cycles, output these four steps for each increment).*

## Best Practices
- **Baby Steps:** If a feature is complex, start with the simplest degenerate case (e.g., returning an empty list, validating bad input).
- **YAGNI (You Aren't Gonna Need It):** Only implement what the current test demands.
- **Keep Tests Fast:** The TDD cycle should be rapid. Keep the test feedback loop as short as possible.
