---
filename: "_ai/specs/SPEC__<YYMMDD-N>__<kebab-case-title>.md"
title: "[Short Human Readable Title]"
specId: [YYMMDD-N, e.g. 261016-1]
status: Draft
date: [YYYY-MM-DD]
createdAt: [YYYY-MM-DD HH:mm]
updatedAt: [YYYY-MM-DD HH:mm]
priority: [low | medium | high | critical]
estimatedComplexity: [simple | moderate | complex]
tags: [comma, separated, tags]
documentType: SPEC
---

# [Title]

## Objective
[Why does this exist? What should be true after it is built? 1–3 sentences.]

## Scope
- [What is in scope]

## Non-goals
- [What is explicitly out of scope]

## Requirements

### Requirement: [Name]
The system SHALL [specific, testable capability].

#### Scenario: [Success case]
- **WHEN** [action or initial state]
- **THEN** [expected observable outcome]
- **AND** [additional outcome]

#### Scenario: [Error or boundary case]
- **WHEN** [invalid input or boundary condition]
- **THEN** [expected observable outcome]

## Edge Cases
- What happens when [boundary condition]?
- How does the system handle [error scenario]?

## Success Criteria
- [Measurable, technology-agnostic outcome]

## Open Questions
- [NEEDS CLARIFICATION: question]

## References
- [path/to/file.ext:42] — [why it matters]
- [Related SPEC__… / ADR__… / plan file]
