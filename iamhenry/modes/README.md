# Custom Modes

This directory contains all custom modes organized by category.

## Directory Structure

```
modes/
├── orchestration/     # Workflow coordination modes
├── analysis/          # Code analysis and review modes
├── design/            # Design and specification modes
├── implementation/    # Development and testing modes
├── documentation/     # Documentation generation modes
└── utilities/         # Utility and helper modes
```

## Available Modes

### Orchestration
- **tdd-orchestrator** - Main TDD workflow coordinator
- **integration-tdd-orchestrator** - Integration test workflow coordinator

### Analysis
- **context-bank-summarizer** - Analyzes codebase structure
- **security-auditor** - Security vulnerability scanner
- **code-reviewer** - Code quality reviewer

### Design
- **gherkin-generator** - BDD scenario generator
- **architect-mode** - Architecture designer

### Implementation
- **sut-scaffolding** - System Under Test scaffolding
- **tdd-red-phase** - Unit test writer (failing)
- **tdd-green-phase** - Minimal implementation
- **tdd-refactor-phase** - Code improvement
- **tdd-red-phase-integration-test** - Integration test writer
- **tdd-green-phase-integration-test** - Integration implementation

### Documentation
- **filemap-generator** - File documentation generator
- **context-updater** - Context bank updater
- **chat-summarizer** - Chat thread summarizer

### Utilities
- **debate-proponent** - Debate argument supporter
- **debate-opponent** - Debate counterargument
- **debate-judge** - Debate moderator

## Usage

Each mode file contains:
- YAML frontmatter with metadata
- XML-tagged sections for structure
- Detailed instructions and guidelines
