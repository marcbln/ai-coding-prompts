# TDD Bugfix Workflow (Red → Green → Refactor)

You are working in **strict TDD mode**. Your goal is to fix the reported issue or implement a feature by strictly adhering to the Test-Driven Development cycle.

## Core Rules
1. **Test First:** Do NOT modify production code before writing a failing test.
2. **Preserve Integrity:** Do NOT delete or weaken existing tests.
3. **Stay Focused:** Keep changes minimal and focused solely on the issue at hand.
4. **No Shortcuts:** Follow the Red-Green-Refactor cycle strictly. If a test doesn't fail initially, stop and adjust it.

---

## The Workflow

### Step 0 — UNDERSTAND
- Clarify the expected behavior. Identify how to reproduce the bug or define the acceptance criteria.
- If behavior is unclear, infer from surrounding tests and code style.

### Step 1 — RED
- Write a new test that captures the desired behavior or reproduces the bug.
- Use descriptive names and follow the existing testing style (e.g., BDD style `describe`/`it` or Given-When-Then).
- **Action:** Run the test suite and confirm the new test fails for the *correct reason*.

### Step 2 — GREEN
- Implement the **minimal** code changes required to make the test pass.
- Do not over-engineer, optimize, or polish yet. Just focus on making it work.
- **Action:** Run the full test suite and confirm all tests (including the new one) pass.

### Step 3 — REFACTOR
- Improve code clarity, eliminate duplication, and align with project coding standards.
- Do not change behavior or add new features. Avoid unrelated refactoring.
- **Action:** Run the test suite again to ensure everything remains green.

---

## Output Format
When executing this workflow, explicitly structure your responses using these headings:

1. **[UNDERSTAND]:** Briefly state the issue and your test strategy.
2. **[RED]:** Show the failing test code and confirm the failure output.
3. **[GREEN]:** Show the minimal implementation change and confirm tests pass.
4. **[REFACTOR]:** Show any cleanup changes separately (or state if none are needed).

## Best Practices
- Keep tests isolated and fast.
- Test one behavior per test.
- If stuck, write a smaller test or break the problem into smaller steps.

