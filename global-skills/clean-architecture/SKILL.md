---
name: clean-architecture
description: Guide and principles from Robert C. Martin's book "Clean Architecture" for designing modular, maintainable, and testable software systems.
---

# Clean Architecture Summary & Principles

This skill provides the core architectural rules, design principles, and component guidelines from Robert C. Martin's (*Uncle Bob*) book **Clean Architecture: A Craftsman's Guide to Software Structure and Design**.

---

## 1. Core Purpose of Architecture
* **Goal**: Minimize human resources required to build and maintain the software system over its lifetime.
* **The Two Values of Software**:
  1. **Behavior (urgent)**: The software does what the user expects today.
  2. **Structure / Architecture (important)**: The software is easy to change tomorrow.
  * *Rule*: Architecture must take precedence over urgent feature delivery to prevent structural decay.

---

## 2. The Dependency Rule (The Golden Rule)

> **Source code dependencies must point only inward, toward higher-level policies.**

Nothing in an inner circle can know anything at all about something in an outer circle (classes, functions, variables, formats).

```
   +--------------------------------------------------------+
   |  Frameworks & Drivers (Web, DB, UI, External APIs)     |
   |   +--------------------------------------------------+ |
   |   |  Interface Adapters (Controllers, Presenters)    | |
   |   |   +--------------------------------------------+ | |
   |   |   |  Use Cases (Application Business Rules)    | | |
   |   |   |   +--------------------------------------+ | | |
   |   |   |   |  Entities (Enterprise Business Rules) | | | |
   |   |   |   +--------------------------------------+ | | |
   |   |   +--------------------------------------------+ | |
   |   +--------------------------------------------------+ |
   +--------------------------------------------------------+
```

### The Concentric Layers:
1. **Entities (Enterprise Business Rules)**
   * Plain domain objects, encapsulating the highest-level, most general business rules and state.
   * Unaffected by changes in UI, database, or application frameworks.
2. **Use Cases (Application Business Rules)**
   * Orchestrates the flow of data to and from Entities.
   * Pure business workflows (e.g., `CreateOrderUseCase`, `AuthenticateUser`).
   * Accepts plain request models / DTOs; returns plain response models.
3. **Interface Adapters (Controllers, Gateways, Presenters)**
   * Translates data between the format most convenient for Use Cases/Entities and external systems.
   * Includes MVC controllers, Repository implementations, ViewModels, and serialization.
4. **Frameworks & Drivers (Infrastructure / Devices)**
   * Frameworks (Spring, Express, ASP.NET), database tools (ORM, SQL), third-party APIs.
   * Treated strictly as plugins/details to the system.

---

## 3. SOLID Principles at the Architecture Level

* **SRP (Single Responsibility Principle)**: A module should have one, and only one, reason to change (i.e., be responsible to only one actor).
* **OCP (Open-Closed Principle)**: Software entities should be open for extension, but closed for modification (achieved via interfaces and polymorphism).
* **LSP (Liskov Substitution Principle)**: Subtypes must be substitutable for their base types without altering system correctness.
* **ISP (Interface Segregation Principle)**: Clients should not be forced to depend on methods they do not use (keep interfaces focused and thin).
* **DIP (Dependency Inversion Principle)**: High-level modules should not depend on low-level modules; both should depend on abstractions. Details depend on policies.

---

## 4. Component Principles

### Component Cohesion (What belongs inside a component)
* **REP (Reuse/Release Equivalence Principle)**: The granule of reuse is the granule of release. Package code together if it is versioned together.
* **CCP (Common Closure Principle)**: Gather together those things that change at the same time and for the same reasons (SRP at the component level).
* **CRP (Common Reuse Principle)**: Don't force users of a component to depend on things they don't need (ISP at the component level).

### Component Coupling (Relationships between components)
* **ADP (Acyclic Dependencies Principle)**: Allow no cycles in the component dependency graph (must form a Directed Acyclic Graph / DAG).
* **SDP (Stable Dependencies Principle)**: Depend in the direction of stability. A component with many dependents should be stable and hard to change.
* **SAP (Stable Abstractions Principle)**: A component should be as abstract as it is stable. Highly stable components should consist of interfaces/abstract classes.

---

## 5. Key Practical Rules & Guidelines

1. **Defer Decisions**: A good architecture leaves options open as long as possible (choice of database, framework, web server, or deployment model).
2. **Crossing Boundaries**:
   * Cross boundaries using simple, decoupled Data Transfer Objects (DTOs) or basic primitives.
   * Never pass domain Entities directly to UI views or database tables.
   * Use Dependency Inversion (Interfaces / Ports & Adapters) so the flow of control crosses the boundary in the opposite direction of the source code dependency.
3. **Main Component / Composition Root**:
   * The `Main` component is the dirtiest component: it creates factories, instantiates dependencies, configures frameworks, and injects them into the higher-level policies.
   * Main is a plugin to the application.
4. **Testability**:
   * Business logic should be 100% testable without starting a web server, database, or UI framework.

---

## 6. Code Review Checklist for Clean Architecture

- [ ] Does the domain/entity layer have zero imports of external frameworks, libraries, or UI components?
- [ ] Are use cases driving business rules rather than acting as pass-throughs to database ORMs?
- [ ] Do dependencies cross boundaries pointing inwards toward abstractions?
- [ ] Are DB models and API DTOs separated from domain Entities?
- [ ] Can core business use cases be executed and unit-tested in isolation without mocks for the database/UI?
