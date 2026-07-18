---
name: check-architecture
description: Analyzes the codebase structure and imports/namespaces (mainly PHP or Python) against Clean Architecture, SOLID, and DDD principles. Use when asked to evaluate architecture quality, detect framework coupling, or plan a refactoring toward cleaner boundaries.
---

# Skill: Codebase Architecture Evaluation & Improvement (check-architecture)

When the user triggers this skill, you must perform a systematic architectural audit of their codebase (with a primary focus on PHP or Python, but extensible to any language). Your goal is to evaluate code coupling, testability, domain isolation, and boundary protection, and present a professional, highly readable report.

## 1. Analysis Workflow

Follow these steps before writing your final evaluation:

1. **Discover & Map Tech Stack:** 
   * Identify the language and primary framework (e.g., Python with Django, FastAPI, or Flask; PHP with Laravel or Symfony).
   * Note standard structural conventions for these frameworks (e.g., `app/`, `src/`, `domain/`, `controllers/`, `views/`).

2. **Establish the Dependency Graph:**
   * Scan directories and look for the direction of imports (`import` / `from` in Python; `use` in PHP).
   * Determine if high-level policy/business logic files are importing low-level details (e.g., direct DB connections, ORM models, HTTP libraries, or framework-specific controllers/request objects).

3. **Identify Architectural Violations:**
   * **Dependency Inversion Principle (DIP) Violations:** Is the domain layer directly calling external APIs, ORMs, or framework classes without going through interfaces/abstractions?
   * **Single Responsibility Principle (SRP) Violations:** Are controllers doing database queries? Are DB models handling complex, multi-entity business rules?
   * **Framework Bleeding:** Are UI/web representations or HTTP request objects being passed deep into the business logic?

---

## 2. Language-Specific Inspection Guidelines

### For Python Projects
* **The "Django Model" Trap:** Check if business rules are heavily bound to Django ORM Models. Search for fat models handling business policies that should be in pure Python use cases.
* **Lack of Abstractions:** Check if services directly instantiate concrete clients (e.g., `boto3.client('s3')` inside a service class). They should instead use Abstract Base Classes (`abc.ABC`) to represent port/gateways.
* **FastAPI Router Leaks:** Look for business logic residing directly inside route functions. Look for database sessions (`Session = Depends(get_db)`) being passed directly into core domain logic.

### For PHP Projects
* **Laravel "Fat Controllers" or Active Record Bleed:** Look for raw Eloquent queries (`User::where(...)->get()`) written directly inside Controllers or Jobs.
* **Inadequate Decoupling:** Check if Controllers depend on concrete class implementations instead of interfaces bound in the Service Container.
* **Modern PHP Features:** Ensure PHP 8.x typed properties, constructor property promotion, and readonly classes are used correctly to enforce immutability in Data Transfer Objects (DTOs) and Domain Entities.

---

## 3. Output Report Structure

Your response must be structured exactly as follows, keeping the tone objective, constructive, and humble:

### 1. Executive Summary
Provide a high-level table evaluating the codebase across three main pillars:
* **Domain Isolation:** (High / Medium / Low) - Are business rules separated from frameworks/DB?
* **Testability:** (High / Medium / Low) - Can the business logic be unit tested without mocking databases/external APIs?
* **Component Cohesion:** (High / Medium / Low) - Are files grouped logically by feature/domain or scattered?

### 2. Core Architectural Map
Provide a visual ASCII diagram of the **current** layer relationships vs the **recommended** Clean Architecture layer relationships for this project.

*Example Current Map:*
`Controller ──> ORM Model (Mixed Logic/DB) ──> Third-Party API`

*Example Target Map:*
`Controller ──> Use Case (Core Logic) ──> Interface (Port) <── Adapter (Infrastructure/DB)`

### 3. Key Findings & Anti-Patterns
Highlight 2 to 4 major architectural pain points found in the codebase. For each finding, provide:
* **The File/Code Location:** Specify path(s) and snippet(s).
* **The Violation:** Explain the architectural issue (e.g., "Leaky Abstraction", "Circular Dependency", "DIP violation").
* **The Reasoning:** Explain *why* this is a risk long-term (e.g., "Changing the SMS provider will require rewriting the core registration use case").

### 4. Step-by-Step Refactoring Plan
Offer a tactical, low-risk sequence of steps to migrate toward a cleaner architecture.
* Avoid massive, "burn it all down" rewrites.
* Focus on introducing Interfaces (Ports), extracting Use Cases (Interactors) from Controllers/Routes, and moving ORM/External Client code into Repository Adapters.
* Provide concrete code comparison templates (e.g., "Before" vs "After") matching the codebase's language.
