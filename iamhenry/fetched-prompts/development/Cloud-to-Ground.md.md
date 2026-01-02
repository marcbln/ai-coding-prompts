---
slug: cloud-to-ground-md
name: "💻 Cloud to Ground.md"
category: development
version: 1.0.0
groups:
  - read
  - command
source: global
---

```
Purpose: Useful in software dev for getting a systemic analysis before implementing a feature/bug. Uses "cloud to ground" methodology (zooming in and out of the codebase to understand it more thoroughly). Applies "tracer bullet" methodology to be more direct with the implementation.
```

## Step 1: Define the Build Target
```
I need to build: [FEATURE DESCRIPTION]
```

## Step 2: Identify Tracer Bullet
**Define the minimal viable technical spike:**
- What's the simplest end-to-end flow that delivers user value?
- What's the riskiest technical assumption to validate first?
- What integration points are most likely to break?

## Step 3: Complexity Assessment
**Rate tracer complexity (1-5):**
- 1-2 (Simple): Basic integration, single API call → Target: 1-2 iterations
- 3 (Moderate): Multi-step flow, data transformation → Target: 2-3 iterations  
- 4-5 (Complex): Real-time, multi-service coordination → Target: 3-4 iterations

**Full feature complexity:** [For reference only]

## Step 4: Priority-Filtered Unknowns
**🔍 KNOWLEDGE CONFIDENCE:** [HIGH/MEDIUM/LOW] [LEARNING:]

**IF LOW:** "🚨 ESCALATION REQUIRED - Domain knowledge insufficient for safe analysis."

**Focus only on tracer-critical unknowns:**
- Core integration feasibility
- Critical performance constraints  
- Security requirements for MVP
- Essential error handling
- [Add specific unknowns based on feature]

## Step 5: Targeted Clarification
**📋 INQUIRY CONFIDENCE:** [HIGH/MEDIUM/LOW] [LEARNING:]

**IF LOW:** "🚨 ESCALATION REQUIRED - Cannot formulate safe clarification questions."

**Ask up to 5 critical questions (numbered multiple choice):**
1. [Most critical tracer unknown] - A) Option B) Option C) Option
2. [Second priority] - A) Option B) Option C) Option
3. [Third priority] - A) Option B) Option C) Option
[Continue up to 5 questions max]

## Step 6: Confidence Assessment
**After user responds, provide:**
```
IMPLEMENTATION CONFIDENCE: [HIGH/MEDIUM/LOW] (X%) [LEARNING:]

HIGH (80%+): "With these answers, I can determine [aspects] with high certainty."
MEDIUM (50-79%): "⚠️ FLAGGED UNCERTAINTIES: [specific gaps]"
LOW (<50%): "🚨 MANDATORY HUMAN REVIEW - Insufficient knowledge to proceed safely."
```

## Step 7: Tracer Iterative Refinement
**Each iteration expands tracer systematically:**

### Iteration Structure:
- **TRACER FOCUS:** What does this iteration prove/expand?
- **CLOUD:** User value delivered at this tracer level
- **GROUND:** Implementation for current tracer scope only
- **VALIDATION CONFIDENCE:** [HIGH/MEDIUM/LOW] [LEARNING:] - **IF LOW:** "🚨 ESCALATION REQUIRED"
- **VALIDATION:** Does tracer work? What's next expansion priority?
- **EXPANSION DECISION:** Ready to expand scope or strengthen current tracer?

### Iteration Progression:
- **Iteration 1:** Prove core integration works (happy path only)
- **Iteration 2:** Add essential error handling
- **Iteration 3:** Address critical security/performance requirements
- **Iteration N:** Expand toward full feature scope

## Step 8: Dynamic Continuation Rules
- **CONTINUE IF:** Critical tracer unknowns remain unresolved
- **AUTO-ESCALATE:** If unknowns remain at target limit, reassess complexity and justify extension
- **HARD STOP:** 6 iterations maximum
- **STOP WHEN:** Tracer proves viability and path to full implementation is clear

## Step 9: Accuracy Flywheel & Final Delivery
**Once tracer is validated:**

**📈 ACCURACY FLYWHEEL:**
- **Abstentions:** [What "I don't know" moments occurred? What should be researched?]
- **Corrections:** [What predictions were wrong? What patterns emerged?]
- **Next Session:** [One thing to watch for or do differently next time]

**Implementation Plan (Markdown):** Complete development roadmap including:
  - Tracer bullet findings and validated assumptions
  - Step-by-step implementation sequence from tracer to full feature
  - Technical architecture decisions discovered through iterations
  - Integration points and API specifications identified
  - Security, performance, and error handling requirements uncovered
  - Risk mitigation strategies for each development phase
  - Testing approach based on tracer validation
  - Deployment considerations and rollout strategy

---
*Show iteration count, unknowns resolved, and expansion reasoning throughout process.*