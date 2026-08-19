---
name: grasp-microworld
description: Builds a temporary interactive "micro-world" — a steppable, manipulable playground that visualizes the state and logic of a piece of code, so you understand it by playing with it instead of reading it. Use after a grasp-diff, when reviewing AI-generated logic with runtime state, when state changes are hard to follow mentally, or when you want to "what-if" through an algorithm before approving it.
argument-hint: "[code-path] [--steps N]"
---

# Grasp the Microworld: Understanding by Playing

## Objective

Build a temporary, single-file interactive simulation that lets the developer **step through program state**, **manipulate inputs**, and **observe what-if behavior** — teaching the logic of a change through exploration, not prose. The artifact is disposable teaching material, never production code.

## Step 1: Analyze the Code

Identify the code whose *behavior* needs understanding (from `$ARGUMENTS`, the working tree, or the change just discussed):

- Extract the **core state**: variables, data structures, and how they transform per step/iteration.
- Extract the **execution steps**: the meaningful transitions a learner should click through (function calls, loop iterations, state mutations).
- Extract the **knobs**: inputs/parameters worth exposing as sliders or toggles.

If there is no meaningful runtime state (pure formatting, config-only, one-line rename), say so and offer `grasp-diff` instead. Do not force a playground.

## Step 2: Choose the Artifact Type

Use this decision matrix — bias toward interactive D3:

| Type | Delegate skill | Best for |
|---|---|---|
| Static state diagram | `viz-static-svg` | Trivial 2–3 step logic, transition charts, before/after boxes |
| Steppable state playground | `viz-d3` | **Default.** Sequential/looping logic, shifting state, data transformations, what-if exploration |
| 3D/spatial playground | `viz-webgl` | Grids, geometry, spatial algorithms, physics — things that live in space |

Load the chosen skill with the **skill tool** and follow its instructions, then apply the micro-world requirements below — they override the generic visualization conventions where they conflict.

## Step 3: Micro-World Requirements (overlay on the chosen skill)

The artifact must be a *teaching instrument*, not a generic chart. Add ALL of the following:

1. **Stepping controls:** Step Forward / Step Back / Play / Reset buttons driving the execution steps.
2. **State readout:** a live panel showing the current values of the core state variables at the current step (name → value, updated on every step).
3. **What-if knobs:** sliders, toggles, or inputs bound to the extracted knobs — changing one recomputes the state and updates the readout and visuals immediately.
4. **Code anchoring:** each step displays a short snippet (or function/line name) of the real code it corresponds to, so the learner maps visualization → code.
5. **Guided tour (optional):** a "Show me" mode that auto-steps and narrates each transition once.
6. **Introduction modal:** shown automatically on first open — a plain-language welcome that explains (a) what the underlying code/system does, (b) what the playground shows and how to read it, and (c) how to use it (buttons, knobs, tour). Include a "don't show again" checkbox persisted via `localStorage` (guarded in `try/catch` so `file://` fails gracefully).
7. **Contextual help modals:** a small round `?` icon button next to each section title, knob group, and the code-anchor panel, each opening a modal with *that section's* explanation (what it shows, how to interpret it, which code/state variable it maps to). Plus a fixed corner `?` button with the global overview. All modals close via ✕, click-outside, or `Esc`. Implement one generic modal + a help-content map keyed by section, not N duplicated modals.
8. Single self-contained `.html` (or `.svg`) file, written to the path the delegated skill specifies; title it `Micro-world: <what this teaches>`.

## Step 4: Verify and Hand Off

- Re-read the artifact once for correctness of the state transitions against the real code.
- **Open the artifact for the user** once it is written, by launching it in the default browser in the background:
  `xdg-open <path-to-file.html> >/dev/null 2>&1 &`
- Confirm the file path to the user and suggest `grasp-diff` if they also want the structured walkthrough, or `grasp-shared` to build team understanding.
- Also offer to regenerate with fewer/more steps (`--steps N`) if the granularity feels wrong.