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

## 6. Driving vs. Driven Ports (Ports & Adapters)

Clean Architecture's boundary crossing is made concrete by naming *who drives* and *who is driven*:

* **Driving (Primary) Ports** — *initiate* use cases; owned by the application core, implemented by the outside world:
  * HTTP Controllers (Symfony, FastAPI, Gin).
  * CLI commands (`bin/console` / Symfony, `click` / Python, `cobra` / Go).
  * Message/queue consumers, scheduled jobs.
  * The driving port is usually an interface the use case exposes (e.g. `OrderService`), and the controller is an adapter for it.
* **Driven (Secondary) Ports** — *required by* the application core to do its job; the core defines the interface, infrastructure implements it:
  * Repository interfaces (Doctrine, GORM, SQLAlchemy adapters).
  * HTTP Client adapters (calling external microservices).
  * Cache, Mailer, File Storage, Time/Clock.
  * The driven port is an interface **defined in the core** (e.g. `OrderRepository`), and the DB/HTTP adapter lives in infrastructure.

**Rule of thumb**: the port (interface) always belongs to the side that *needs* it. Driving ports sit on the use-case boundary; driven ports sit on the repository/gateway boundary. Dependencies point inward in both cases.

---

## 7. Multi-Language Project Conventions

Concrete directory layouts that realize the dependency rule in the common backend languages:

* **Go**:
  * `internal/domain` — entities, value objects, repository interfaces. Zero external imports.
  * `internal/usecase` (or `internal/application`) — use cases, ports.
  * `internal/adapter/http` — Gin/Echo handlers (driving adapters).
  * `internal/adapter/postgres` (or `.../repository`) — driven adapters.
  * Keep interfaces **next to the consumer**, not the implementer: an interface used by a use case lives in the use case package; the implementation imports it, not vice versa.
* **PHP (Symfony)**:
  * `src/Domain` — entities, value objects, repository **interfaces**. Zero framework imports (no Doctrine annotations, no Symfony components).
  * `src/Application` — use cases / command handlers, port interfaces.
  * `src/Infrastructure` — Doctrine repositories, API clients, Symfony controllers (thin), mailer, cache.
* **Python**:
  * Use **Pydantic models only at the boundaries** (adapters/DTOs, request/response schemas).
  * Keep pure `dataclasses` / domain entities in `domain/` — no framework dependency.
  * FastAPI routers in `adapter/http`, repositories in `adapter/db`, business logic in `application/` + `domain/`.

---

## 8. Microservice Boundary Crossing

When two services of the same ecosystem communicate (REST/JSON, gRPC), the boundary must be crossed deliberately:

* Route every cross-service call through a dedicated **Gateway Adapter** (driven port), never ad-hoc `curl`/`guzzle`/raw HTTP calls scattered through business code.
* The gateway adapter is responsible for: URL/route resolution, auth (tokens/API keys), timeouts, serialization, and error translation into domain terms.
* Deserialize the response into an **internal DTO**, never leak the remote service's raw schema into the domain model (see `domain-driven-design` skill, Synchronous ACLs).
* Each service keeps its own source of truth; a remote call is treated like any other I/O boundary — mockable at the port, testable in isolation.

---

## 9. Code Review Checklist for Clean Architecture

- [ ] Does the domain/entity layer have zero imports of external frameworks, libraries, or UI components?
- [ ] Are use cases driving business rules rather than acting as pass-throughs to database ORMs?
- [ ] Do dependencies cross boundaries pointing inwards toward abstractions?
- [ ] Are DB models and API DTOs separated from domain Entities?
- [ ] Can core business use cases be executed and unit-tested in isolation without mocks for the database/UI?
