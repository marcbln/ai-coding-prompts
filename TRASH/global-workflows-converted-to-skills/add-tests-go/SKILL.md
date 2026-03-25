---
name: add-tests-go
description: "You are an expert Go developer. Your task is to add comprehensive tests to this Go project."
---

You are an expert Go developer. Your task is to add comprehensive tests to this Go project.

## Instructions

1. Analyze the existing code structure and understand what each package/function does
2. For each .go file (excluding existing _test.go files), create a corresponding _test.go file
3. Follow these testing conventions:
   - Use table-driven tests for functions with multiple input/output cases
   - Use t.Run() for subtests with descriptive names
   - Test both happy paths and edge cases (nil inputs, empty strings, boundary values, errors)
   - Mock external dependencies (DB, HTTP, filesystem) — do not make real calls in tests
   - Prefer testify's assert/require packages for assertions

## Test quality checklist per function:
- At least one happy path test
- At least one error/failure path test
- Edge cases (zero values, empty, nil, max boundary)
- Table-driven where there are 3+ similar cases

## Naming conventions:
- Test functions: TestFunctionName_Scenario (e.g. TestGetUser_NotFound)
- Table-driven test cases: use a `name` field and pass it to t.Run()

## Output rules:
- Only create or edit _test.go files — never modify production code
- Ensure all tests pass with `go test ./...`
- Add a // TODO comment for any function that is too complex to test without 
  a larger refactor (e.g. missing dependency injection)

## Documentation
- Update the README with instructions how to run tests.
