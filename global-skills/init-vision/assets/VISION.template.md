# [Project Name] — Project Charter & Vision

**License**: [License] · **Status**: [e.g., Pre-1.0 (breaking changes permitted)]
**Stack**: [Primary language/framework, target environments, runtime constraints]

## 🎯 PRODUCT VISION

[1-2 punchy paragraphs defining what the project replaces, why it exists, and who it serves.]

**Prime directives** (in strict priority order; when they conflict, the higher one wins):

1. **[Directive 1 Name]**: [Definition and concrete trade-off stance].
2. **[Directive 2 Name]**: [Definition and concrete trade-off stance].
3. **[Directive 3 Name]**: [Definition and concrete trade-off stance].
4. **[Directive 4 Name]**: [Definition and concrete trade-off stance].

## 🚫 NON-GOALS

- **[Non-Goal 1]** — [Why it's out of scope and what dedicated tool handles it instead].
- **[Non-Goal 2]** — [Why it's out of scope and what dedicated tool handles it instead].
- **[Non-Goal 3]** — [Why it's out of scope and what dedicated tool handles it instead].

## 🧭 INVARIANTS (violating any of these is a bug, regardless of what a test says)

- **[Invariant 1 — Crash Safety / State]**: [e.g., Unclean shutdown never corrupts state; in-flight tasks marked interrupted].
- **[Invariant 2 — Network / Offline Policy]**: [e.g., Core features require zero internet access].
- **[Invariant 3 — Concurrency & Single Writer]**: [e.g., Exactly one manager goroutine/thread owns task lifecycle].
- **[Invariant 4 — Source of Truth]**: [e.g., Disk configuration is immutable from the web UI/API].

## 🔐 TRUST & SECURITY MODEL

- [Process execution privileges, untrusted data boundaries, secret persistence rules].

## 🧠 DECISION HEURISTICS (use when the spec is silent)

1. [Litmus test question 1, e.g., "Does this help one operator on one machine?"]
2. [Litmus test question 2, e.g., "Does it make failures more visible?"]
3. [Litmus test question 3, e.g., "Does it add an external runtime dependency?"]

## 🏗 ARCHITECTURE & BOUNDARIES

- [Directional dependency rules: A may import B, but B never imports A].
- [Subsystem responsibilities and state ownership boundaries].

## 🤖 AGENT & VERIFICATION RULES

1. **Validation**: `[single command]` is the only validation command required before finishing any session.
2. **Schema & Config**: [Rules around breaking changes and schema sync].
3. **Bug-first policy**: A bug fix is not complete without a test that reproduces the failure first.
