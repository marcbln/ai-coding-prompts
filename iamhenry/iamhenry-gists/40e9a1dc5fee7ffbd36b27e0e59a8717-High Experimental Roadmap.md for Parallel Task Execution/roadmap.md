# HIGHLY Experimental Roadmap.md Parallel Task Execution

```
## Purpose
1. Break down work into granular tasks
2. Define clear interfaces (contracts)
3. Facilitate parallel development
4. Minimize integration conflicts

## When to Use
- Starting a new software project and needing a comprehensive development plan.
- Planning projects where tasks will be delegated to multiple developers or AI agents simultaneously.
- When aiming to reduce merge conflicts through contract-first development and parallelizable task structures.
- For projects following a layered architecture (Static UI -> Frontend -> Backend -> Polish).
- To ensure consistency and clarity in roadmap documentation across different projects.
```

# Instructions

- Review and analyze the `Required` documents (Bill of Materials, Overview/User Stories).
- Decompose the project into a step-by-step development plan.
- **Prioritize breaking down tasks into the smallest, most independent units possible to enable parallel execution by AI agents and support frequent, small integrations/merges.**
- Break down complex tasks into subtasks with a complexity scale (1-5, where 5 is very complex).
- **Emphasize 'Interface-First' or 'Contract-First' development.** Define data structures (e.g., mock data, TypeScript types), API signatures (e.g., OpenAPI specs for backend), and component prop types *before* dependent tasks are assigned. These contracts are crucial for minimizing merge conflicts when multiple agents work concurrently.

## Parallel Execution Documentation

### REQUIRED SECTIONS FOR ROADMAP:
Include these sections in every generated roadmap to enable clear parallel task execution:

#### 1. Parallel Execution Guide Section
Add immediately after the Overview section:
```markdown
## Parallel Execution Guide

### Phase Dependencies
- Static UI → Frontend → Backend → Polish (sequential)

### Milestone Parallelization
- **Phase 1**: M2, M3, M4 can run parallel after M1 complete
- **Phase 2**: M6, M7, M8 can run parallel after M5 complete  
- **Phase 3**: M9, M10, M11 can run parallel (independent backend systems)
- **Phase 4**: M12, M13 can run parallel (different optimization areas)

### Task Symbols
- ⚠️ **BLOCKING** - Must complete before other tasks can start
- 🔄 **PARALLEL** - Can run simultaneously with other tasks
- ✅ **DEPENDENT** - Requires specific prior task completion
```

#### 2. Task Execution Plans
For each milestone, include execution syntax directly in the milestone header showing parallel opportunities:
```markdown
### Milestone X: [Milestone Name]
**Task Execution Plan: Task 1 ⚠️ → Task 2,3 🔄 (parallel after Task 1)**

Objective: [Brief description]
```

#### 3. Dependencies & Parallelization Per Milestone
For each milestone, include this subsection:
```markdown
Dependencies & Parallelization:
- **BLOCKS**: What this milestone blocks (or "None")
- **BLOCKED BY**: What blocks this milestone
- **PARALLEL WITHIN**: Which tasks within milestone can run parallel
- **PARALLEL WITH**: Which other milestones can run parallel
```

### TASK SYMBOLS USAGE:
- Use ⚠️ for contract/mock data tasks that block other work
- Use 🔄 for component implementations that can run simultaneously  
- Use ✅ for integration tasks that depend on multiple prior completions
- Apply symbols consistently in Step-by-Step Tasks

- Outline the plan in milestones, supporting multiple milestones per phase as needed.
- **Design milestones to group features or components that can be developed in parallel within a phase, guided by clear interfaces.**
- Follow these phases in order: Static UI (UI scaffold, no functionality yet) -> Frontend -> Backend -> UI Polish (e.g., animations).
- Generate a new file in `_ai/docs/ROADMAP.md`.
- **Be mindful of task dependencies: ensure precedent tasks or contract definitions are clear before dependent tasks are listed.**
- Important:
  - Exclude tests in the Static UI phase to keep it lightweight.
  - Name milestones with a project-wide focus (e.g., "Initial UI Components" instead of "Task List")—see Style Guide for details.

## Phase-Specific Guidance

### Phase 1: Static UI
- Objective: Create UI scaffolds with no functionality, using centralized mock data to represent future real data structures. This phase establishes the initial visual contracts.
- Mock Data Instructions:
  1. Create Centralized Mock Data Files:
     - For each major feature or component set, create a file in a `mocks/` directory (e.g., `mocks/[feature].js` where `[feature]` is a descriptive name like "tasks" or "users").
     - Define a lightweight function (e.g., `get[Feature]Data`) that returns a simple data structure mirroring the expected real data (e.g., `[{ id: 1, title: "Task 1" }]`).
     - Keep it minimal: include only essential fields (e.g., `id`, `title`) based on User Stories or Overview document assumptions.
     - Use plain JavaScript objects—no third-party libraries. Consider defining TypeScript types for this data if applicable to the project.
  2. Integrate Mock Data into Components:
     - In each UI component task, import the mock data function (e.g., `import { get[Feature]Data } from '../mocks/[feature].js'`).
     - Pass the mock data as props to the component (e.g., `<Component data={get[Feature]Data()} />`) to render static UI elements.
  3. Document in Roadmap:
     - In the `Data Flow` section, specify the mock data source and its structure as the contract (e.g., "Mock data from `mocks/[feature].js` (contract: `[{ id, title }]`) passed as props to components").
     - In `Acceptance Criteria`, ensure components render mock data correctly (e.g., "Components display [field] from mock data").
     - In `Step-by-Step Tasks`, include steps for creating the mock file and using it in components (see template example).
- Goal: Ensure mock data is easy to swap with real API data in the Frontend phase by maintaining consistent structure and establishing clear data contracts early.

### Other Phases (Frontend, Backend)
- **Contract Definition is Key:**
    - **Frontend Phase:** Before implementing UI interactivity that consumes data, ensure the backend API contracts (e.g., endpoints, request/response schemas from an OpenAPI spec or similar document) are defined. Frontend tasks will be built against these contracts.
    - **Backend Phase:** Backend tasks will focus on implementing the APIs according to the pre-defined contracts. If new data structures are needed, define their schemas first.
- This approach allows frontend and backend development (or different parts of the frontend/backend) to proceed in parallel more safely once contracts are established.

# Requirements

- `USER-STORIES.md`
- (Potentially: `API-CONTRACTS.yaml` or `DATA-MODELS.md` if available upfront for later phases)

---

# Style Guide

### Structure & Formatting
- Use headers for section titles.
- Keep milestone descriptions concise and action-oriented.
- Use bullet points for Data Flow and Acceptance Criteria.
- Use step numbering for Step-by-Step Tasks.
- Reference file paths and contract documents explicitly to ensure clarity.

### Naming Conventions
- Use `Phase X: [Phase Name]` for broader project stages.
- Use `Milestone X: [Milestone Name]` to segment major goals.
- Milestone Naming Rule: Name milestones after broad project goals or feature sets (e.g., "Initial UI Components" or "Core Authentication Services"). **Consider grouping parallelizable feature sets or component groups into distinct milestones within the same phase to facilitate concurrent development.** Avoid single-entity focus (e.g., "Task List"), based on the Overview/User Stories document.
- Keep file names and paths consistent across projects (e.g., `mocks/[feature].js` for mock data, `contracts/api.yaml` for API specs).

### Task Complexity Ratings
- 1-2: Simple UI tasks, minor adjustments, implementing against a well-defined contract.
- 3: Mid-level complexity such as basic API integrations (consuming or implementing a defined endpoint).
- 4-5: High-complexity tasks like complex state management, defining new core data structures/API contracts, performance optimization.
- Ensure tasks are broken down at least 3 levels deep. **Even tasks with higher overall complexity (4-5) should be decomposed into smaller, independent sub-tasks (ideally 1-2 complexity each) suitable for individual assignment by an agent and frequent integration.**

---

This template ensures each development roadmap follows a structured and repeatable format, optimized for clarity and parallel execution.


# Template

```markdown
# [Project Name] Development Roadmap

## Overview
This roadmap outlines the development plan for [Project Name], broken down into clear milestones and phases. Each task includes a complexity rating (1-5, where 5 is most complex) and is designed to support parallel work where possible by defining clear interfaces.

IMPORTANT: Breakup Phases in this order: Static UI (UI scaffold, no functionality yet) -> Frontend -> Backend -> UI Polish (e.g. animations)

## Phase 1: Static UI
Focus on creating UI scaffolds with centralized mock data, no functionality yet. Establishes initial visual and data contracts.

### Milestone 1: [Milestone Name - e.g., "Core Application Shell UI"]
**Task Execution Plan: Task 1 ⚠️ → Task 2,3 🔄 (parallel after Task 1)**

Objective: [Brief description of milestone goal, focusing on a cohesive set of features/components that can ideally be worked on in parallel or with clearly defined interfaces, e.g., "Build foundational UI elements like navbar, sidebar, and main layout structure using mock data."].

Dependencies & Parallelization:
- **BLOCKS**: [What this milestone blocks, e.g., "All other Phase 1 milestones (foundational architecture required)"]
- **BLOCKED BY**: [What blocks this milestone, e.g., "None (starting milestone)"]
- **PARALLEL WITHIN**: [Which tasks within milestone can run parallel, e.g., "Tasks 2, 3 can run after Task 1 complete"]
- **PARALLEL WITH**: [Which other milestones can run parallel, e.g., "None (blocking milestone)"]

Data Flow:
- [Describe mock data flow and the contract it represents, e.g., "Mock data from `mocks/user.js` (contract: `{ id, name, avatarUrl }`) passed as props to UserProfile component."]
- [e.g., "Mock data from `mocks/navigation.js` (contract: `[{ id, label, path }]`) for Navbar items."]

Acceptance Criteria:
- [List criteria, e.g., "Components render with mock data adhering to the defined contract from `mocks/[feature].js`"]
- [e.g., "UI displays [field] from mock data"]
- [e.g., "Layout matches Bill of Materials"]
- Components handle empty data gracefully (show appropriate empty states)
- Components use default props to prevent crashes

Step-by-Step Tasks:
- [ ] 1. Define and create centralized mock data for [feature] ⚠️
  - File: `mocks/[feature].js` [e.g., "user.js"]
  - Contract Definition: [e.g., `function getUserData(): { id: number, name: string, email: string }`]
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 1  
  - [ ] 1.1. Define `get[Feature]Data()` returning [data shape/contract, e.g., "object: { id, name, email }"]  
  - [ ] 1.2. Export the function for component use  
- [ ] 2. Create [feature] UI component(s) 🔄
  - File: `components/[Feature].tsx` [e.g., "UserProfile.tsx"]
  - Consumes Contract: Mock data from `mocks/[feature].js`
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 2  
  - [ ] 2.1. Import `get[Feature]Data` from `mocks/[feature].js`  
  - [ ] 2.2. Render [describe output, e.g., "user name and email"] using `get[Feature]Data()`  
  - [ ] 2.3. Add empty state handling (show message when data is empty, use default props)
  - [ ] 2.4. Apply basic CSS [e.g., "flexbox"] per Overview document  
- (Note: Subsequent tasks for other components in this milestone can be listed here and potentially worked on in parallel if their mock data contracts are also defined.)

### Milestone 2: [Milestone Name - e.g., "Product Catalog UI Elements"]
**Task Execution Plan: Task 1 ⚠️ → Task 2,3,4 🔄 (parallel after Task 1)**

Objective: [Brief description, e.g., "Build UI components for displaying product listings and details using mock data."].

Dependencies & Parallelization:
- **BLOCKS**: [What this milestone blocks, e.g., "None (UI components only)"]
- **BLOCKED BY**: [What blocks this milestone, e.g., "Milestone 1 complete"]
- **PARALLEL WITHIN**: [Which tasks within milestone can run parallel, e.g., "Tasks 2, 3, 4 can run after Task 1"]
- **PARALLEL WITH**: [Which other milestones can run parallel, e.g., "Milestones 3, 4 (different component families)"]

Data Flow:
- [Describe mock data flow and contract, e.g., "Mock data from `mocks/products.js` (contract: `[{ id, name, price, imageUrl }]`) passed as props"]

Acceptance Criteria:
- [List criteria, e.g., "Components render with mock data per contract"]
- Components handle empty data gracefully (show appropriate empty states)
- Components use default props to prevent crashes

Step-by-Step Tasks:
- [ ] 1. Define and create centralized mock data for [secondary_feature] ⚠️
  - File: `mocks/[secondary_feature].js` [e.g., "products.js"]
  - Contract Definition: [e.g., `function getProductsData(): Array<{ id: string, name: string, price: number, imageUrl: string }>`]
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 1  
  - [ ] 1.1. Define `get[SecondaryFeature]Data()` returning [data shape/contract]  
  - [ ] 1.2. Export the function  
- [ ] 2. Create [secondary_feature] UI component(s) 🔄
  - File: `components/[SecondaryFeature].tsx` [e.g., "ProductList.tsx", "ProductCard.tsx"]
  - Consumes Contract: Mock data from `mocks/[secondary_feature].js`
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 2  
  - [ ] 2.1. Import `get[SecondaryFeature]Data` from `mocks/[secondary_feature].js`  
  - [ ] 2.2. Render [describe output] using `get[SecondaryFeature]Data()`
  - [ ] 2.3. Add empty state handling (show message when data is empty, use default props)  

(Continue for additional milestones in this phase as needed)

## Phase 2: Frontend
Focus on adding interactivity and real data integration, working against defined API contracts.

### Milestone 5: [Milestone Name - e.g., "Database Integration and State Management"] 
**Task Execution Plan: Task 1 ⚠️ → Task 2,3 🔄 → Task 4 ✅ (Task 4 depends on 2,3)**

Objective: [Brief description, e.g., "Implement database layer and state management to replace mock data with real data storage."].

Dependencies & Parallelization:
- **BLOCKS**: [What this milestone blocks, e.g., "All other Phase 2 milestones (core data layer required)"]
- **BLOCKED BY**: [What blocks this milestone, e.g., "Phase 1 complete"]
- **PARALLEL WITHIN**: [Which tasks within milestone can run parallel, e.g., "Tasks 2, 3 can run after Task 1; Task 4 after Tasks 2, 3"]
- **PARALLEL WITH**: [Which other milestones can run parallel, e.g., "None (blocking milestone for Phase 2)"]

Data Flow:
- [Describe data flow and contracts, e.g., "Database schema implementation replaces mock data contracts"]
- [e.g., "State management layer consumes database operations through service layer"]

Acceptance Criteria:
- [List criteria, e.g., "User can successfully log in using credentials validated by the backend API."]
- [e.g., "API contract (e.g., `contracts/auth-api.yaml`) for request/response is strictly adhered to."]

Step-by-Step Tasks:
- [ ] 1. Define database schema and API contracts ⚠️
  - Document: `contracts/database-api.yaml` (or relevant section)
  - Contract Definition: [e.g., Database schema interfaces and service layer contracts]
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 4
  - [ ] 1.1. Implement database schema matching architecture design
  - [ ] 1.2. Define service layer interface contracts
- [ ] 2. Implement database service layer 🔄
  - File: `services/databaseService.ts`
  - Consumes Contract: Database schema contracts
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 3
  - [ ] 2.1. Create CRUD operations with proper error handling
  - [ ] 2.2. Implement data validation and transformation
- [ ] 3. Implement state management stores 🔄
  - Files: `stores/[feature]Store.ts`
  - Consumes Contract: Database services
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 3
  - [ ] 3.1. Create feature-specific state stores with database integration
  - [ ] 3.2. Implement loading and error state management
- [ ] 4. Migrate UI components from mock data to state stores ✅
  - Files: Update all existing components to use stores
  - Branch Name: `<type>/<context>-<medium-description>`
  - Complexity: 3
  - [ ] 4.1. Update components to use state stores instead of mock data
  - [ ] 4.2. Add loading and error state handling throughout UI

(Continue for additional phases and milestones as needed, always emphasizing contracts for Backend phase tasks as well, e.g., "Implement API endpoints for [feature] as defined in `contracts/[feature]-api.yaml`")