# Governance

Constitution: `.specify/memory/constitution.md` (v1.0.0, ratified 2026-11-01).
It is enforced by `/speckit.plan`'s Complexity Check. Read it; do not paraphrase it
back into code.

## Principles

| # | Principle | Practical check |
|---|---|---|
| I | Token-only styling (non-negotiable) | kit CSS uses `--td-*` only; no hex/rgb/hsl, no Tailwind utilities inside kit components, no inline visual styles |
| II | Escape the box (non-negotiable) | popover-family panels teleport to `body`, use `usePopover` flip/shift/cap, reposition on resize/scroll |
| III | Compiled-CSS distribution | `dist/styles.css` is self-sufficient with token variables; consumers never run kit source through their bundler |
| IV | Test-first + axe | failing `vitest` before behaviour; `expectNoA11yViolations`; keyboard and ARIA are part of the contract |
| V | One shared implementation | `useFocusTrap`, `usePopover`, `useScrollLock`, `useId`, `modalStack`; no per-component copies |
| VI | Registry and docs stay true | registry, package README, and `_ai/specs/` updated in the same change |
| VII | YAGNI | no adapters, brand variants, or second medium until a real second consumer exists |

## When to write what

| Situation | Artifact |
|---|---|
| New feature or behaviour | SPEC in `_ai/specs/`, indexed |
| Breaking public API | ADR in `_ai/technical_decisions/` |
| Violating I, II, or IV | Explicit exemption in the SPEC |
| Change inside a governed area | Amend the SPEC; do not diverge silently |

Naming: `SPEC__YYMMDD-N__kebab-title.md` (per-day sequence) and
`YYMMDD_HHMM__ADR__kebab-title.md`. Every ADR is referenced from the SPEC or plan
that depends on it.

## Gates

CI (`.github/workflows/ui.yml`) runs `pnpm -r typecheck`, `pnpm -r test`, and
`pnpm -r build` on every PR, and publishes on tags. Run the same locally before
reporting done.

Known drift: the workflow's publish step still filters `@topdata-software-gmbh/ui`;
the renamed package is `@topdata-software-gmbh/ui-kit-web-vue3`. Verify before
touching publishing.

## Review checklist

- Does the change alter a public component API, token name, or token value?
- If yes: is there a SPEC (and ADR for breaking changes) and an index entry?
- Does any component still pass `src/styles.test.ts` (no raw colours, expected
  stylesheet list)?
- Is shared behaviour in a composable rather than a second copy?
- Are popovers teleported and collision-handled?
- Did the registry, README, playground, and CHANGELOG move with the code?
