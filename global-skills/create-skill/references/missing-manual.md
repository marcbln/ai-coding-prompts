# The Missing Manual: How to Write Great Skills

Here is a structured summary of the core concepts from the presentation **"The Missing Manual: How to Write Great Skills"** by Matt Pocock [https://www.youtube.com/watch?v=UNzCG3lw6O0]

---

## Overview & Problem Statement
* **"Skill Hell":** Developers and organizations have access to many AI skills/prompts but lack a systematic framework to determine quality, evaluate effectiveness, or reliably steer agents.
* **Objective:** A 4-part **Skill Checklist** to design, structure, steer, and optimize agent skills.

## The 4-Part Skill Checklist

```
1. Trigger  ➔  2. Structure  ➔  3. Steering  ➔  4. Pruning
```

## 1. Trigger (How the skill is invoked)
Decide whether a skill should be triggered automatically by the model or manually by the user.

* **Model-Invoked Skills:**
  * Uses a description that stays in the agent's system context. The model decides autonomously when to call the skill.
  * **Trade-off:** Increases **Context Load** (consumes token space, adds noise) and introduces **unpredictability** (the model may fail to call it when needed).
* **User-Invoked Skills (e.g., `/skill-name`):**
  * Invoked explicitly by the user (`disable-model-invocation: true`).
  * **Trade-off:** Reduces context load and eliminates invocation uncertainty, but increases **Cognitive Load** on the user (the user must know the skill exists and when to use it).
* **Tip #1:** *Deliberately decide between user-invoked and model-invoked based on the trade-off between context load and cognitive load.*

## 2. Structure (Internal layout of the skill)
Organize the skill file (`SKILL.md`) to maximize clarity and minimize token usage.

* **Two Core Components:**
  * **Steps:** The step-by-step procedure the agent must follow.
  * **Reference:** Templates, glossaries, or background information supporting those steps.
* **Optimizing File Size:**
  * Keep `SKILL.md` as small and concise as possible to reduce token consumption and improve auditability.
* **Handling Branching Logic (Context Pointers):**
  * If reference material is only needed for certain branches/use cases, remove it from `SKILL.md` into separate Markdown files.
  * Use **Context Pointers** (file references) so the agent only loads external reference files when relevant.
* **Tip #2 & #3:** *Structure skills into distinct Steps and References, and keep the main `SKILL.md` minimal.*
* **Tip #4:** *Hide branching reference material behind external context pointers.*

## 3. Steering (Guiding agent behavior effectively)
How to ensure the agent follows your intent and performs high-quality work.

* **Technique 1: Leading Words (Leitmotifs)**
  * **Problem:** Agent does not behave as expected despite lengthy instructions.
  * **Solution:** Use dense, high-leverage domain terms (e.g., *"Vertical Slice"* vs. long paragraphs against layer-by-layer coding).
  * **Mechanism:** When the model repeats the leading word in its reasoning/output tokens, it activates relevant priors and aligns its behavior.
  * **Tip #5:** *Use consistent, high-leverage leading words throughout the skill.*

* **Technique 2: Hiding Future Steps (Enforcing Legwork)**
  * **Problem:** When given multi-step tasks (e.g., 1. Ask clarifying questions, 2. Write plan), agents often rush through the preliminary legwork to reach the final goal.
  * **Solution:** Split compound tasks into distinct, sequential skills (e.g., `/grill-with-docs` for interviewing, followed by `/to-prd` for plan generation).
  * **Tip #6:** *Increase thoroughness on early phases by hiding future steps in separate skills.*

## 4. Pruning (Cleaning and refining skills)
Eliminate bloat to keep skills reliable and token-efficient.

* **Avoid Duplication (DRY):** Ensure every instruction, step, or template has a single source of truth.
* **Remove "Sediment":** Regularly delete stale, unmaintained, or legacy instructions accumulated over time.
* **Eliminate "No-ops":** Remove instructions that sound good but don't measurably change agent output.
* **Tip #7: The Deletion Test:** *Test deleting instructions. If the agent's behavior doesn't degrade without it, leave it out.*

## Summary Review Checklist

| Pillar | Core Question | Action |
| :--- | :--- | :--- |
| **1. Trigger** | Who invokes it? | Choose model-invoked vs. user-invoked intentionally. |
| **2. Structure** | How is it laid out? | Separate Steps from References; offload branch docs via pointers. |
| **3. Steering** | How do we guide it? | Use **Leading Words**; split multi-step workflows to force legwork. |
| **4. Pruning** | What can be removed? | Apply the **Deletion Test**, remove No-ops, and eliminate sediment. |