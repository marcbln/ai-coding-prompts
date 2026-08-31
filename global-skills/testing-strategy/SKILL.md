---
name: testing-strategy
description: Testing pyramid, test patterns, in-memory test fakes, Testcontainers integration testing, and fixture management for Clean Architecture and Hexagonal Systems.
---

# Testing Strategy & Verification Skill

Guidelines for building fast, reliable, and decoupled automated test suites across domain, application, and infrastructure layers.

---

## 1. The Hexagonal Testing Pyramid

```
           / \
          /   \     E2E / Contract Tests (Few, Slow, Real I/O)
         /-----\
        /       \   Integration Tests (Driven Adapters, DB with Testcontainers)
       /---------\
      /           \ Unit Tests (Application Use Cases with In-Memory Fakes)
     /-------------\
    /               \ Pure Domain Tests (Entities, Value Objects, Zero Mocks)
   -------------------
```

| Layer | Test Type | What to Test | Dependencies / Mocks |
|---|---|---|---|
| **Domain** | Pure Unit | Entities, Value Objects, Domain Services, Invariants | No mocks, pure state assertions. |
| **Application** | Use Case Unit | Use case orchestration, authorization, transactions | Use **In-Memory Fakes** for ports (repositories/gateways). |
| **Infrastructure** | Integration | SQL Repositories, Redis adapters, HTTP Clients | Real databases via **Testcontainers**; mock HTTP via wiremock. |
| **Boundaries** | Contract | API serialization, schema backward compatibility | OpenAPI / Pact / Schema validation. |

---

## 2. In-Memory Fakes vs. Mocking Frameworks
- **The Mocking Anti-Pattern**: Overusing mock frameworks (`when(...)->thenReturn(...)`) couples tests to implementation details and method call order, leading to brittle tests that break during refactoring.
- **Prefer In-Memory Fakes**:
  - Implement driven ports with a fast, thread-safe in-memory map or array.
  - Example: `InMemoryOrderRepository implements OrderRepository`.
  - Application use cases test against the fake, verifying business outcomes rather than method call counts.

```
+---------------------------+       +----------------------------+
|   CreateOrderUseCaseTest  | ----> | InMemoryOrderRepository    |
+---------------------------+       | (Implements driven port)   |
                                    +----------------------------+
```

---

## 3. Test Fixtures: Object Mother & Builder Patterns
Avoid copy-pasting raw JSON or huge constructor calls inside test files.

- **Object Mother Pattern**: Factory providing standard test instances.
  - `OrderMother.createPaidOrder()`, `UserMother.createAdmin()`
- **Test Data Builder**: For tests requiring custom variations:
  ```go
  order := NewOrderBuilder().
      WithCustomer(customerID).
      WithItem(productID, 2, 100).
      WithStatus(StatusPending).
      Build()
  ```

---

## 4. Integration Testing with Testcontainers
- Test database adapters against real PostgreSQL/MySQL instances, not SQLite or in-memory equivalents that behave differently.
- Use **Testcontainers** (in Go, PHP, or Python) to spin up ephemeral Docker containers during the integration test suite.
- Clean database state between test runs using transactions (`BEGIN ... ROLLBACK`) or fast table truncations.

---

## 5. Practical Testing Checklist per Layer

### Domain Layer Tests
- [ ] Are business invariants and validations tested for edge cases (e.g., negative prices, empty strings)?
- [ ] Are value objects verified for equality by value and immutability?
- [ ] Is execution completely free of network, filesystem, and framework imports?

### Application Layer Tests
- [ ] Does each use case test the happy path and each domain error branch?
- [ ] Are driven dependencies supplied via in-memory fakes rather than heavy mocks?
- [ ] Are compensating actions and rollback logic verified on failure?

### Infrastructure Layer Tests
- [ ] Do repository tests assert real SQL queries, constraint violations, and locking semantics?
- [ ] Are API client adapters tested against simulated timeout and HTTP 5xx responses?
