# Functional Specification: [Feature / Plugin Name]

> Source: [meeting date, transcript, ticket, or "reverse-engineered from <area>"]
> Status: Draft — pending clarification items below

## 1. Problem Statement & Goals

- **Context:** Why does this exist? What problem does it solve, and for whom?
- **Goals:** Measurable outcomes and business value.
- **Out of Scope:** What this feature explicitly will NOT do (prevents scope creep).

## 2. Actors & User Journeys

- **Actor:** [Role — e.g. Guest customer, B2B buyer, Admin, System/cron]
  - **Journey:** Trigger → steps → resolution, in the actor's terms.

## 3. Functional Requirements

- **FR-01: [Requirement title]**
  - The system MUST [observable behavior].
  - Constraints: [limits, formats, permissions, one-per-order, etc.]

- **FR-02: [Requirement title]**
  - The system MUST [observable behavior].

## 4. Assumed Defaults

| # | Assumption | Basis | Confirm? |
| :- | :--- | :--- | :--- |
| A1 | [assumed behavior] | [why this is the safe default] | [ ] |

## 5. Edge Cases & Error Handling

- Third-party/network timeout or downtime → [fallback, retry, message].
- Missing, invalid, or conflicting input → [validation, rejected state].
- State conflict (e.g. acting on an already-completed order) → [behavior].
- Boundary values (zero, one, maximum) → [behavior].

## 6. Acceptance Criteria (BDD / Gherkin)

```gherkin
Scenario: [Successful core flow]
  Given [precondition]
  When [trigger action]
  Then [expected result]

Scenario: [Failure or boundary condition]
  Given [precondition]
  When [error condition]
  Then [expected fallback or validation message]
```

## 7. Open Questions & Risks

- [NEEDS CLARIFICATION: question] *(default if unanswered: …)*
- Risk: [business or technical uncertainty, and its blast radius]

## 8. References

- Source notes: [path or link]
- Related specs / ADRs / backlog items: [paths]
