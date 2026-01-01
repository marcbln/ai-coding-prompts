# Best Practices

Guidelines and recommendations for effective TDD/BDD workflows.

## General Principles

### 1. Follow the TDD Cycle Strictly

```
Red → Green → Refactor
```

- **Red**: Write failing tests before any implementation
- **Green**: Write minimal code to pass tests
- **Refactor**: Improve code without changing behavior

**Never skip phases or deviate from this order.**

### 2. Write Behavior-Driven Tests

Focus on what the system should do, not how it does it.

**Good:**
```javascript
test("should return user profile when valid ID is provided", () => {
  // Given
  const userId = "123";

  // When
  const profile = getUserProfile(userId);

  // Then
  expect(profile).toBeDefined();
  expect(profile.id).toBe(userId);
});
```

**Avoid:**
```javascript
test("should call database with correct query", () => {
  // Implementation details!
});
```

### 3. Keep Tests Isolated

Each test should be independent and able to run in any order.

**Guidelines:**
- Don't rely on shared state between tests
- Clean up in `afterEach` hooks
- Use fresh data for each test
- Mock external dependencies

### 4. Use Descriptive Test Names

Test names should describe the behavior being tested.

**Good:**
```javascript
test("should return error when user attempts to withdraw more than balance");
test("should increment user login count after successful authentication");
```

**Avoid:**
```javascript
test("testWithdraw");
test("loginTest");
```

### 5. Write Minimal Implementations

In Green Phase, write only the code needed to pass the current test.

**Principles:**
- KISS: Keep It Simple, Stupid
- YAGNI: You Ain't Gonna Need It
- Don't build for future requirements
- One test at a time

### 6. Refactor Relentlessly

Don't let technical debt accumulate. Refactor when code smells appear.

**When to Refactor:**
- After Green Phase completes
- Code duplication spotted
- Long, complex methods
- Unclear variable names
- Violation of SOLID principles

## Workflow-Specific Best Practices

### Orchestrator Workflows

#### When to Use Orchestrator

**Use when:**
- Implementing new features
- Multiple components involved
- Complete feature development
- You're new to TDD

**Avoid when:**
- Quick bug fixes
- Simple changes
- Debugging existing code
- Need fine-grained control

#### Tips for Orchestrator Usage

1. **Provide clear requirements**: Be specific about what you want
2. **Review Gherkin scenarios**: Ensure scenarios accurately reflect requirements
3. **Check test failures**: Verify Red Phase failures are appropriate
4. **Review Green Phase implementations**: Ensure code is minimal
5. **Assess Refactor changes**: Make sure refactoring improves quality

### Manual Workflows

#### When to Use Manual Workflow

**Use when:**
- Need to understand each phase in detail
- Debugging specific issues
- Iterating on a phase
- Learning TDD process

#### Tips for Manual Workflow

1. **Start with Context Bank**: Always understand the codebase first
2. **Write thorough Gherkin scenarios**: Capture all edge cases
3. **Create proper SUT scaffolds**: Define clear contracts
4. **Write meaningful tests**: Focus on behavior, not implementation
5. **Run tests frequently**: After every code change

## Red Phase Best Practices

### Unit Tests

1. **Ensure 100% test failure**: All tests must fail due to missing logic
2. **Mock external dependencies**: Don't test integrations in unit tests
3. **One behavior per test**: Keep tests focused
4. **Use descriptive names**: Make tests self-documenting
5. **Test edge cases**: Don't forget boundary conditions

**Good Test Structure:**
```javascript
describe("Scenario: User Profile Retrieval", () => {
  describe("When user exists", () => {
    test("should return user profile with valid ID", () => {
      // Test happy path
    });

    test("should include all user fields", () => {
      // Test completeness
    });
  });

  describe("When user does not exist", () => {
    test("should return null", () => {
      // Test not found
    });

    test("should log appropriate message", () => {
      // Test error handling
    });
  });
});
```

### Integration Tests

1. **User-First Pattern**: Test from user's perspective
2. **Real Components**: Use real components, mock only external boundaries
3. **Multiple Components**: Ensure tests span at least 2 components
4. **User Outcomes**: Focus on what the user experiences
5. **Business Rules**: Verify business logic across layers

**Good Integration Test:**
```javascript
describe("Scenario: Complete Purchase Flow", () => {
  test("should process payment and confirm order", async () => {
    // Given
    const user = await createTestUser();
    const cart = await addItemsToCart(user.id, items);

    // When
    const result = await completePurchase(user.id);

    // Then
    expect(result.orderStatus).toBe("CONFIRMED");
    expect(result.paymentStatus).toBe("COMPLETED");
    expect(result.orderId).toBeDefined();
  });
});
```

## Green Phase Best Practices

### Unit Test Implementation

1. **Change only failing code**: Don't implement unrelated features
2. **Simplest solution**: Write straightforward code
3. **No premature optimization**: Make it work, then make it right
4. **Follow test requirements**: Code should exactly match test expectations
5. **Don't modify tests**: Tests define requirements, code fulfills them

**Example:**
```javascript
// Test says:
expect(calculateTax(price, taxRate)).toBe(10);

// Implement:
function calculateTax(price, taxRate) {
  return price * taxRate;  // Simple, minimal
}
```

### Integration Test Implementation

1. **Implement components in order**: Start with inner dependencies
2. **Ensure data flow**: Verify data moves correctly across layers
3. **Handle errors**: Implement proper error handling
4. **Test user journeys**: Ensure complete user workflows work
5. **Keep integration minimal**: Don't over-integrate

## Refactor Phase Best Practices

1. **Run tests first**: Ensure all tests pass before refactoring
2. **Small increments**: Refactor in small, safe steps
3. **Run tests after each change**: Catch regressions immediately
4. **Focus on one improvement at a time**: Don't change too much
5. **Maintain behavior**: Tests ensure behavior doesn't change

**Common Refactorings:**
- Extract method
- Rename variable/method
- Replace magic numbers with constants
- Reduce method length
- Eliminate duplication
- Improve variable names

## Gherkin Scenario Best Practices

1. **Focus on behavior**: Describe what, not how
2. **Use user perspective**: Write from user's viewpoint
3. **Include acceptance criteria**: Define measurable outcomes
4. **Consider edge cases**: Document boundary conditions
5. **Keep scenarios independent**: Each scenario should stand alone

**Good Gherkin:**
```gherkin
# Scenario: User Login with Valid Credentials
  Given a user account exists with email "user@example.com"
    And the user's password is "securePassword123"
  
  When the user enters their email and password
    And clicks the login button
  
  Then the user is redirected to the dashboard
    And a welcome message is displayed
    And the user session is created

  ## Acceptance Criteria:
  * User is authenticated within 2 seconds
  * Session token is generated and stored
  * Login attempt is logged
  * Failed login shows generic error

  ## Edge Cases:
  * Invalid email format
  * Incorrect password (3 attempts max)
  * Account locked after failed attempts
  * Concurrent login from different devices
```

## Code Quality Best Practices

### Naming Conventions

- **Classes**: PascalCase (`UserProfileService`)
- **Methods/Functions**: camelCase (`getUserProfile`)
- **Variables**: camelCase (`userId`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_LOGIN_ATTEMPTS`)
- **Test Files**: `*.test.js` or `*.spec.js`
- **Gherkin Files**: `bdd-[feature].md`

### File Organization

```
src/
  components/
    UserProfile/
      UserProfile.tsx
      UserProfile.test.tsx
  services/
    UserService.ts
  types/
    User.ts
  utils/
    helpers.ts
```

### Error Handling

1. **Handle errors gracefully**: Don't let errors propagate to UI
2. **Log appropriately**: Log errors with context
3. **User-friendly messages**: Show understandable errors to users
4. **Don't expose internals**: Don't leak stack traces in production
5. **Test error cases**: Include error scenarios in tests

### Security Best Practices

1. **Never commit secrets**: Keep API keys, passwords out of code
2. **Validate inputs**: Sanitize all user inputs
3. **Use HTTPS**: Always use secure connections
4. **Implement authentication**: Protect sensitive endpoints
5. **Principle of least privilege**: Minimize permissions

## Testing Best Practices

### Test Coverage

- Aim for 80%+ code coverage
- Focus on critical paths
- Don't obsess over 100%
- Coverage is a metric, not a goal

### Test Organization

```javascript
describe("Feature: [Feature Name]", () => {
  describe("Scenario: [Scenario Name]", () => {
    describe("When [condition]", () => {
      test("should [expected outcome]", () => {
        // Test implementation
      });
    });
  });
});
```

### Test Data Management

1. **Use test helpers**: Create reusable test data builders
2. **Clean up after tests**: Use `afterEach` hooks
3. **Isolate test data**: Each test should have its own data
4. **Use meaningful test data**: Make test data readable

**Test Helper Example:**
```javascript
function createTestUser(overrides = {}) {
  return {
    id: "test-user-id",
    email: "test@example.com",
    name: "Test User",
    ...overrides
  };
}
```

## Common Pitfalls to Avoid

### Red Phase Pitfalls

1. **Writing tests that pass**: Ensure tests actually fail
2. **Testing implementation**: Test behavior, not code
3. **Over-mocking**: Only mock external dependencies
4. **Complex test setup**: Keep tests simple
5. **Missing edge cases**: Cover all scenarios

### Green Phase Pitfalls

1. **Over-engineering**: Write minimal code
2. **Writing tests**: Don't modify tests in Green Phase
3. **Adding features**: Only implement what tests require
4. **Skipping validation**: Ensure all test assertions pass
5. **Ignoring tests**: Address all failing tests

### Refactor Phase Pitfalls

1. **Breaking behavior**: Tests should still pass
2. **Too many changes**: Refactor incrementally
3. **Not running tests**: Run tests after each change
4. **Premature optimization**: Focus on clarity first
5. **Skipping refactoring**: Refactor when code smells

## Performance Considerations

1. **Fast tests**: Keep test execution under 10 seconds per suite
2. **Parallel execution**: Run tests in parallel when possible
3. **Test database isolation**: Use in-memory databases for tests
4. **Mock slow dependencies**: Don't test network calls in unit tests
5. **Measure, don't guess**: Profile before optimizing

## Documentation Best Practices

1. **Document decisions**: Use Architecture Decision Records
2. **Keep Gherkin current**: Update scenarios when requirements change
3. **Comment complex logic**: Explain "why", not "what"
4. **Maintain READMEs**: Keep project documentation up to date
5. **Document APIs**: Describe public interfaces clearly

## Continuous Improvement

1. **Regular retrospectives**: Review what worked and what didn't
2. **Update guidelines**: Improve best practices based on experience
3. **Share knowledge**: Document learnings with team
4. **Measure metrics**: Track test coverage, execution time
5. **Stay current**: Keep up with TDD/BDD practices

## Conclusion

Following these best practices will help you:

- Write better, more maintainable tests
- Implement features more confidently
- Catch bugs earlier
- Reduce technical debt
- Improve code quality
- Work more efficiently

Remember: TDD is a discipline, not just a technique. Consistent practice leads to mastery.
