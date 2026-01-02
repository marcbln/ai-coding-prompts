# AI Agent Guidelines

This repository provides a Roo Code-optimized AI-assisted development starter kit with structured templates and workflows. All tool definitions in `_ai/tools/` use frontmatter metadata (description, alwaysApply) and XML-tagged prompts designed for Roo Code's custom tool system.

## Build/Lint/Test Commands

This is a documentation template repository with no executable code. When implementing actual projects:

- **Single test**: Language-specific (e.g., `pytest tests/test_feature.py::test_specific_case`, `npm test -- --testNamePattern="testSpecific"`)
- **All tests**: `npm test`, `pytest`, `cargo test`, etc.
- **Linting**: `npm run lint`, `eslint .`, `ruff check .`, etc.
- **Type checking**: `npm run typecheck`, `tsc --noEmit`, `mypy .`, etc.
- **Build**: `npm run build`, `cargo build`, `go build`, etc.

Check project-specific configuration files for exact commands.

## Code Style Guidelines

### Core Philosophy: Contract-First Feature Fortress

Each feature is a fortress with clear contracts governing all interactions:
- **Walls** = Clear boundaries between features
- **Gates** = Well-defined interfaces with validation
- **Guards** = Error handling and input sanitization
- **Keep** = Core business logic protected inside
- **Contracts** = Explicit agreements about what goes in/out

### Imports and Organization

- Follow existing import organization patterns in the codebase
- Group imports: external libraries, internal modules, relative imports
- No cross-feature imports - use dependency injection or events
- Make all dependencies explicit and injectable/mockable

### Naming Conventions

- Function names should read like sentences describing what they do
- Keep variable scope as close to usage as possible
- Extract magic numbers to named constants with explanatory comments
- Use descriptive names that reveal intent

### Types and Validation

- Define contracts before implementation
- Use runtime validation (Zod, io-ts) at boundaries - never trust external data
- Wrap external calls in Result/Either types for error handling
- Create explicit error types: ValidationError, NetworkError, BusinessLogicError
- Fail fast and visibly when contracts are violated

### Error Handling

- At boundaries: Always validate and sanitize inputs
- Handle async operations: network failures, timeouts, partial failures
- User feedback: Provide actionable error messages, not technical details
- Surface problems immediately rather than letting them cascade silently
- No direct database access across features - go through service layer

### Architectural Principles

#### Single Responsibility
Each vertical slice owns exactly one business capability and its complete stack (UI → Logic → Data)

#### Security by Default
Every boundary is a potential attack vector. Validate, sanitize, and authenticate at every gate.

#### Composition over Configuration
Build with small, focused pieces that combine cleanly rather than large configurable components.

#### Explicit over Implicit
Make dependencies, side effects, and data flows obvious in the code structure.

### Inter-Fortress Communication

**Preferred: Events/Messages**
```typescript
eventBus.emit('user.authenticated', { userId, timestamp })
eventBus.on('user.authenticated', (event) => {
  analytics.track('login', event)
})
```

**Acceptable: Service Interfaces**
```typescript
interface NotificationService {
  sendWelcomeEmail(userId: string): Promise<Result<void, EmailError>>
}
```

**Avoid: Direct Coupling** - Features should not directly access other feature internals

### Complexity Triggers

Stop and refactor when:
- Functions: >30 lines, >5 branches, >3 nesting levels, >4 parameters
- Components: >8 props, >5 local state, >3 useEffect hooks
- Architecture: Circular imports, >3 feature dependencies, logic in >2 places

### Testing Workflow (TDD)

1. **Red Phase**: Write failing tests
2. **Green Phase**: Make tests pass
3. **Refactor**: Improve code while maintaining tests
4. **Code Review**: Follow hybrid code review process
5. **Update Docs**: Filemap, changelog, memory, roadmap

### Quality Checkpoints

Before committing:
- [ ] All inputs validated with runtime checks
- [ ] All outputs properly typed and documented
- [ ] Error cases handled with specific error types
- [ ] No direct access to other feature internals
- [ ] Feature can be tested in isolation
- [ ] User inputs sanitized and validated
- [ ] No unnecessary re-renders or recomputations
- [ ] Code reads like well-structured prose

### Performance Consciousness

Consider performance implications:
- Before loops: batch or memoize operations
- Before API calls: cache or deduplicate data
- Before re-renders: verify dependencies are properly memoized
- Every operation has a cost

### Prevention Heuristics

- Before writing logic: define inputs, outputs, edge cases
- Before async operations: plan error scenarios and timeout handling
- Before state changes: consider race conditions and rollback strategies
- Before copying code: extract shared logic to utilities
- Before adding state: consider if it can be derived or computed

### Best Practices

- Keep internals private - only expose what's necessary
- Design for replaceability - any fortress should be swappable
- Shared utilities only, no shared business logic
- Maintain backward compatibility with clear migration paths
- Version breaking changes explicitly

This guide evolves with the codebase. Prevention is cheaper than cure, especially for solo developers who wear all the hats.
