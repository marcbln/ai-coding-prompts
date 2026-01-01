# TDD/BDD Workflows Guide

This document provides detailed explanations of the available TDD/BDD workflows.

## Orchestrated Workflows

### 1. Unit Test TDD Workflow

The orchestrator manages all phases automatically from start to finish.

#### Phases

| Phase | Mode | Purpose | Output |
|-------|------|---------|--------|
| 1 | Context Bank Summarizer | Analyze existing codebase | Codebase summary |
| 2 | Gherkin Generator | Create BDD scenarios | `bdd-[feature].md` files |
| 3 | SUT Scaffolding | Create empty classes/interfaces | Stub implementations |
| 4 | Red Phase | Write failing unit tests | 100% failing tests |
| 5 | Green Phase | Implement minimal code | All tests passing |
| 6 | Refactor Phase | Improve code quality | Clean, maintainable code |
| 7 | Filemap Generator | Document changes | Updated documentation |
| 8 | Context Updater | Update project context | New context bank entries |

#### Usage

```
@tdd-orchestrator "Add user authentication with email and password login"
```

The orchestrator will:
- Break down the feature into logical subtasks
- Delegate each phase to the appropriate specialized mode
- Track progress through all phases
- Synthesize results upon completion

### 2. Integration Test TDD Workflow

Similar to unit test TDD but focuses on integration testing across components.

#### Phases

| Phase | Mode | Purpose | Output |
|-------|------|---------|--------|
| 1 | Context Bank Summarizer | Analyze existing codebase | Codebase summary |
| 2 | Gherkin Generator | Create BDD scenarios | `bdd-[feature].md` files |
| 3 | Integration Red Phase | Write failing integration tests | Tests for user journeys |
| 4 | Integration Green Phase | Implement components | Working integrations |
| 5 | Refactor Phase | Improve code quality | Clean integrations |
| 6 | Filemap Generator | Document changes | Updated documentation |
| 7 | Context Updater | Update project context | New context bank entries |

#### Key Differences from Unit Test TDD

- **No SUT Scaffolding**: Components are created as needed
- **Integration Red Phase**: Tests span multiple components
- **Integration Green Phase**: Implements working integrations
- **User-First Pattern**: Tests actual UI components and user flows

#### Usage

```
@integration-tdd-orchestrator "Implement complete checkout flow with payment processing"
```

## Manual Workflows

### When to Use Manual Workflow

- You need more control over each phase
- You're debugging an issue
- You want to understand each step in detail
- You need to iterate on specific phases
- You're learning the TDD process

### Unit Test TDD Manual Workflow

```bash
# Step 1: Understand existing codebase
@context-bank-summarizer

# Step 2: Create BDD scenarios from requirements
@gherkin-generator

# Step 3: Create empty classes/interfaces
@sut-scaffolding

# Step 4: Write failing unit tests
@tdd-red-phase

# Step 5: Implement minimal code to pass tests
@tdd-green-phase

# Step 6: Refactor for code quality
@tdd-refactor-phase
```

### Integration Test TDD Manual Workflow

```bash
# Step 1: Understand existing codebase
@context-bank-summarizer

# Step 2: Create BDD scenarios from requirements
@gherkin-generator

# Step 3: Write failing integration tests
@tdd-red-phase-integration-test

# Step 4: Implement components to pass tests
@tdd-green-phase-integration-test

# Step 5: Refactor for code quality
@tdd-refactor-phase
```

## Phase Deep Dives

### Red Phase (Unit Tests)

**Goal:** Write 100% failing tests based on Gherkin scenarios

**Guidelines:**
- All tests must fail (no exceptions)
- Tests should fail due to missing business logic, not setup errors
- Mock external dependencies
- One behavior per test
- Use dynamic assertions

**Test Structure:**
```javascript
describe("Scenario: [BDD Title]", () => {
  test("should [expected outcome]", async () => {
    // Given: Set up state
    // When: Perform action
    // Then: Assert outcome (FAILS here)
  });
});
```

### Red Phase (Integration Tests)

**Goal:** Write failing tests for complete user journeys

**Key Principles:**
- User-First Pattern: Test actual UI components
- Include 2+ components in each test
- Mock only at external system boundaries
- Verify user outcomes and business rules

**Integration Validation Checklist:**
- [ ] Test exercises actual UI component users see
- [ ] Test requires 2+ components to work together
- [ ] Test verifies meaningful user goal
- [ ] Breaking any critical component would fail the test
- [ ] Test spans multiple layers (UI + logic + data)

### Green Phase (Unit Tests)

**Goal:** Write minimal code to pass failing tests

**Guidelines:**
- Change only code relevant to failing tests
- Implement straightforward logic
- No side effects
- Smallest possible code change
- Do NOT edit test files

**Priority Order:**
1. User interaction layer
2. Critical state management
3. Data persistence
4. Business rules enforcement
5. System integration points
6. Error handling

### Green Phase (Integration Tests)

**Goal:** Implement components to make integration tests pass

**Differences from Unit Test Green Phase:**
- May create multiple files/components
- Implement real integrations between components
- Handle data flow across layers
- Ensure user journeys work end-to-end

### Refactor Phase

**Goal:** Improve code quality without changing behavior

**Guidelines:**
- Improve readability and clarity
- Eliminate code smells
- Implement architectural adjustments
- Improve performance
- Run tests after each change
- All tests must still pass

**Code Quality Principles:**
- KISS: Keep It Simple, Stupid
- DRY: Don't Repeat Yourself
- YAGNI: You Ain't Gonna Need It
- Single Responsibility Principle
- Testability

## Workflow Comparison

| Aspect | Orchestrated | Manual |
|--------|-------------|--------|
| **Effort** | One invocation | Multiple invocations |
| **Control** | Orchestrator manages all | You manage each phase |
| **Flexibility** | Fixed sequence | Skip phases, iterate freely |
| **Learning** | Less visible | See each step in detail |
| **Best For** | New features, complete workflows | Quick fixes, debugging, learning |

## Common Workflows

### New Feature Implementation

Use orchestrated workflow for complete feature development.

```bash
@tdd-orchestrator "Add user profile management with avatar upload"
```

### Bug Fix

Use manual workflow, starting directly at the appropriate phase.

```bash
@context-bank-summarizer  # Understand the codebase
@tdd-red-phase            # Write failing test for bug
@tdd-green-phase          # Fix the bug
@tdd-refactor-phase       # Clean up if needed
```

### Refactoring Existing Code

Skip red/green phases, focus on refactor.

```bash
@context-bank-summarizer  # Understand codebase
@tdd-refactor-phase       # Refactor with existing tests
```

### Adding Tests to Legacy Code

Use red phase only to add tests, then implement.

```bash
@context-bank-summarizer  # Understand codebase
@tdd-red-phase            # Write tests for existing code
```

## Troubleshooting

### Tests Don't Fail in Red Phase

- Check that SUT scaffolding created empty implementations
- Verify no business logic exists in stub files
- Ensure test assertions will fail with stubs

### Tests Don't Pass in Green Phase

- Review test error messages
- Check for missing implementations
- Verify test setup and data
- Run tests individually to isolate issues

### Tests Fail After Refactor

- Revert the refactor
- Refactor in smaller increments
- Run tests after each change
- Check for accidental behavior changes

### Integration Tests Are Too Brittle

- Mock at proper boundaries
- Reduce test complexity
- Focus on user outcomes, not implementation details
- Use test helpers for common setup

## Best Practices

1. **Start with Orchestrator**: Use orchestrated workflow first, switch to manual if needed
2. **Write Tests First**: Always follow Red-Green-Refactor order
3. **Keep Tests Small**: One behavior per test
4. **Use Descriptive Names**: Test names should describe the behavior
5. **Run Tests Frequently**: After every code change
6. **Refactor Relentlessly**: Keep code clean and maintainable
7. **Document Decisions**: Use Gherkin scenarios as living documentation
8. **Review Gherkin**: Ensure scenarios accurately represent requirements
