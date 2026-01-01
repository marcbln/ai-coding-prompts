# TDD/BDD Workflows Documentation

Welcome to the TDD/BDD (Test-Driven Development / Behavior-Driven Development) workflows documentation. This collection of AI coding modes provides structured workflows for implementing features using TDD and BDD principles.

## Quick Start

### For New Features (Recommended)

Use the orchestrator for automated workflow management:

```bash
# Unit Test TDD
@tdd-orchestrator "Add user authentication feature"

# Integration Test TDD
@integration-tdd-orchestrator "Add shopping cart checkout flow"
```

### For Manual Control

Invoke modes sequentially:

```bash
@context-bank-summarizer
@gherkin-generator
@sut-scaffolding  # Unit tests only
@tdd-red-phase
@tdd-green-phase
@tdd-refactor-phase
```

## Workflow Overview

### Unit Test TDD Workflow

```
Context Analysis → Gherkin Scenarios → SUT Scaffolding → Red Phase → Green Phase → Refactor
```

- **Red Phase**: Write failing tests (100% must fail)
- **Green Phase**: Write minimal code to pass tests
- **Refactor Phase**: Improve code without changing behavior

### Integration Test TDD Workflow

```
Context Analysis → Gherkin Scenarios → Integration Red Phase → Integration Green Phase → Refactor
```

- Tests complete user journeys across multiple components
- Mocks only at external system boundaries
- Focuses on user outcomes and business rules

## Documentation Files

- [Workflows Guide](workflows.md) - Detailed workflow explanations
- [Modes Reference](modes-reference.md) - Complete mode documentation
- [Best Practices](best-practices.md) - Guidelines and recommendations

## Core Principles

1. **TDD Cycle**: Red → Green → Refactor
2. **BDD Focus**: Behavior over implementation
3. **Test Isolation**: Each test is independent
4. **Minimal Implementation**: YAGNI (You Ain't Gonna Need It)
5. **Continuous Testing**: Run tests after every change

## Categories

- **🤖 Orchestration** - Workflow coordination modes
- **🤓 Analysis** - Code analysis and review modes
- **🏛️ Design** - Design and specification modes
- **🔴🟢🔄 Implementation** - Development and testing modes
- **📚 Documentation** - Documentation generation modes
- **⚖️ Utilities** - Utility and helper modes
