---
name: domain-driven-design
description: Principles, patterns, and architectural guidelines for Domain-Driven Design (DDD). Use this skill when designing domain models, structuring bounded contexts, defining aggregates, or applying tactical and strategic DDD patterns.
---

# Domain-Driven Design (DDD) Skill

## 1. Core Philosophy
Domain-Driven Design (introduced by Eric Evans) tackles complexity in the heart of software by connecting the implementation directly to an evolving model of business concepts.

* **Domain First:** Software design is driven by deep business understanding, not database schemas or framework conventions.
* **Shared Understanding:** Developers and domain experts build software using a common conceptual model.

---

## 2. Strategic Design
Strategic design focuses on large-scale architectural boundaries and the relationships between business domains.

### 2.1 Ubiquitous Language
* A shared, unambiguous language used by both technical teams and domain experts.
* Used consistently in speech, documentation, user stories, class names, method names, and database schemas (within the context).
* If a term is ambiguous across teams, it belongs in different **Bounded Contexts**.

### 2.2 Subdomains
* **Core Domain:** The unique business differentiator providing a competitive advantage. Demands the highest engineering quality.
* **Supporting Domain:** Complements the core domain; custom-built but not the primary differentiator.
* **Generic Domain:** Standard problems with no competitive advantage (e.g., identity management, billing, notifications). Buy or use off-the-shelf solutions when possible.

### 2.3 Bounded Contexts & Context Mapping
* **Bounded Context:** An explicit boundary (often a service or module) within which a domain model and ubiquitous language apply.
* **Context Relationships:**
  * **Shared Kernel:** A shared subset of the domain model and code between two teams.
  * **Customer / Supplier:** Upstream (Supplier) serves downstream (Customer); downstream influences upstream priorities.
  * **Conformist:** Downstream team conforms strictly to the upstream model without translation.
  * **Anti-Corruption Layer (ACL):** A translation layer isolating downstream domain logic from an external/upstream system.
  * **Open Host Service (OHS) / Published Language (PL):** Upstream provides a stable, documented protocol/API (e.g., REST/JSON, Protobuf).
  * **Separate Ways:** No integration; two systems solve needs independently.

---

## 3. Tactical Design (Building Blocks)
Tactical patterns structure the code inside a single Bounded Context.

```
┌────────────────────────────────────────────────────────┐
│                    AGGREGATE ROOT                      │
│                                                        │
│   ┌──────────────┐     ┌──────────────┐     ┌────────┐ │
│   │ Entity       │────▶│ Value Object │     │ Entity │ │
│   └──────────────┘     └──────────────┘     └────────┘ │
└────────────────────────────────────────────────────────┘
```

### 3.1 Entities vs. Value Objects
* **Entity:**
  * Defined by unique **identity**, not attributes (e.g., `User(id=123)`).
  * Has a mutable lifecycle across state changes.
  * Encapsulates state transitions and business rules.
* **Value Object (VO):**
  * Defined solely by its **attributes** (equality by value).
  * **Immutable**: Any modification returns a new instance (e.g., `Money(amount=10, currency="EUR")`, `Address`, `DateRange`).
  * Replaces primitive obsession (avoid raw strings/ints for domain concepts).

### 3.2 Aggregates & Aggregate Roots
* **Aggregate:** A cluster of associated Entities and Value Objects treated as a single transactional unit.
* **Aggregate Root (AR):** The primary Entity through which external objects interact with the aggregate.
* **Rules of Aggregates:**
  1. Protect business invariants across all enclosed objects.
  2. Outside references may only hold a reference to the Aggregate Root (never internal entities).
  3. Reference other Aggregates by **Identity (ID)** only, not direct object references.
  4. Modify one Aggregate per transaction (use eventual consistency across aggregates).

### 3.3 Domain Services
* Stateless operations that orchestrate domain logic that does not naturally belong to a single Entity or Value Object (e.g., `FundTransferService`).
* *Note:* Keep distinct from Application Services (which coordinate use cases, security, and transactions).

### 3.4 Domain Events
* Represents a fact that occurred in the domain in the past (e.g., `OrderPlaced`, `InvoicePaid`).
* Immutable payloads named in **past tense**.
* Used to synchronize other aggregates/contexts via asynchronous messaging (eventual consistency).

### 3.5 Repositories & Factories
* **Repository:** Provides collection-like access to persist and reconstitute **Aggregate Roots** (e.g., `OrderRepository.findById(orderId)`). Do not create repositories for internal entities.
* **Factory:** Encapsulates complex creation logic for aggregates or value objects when direct instantiation is too involved.

---

## 4. Architecture & Layering

### 4.1 Ports & Adapters (Hexagonal / Clean Architecture)
Keep the domain model isolated from I/O, databases, frameworks, and UI:

```
[ UI / API ] ──▶ [ Application Services (Use Cases) ] ──▶ [ Domain Model ]
                             ▲                                    ▲
[ Message Bus ] ─────────────┤                                    │
                                                            (implements)
[ Infrastructure (DB / External APIs) ] ──────────────────────────┘
```

1. **Domain Layer:** Pure domain logic (Entities, Value Objects, Domain Events, Repository Interfaces). No external dependencies.
2. **Application Layer:** Orchestrates use cases, manages transactions, invokes domain objects and repository interfaces.
3. **Infrastructure Layer:** Implements persistence, external APIs, messaging, and database adapters.

---

## 5. Key Heuristics & Anti-Patterns to Avoid

| Anti-Pattern | Recommended Solution |
|---|---|
| **Anemic Domain Model** (Entities with only getters/setters and logic in services) | **Rich Domain Model:** Put business rules, validation, and state mutations inside Entities and Value Objects. |
| **Giant Aggregates** (Whole object graphs locked together) | **Small Aggregates:** Keep aggregates small (often 1-3 entities). Reference by ID and use eventual consistency. |
| **Database-Driven Design** (Designing tables before domain concepts) | **Domain-First:** Model domain behavior first; map persistence to the model, not vice-versa. |
| **Leaking External Models** | Use an **Anti-Corruption Layer (ACL)** to translate external DTOs into domain concepts. |

---

## 6. DDD in a Synchronous Microservices Ecosystem

These sections adapt the book principles to a landscape of **synchronous** (REST/JSON, gRPC) service-to-service microservices **without Event-Driven Architecture**.

### 6.1 One Microservice ≈ One Bounded Context
* The microservice boundary **is** the bounded context boundary. No shared kernel across processes; context maps become API contracts.
* Each microservice owns its database exclusively — never query another service's database directly.
* The ubiquitous language stops at the service boundary: the same business term may (and will) mean different things in different services.

### 6.2 Synchronous Anti-Corruption Layers (ACL)
* When Service A calls Service B over REST/JSON, Service A **must**:
  1. Deserialize B's response into an internal DTO (a plain data structure owned by A).
  2. Map that DTO into A's own domain model inside an ACL adapter.
* **Never let Service B's schema dictate Service A's domain model.** B's field names, units, or nesting are implementation details of B.
* The ACL is a driven port in A's hexagonal architecture: the domain defines the interface, the infrastructure adapter does the translation.
* Treat B's error payloads the same way: translate HTTP error responses into typed domain errors understood by A's use cases.

### 6.3 Consistency Without Events
* Without asynchronous domain events / eventual consistency across services, transactions are **strictly local to each microservice's database**.
* Cross-service workflows require **synchronous orchestration**: an application service (orchestrator) calls downstream services in sequence and manages the workflow state.
* Explicit **compensating actions** are required for partial failures — there is no outbox/event replay to heal inconsistencies automatically.
* Apply the dual-write rule: commit the local transaction first; if the outbound call fails afterward, record a pending-sync state for a background worker (see `microservice-patterns` skill).
