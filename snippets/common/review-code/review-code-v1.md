---
name: "Review Code V1"
description: "REVIEW CODE V1"
createdAt: 2025-12-17
createdBy: Cascade
updatedAt: 2025-12-17
updatedBy: Cascade
tags: [common, review]
documentType: PROMPT_TEMPLATE
---

Here is a robust prompt designed to make the AI agent act as a **Senior Lead Developer** conducting a code review before any code is written.

It leverages the fact that the agent has codebase access by instructing it to cross-reference the plan against your specific Entity definitions and Service architecture.

### The Prompt

```markdown
Act as a Senior Symfony/Vue Architect and Shopware 6 Integration Specialist. Your task is to perform a rigorous "Pre-Implementation Review" of the plan located at: 

`ai-backlog/plans251217__IMPLEMENTATION_PLAN__sw6_multilingual_categories.md`

You have full access to my codebase. Do not just read the text of the plan; you must cross-reference the plan's proposed steps against my existing implementation to ensure technical feasibility, correctness, and adherence to Shopware 6 data structures.

**Context:**
- **Goal:** Implement multilingual category support for a Shopware 6 sales integration.
- **Stack:** Symfony (Backend), Doctrine ORM (MariaDB), Vue.js (Frontend).

**Please analyze the plan based on the following criteria:**

### 1. Database & Doctrine Schema Verification
Scan my `src/Entity` directory. 
- Does the plan correctly propose how to handle translations? (e.g., separate Translation entities vs. Gedmo Translatable vs. JSON columns).
- If the plan proposes a new association (e.g., `Category` -> `CategoryTranslation`), check if my current `Category` entity architecture supports this or if it requires a breaking change.
- Does the plan account for Shopware's specific `language_id` or `locale` mapping?

### 2. Shopware 6 Integration / Sync Logic
Scan my existing synchronization services (likely in `src/Service/Shopware` or similar).
- Does the plan explain how we fetch translated fields from the Shopware 6 Store-API or Admin-API?
- Does it address how we handle "Fallback Languages" (e.g., if a category has no EN translation, does it fallback to DE or crash)?
- Are we syncing the `bread_crumb` or `slot_config` in multiple languages?

### 3. API & Serialization (Symfony)
Scan my `src/Controller` and serialization groups (Attributes or XML/YAML).
- Does the plan define how the API will serve the correct language to the Vue frontend? (e.g., via a `?locale=en` query param or `Accept-Language` header).
- Will the proposed changes cause N+1 query issues in Doctrine when fetching the category tree?

### 4. Frontend Feasibility (Vue.js)
Scan my `assets/js` or `src/frontend` (Store/Pinia/Vuex and Components).
- Does the plan align with my current state management for switching languages?
- Does the plan account for reactive updates to the Category Tree when the user switches the language?

### 5. Missing Elements
Identify gaps in the plan. Examples to look for:
- Database Migrations.
- Handling of slugs/SEO URLs in multiple languages.
- Cache invalidation strategies when translations change.

**Output Format:**
Provide a report with:
1.  **Feasibility Score (0-10):** How ready is this plan?
2.  **Critical Risks:** Any step that will break the build or corrupt data.
3.  **Code Context Checks:** Specific files in my repo that conflict with the plan.
4.  **Refinement Suggestions:** Rewrite any vague steps in the plan to be specific code instructions.
```

---

### Why this prompt works

1.  **Forced Context Awareness:** By explicitly telling it to "Scan `src/Entity`" or "Scan `src/Controller`," you force the AI to ground its feedback in your actual code, rather than giving generic advice.
2.  **Shopware Specificity:** It addresses the specific pain points of SW6 integrations (Fallback languages, API structures, SEO URLs).
3.  **Full Stack Coverage:** It checks the data layer (Doctrine), the transport layer (API/Serialization), and the presentation layer (Vue).
4.  **N+1 Prevention:** Multilingual implementations often destroy performance by querying translations one by one. This prompt specifically asks the agent to look for that risk.

### Follow-up Tip

If the AI returns a high feasibility score, ask it to generate the **Database Migration** file immediately. That is usually the "source of truth"—if the migration looks correct, the rest of the plan is usually solid.