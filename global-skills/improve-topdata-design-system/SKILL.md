---
name: improve-topdata-design-system
description: Add or change TopData design-system components, `--td-*` tokens, or brand manifests, and fix registry, style-guard, or a11y drift. Use when creating or refactoring a `Td*` component, adding a token, changing a brand value, updating `packages/ui-component-registry.yaml`, or when asked to "improve the component library", "add a component", or "fix the design system". Routes through the constitution, SPEC, and ADRs and runs the pnpm gates.
---

# Improve TopData Design System

Change the canonical monorepo
(`github.com/topdata-software-gmbh/topdata-design-system`). If the task is only
about *using* the kit inside an app, use `use-topdata-design-system`; do not edit
the monorepo from a consumer task.

## Hard rules

- **Governance is upstream.** Read `.specify/memory/constitution.md` before editing.
  Principles I (token-only), II (viewport-safe overlays), and IV (test-first + axe)
  are non-negotiable; a violation needs an explicit, documented exemption.
- **Never hand-edit generated output.** `packages/tokens/dist/` and the kit's
  compiled `styles.css` are build artifacts.
- **Tokens come only from `designs/<brand>/design.yaml`.** Never sample a hex from
  `previews/` or `examples/` and write it back; that corrupts the brand.
- **No raw colour or palette in kit CSS.** Hex, `rgb()`, `hsl()`, and raw Tailwind
  palette classes are banned; `src/styles.test.ts` fails on them.
- **One shared implementation per behaviour.** Reuse `useFocusTrap`, `usePopover`,
  `useScrollLock`, `useId`, and `modalStack`; do not copy logic per component.
- **Breaking public API needs an ADR; new behaviour needs a SPEC** (`_ai/specs/`,
  `index.md` updated) plus a registry row (`packages/ui-component-registry.yaml`).
- **YAGNI.** No second kit, brand variant, or medium without a real second
  consumer and an approved ADR.
- **No auto-commit.** Commit only when the user asks in this conversation.

## Workflow

### 1. Locate and prime

- Repo root: the directory whose `package.json` has `"name": "topdata-design-system"`.
- Read `.specify/memory/constitution.md`, `packages/ui-component-registry.yaml`,
  the ADRs in `_ai/technical_decisions/` that touch the area, and the relevant
  `_ai/specs/SPEC__*.md`.
- Toolchain: Node 26 and `pnpm@12.16.1` (CI pins both).

### 2. Classify the change

| Change | Where it lands |
|---|---|
| Brand or token value | `designs/<brand>/design.yaml` |
| Token name or contract | `packages/tokens/src/contract.ts` + `semantic-map.yaml` |
| Component behaviour or markup | `src/components/Td*.vue` + `Td*.test.ts` |
| Component visuals | `src/styles/components/<name>.css` (`.td-*`, `--td-*` only) |
| Registry or doc drift | `packages/ui-component-registry.yaml`, package README, `_ai/specs/index.md` |

### 3. Governance gate

- Breaking public API: add an ADR in `_ai/technical_decisions/`.
- New or changed behaviour: add one SPEC per feature in `_ai/specs/`
  (`SPEC__YYMMDD-N__kebab-title.md`, Requirement/Scenario format) and index it.
- Constitution I/II/IV conflict: record the exemption in the SPEC; never take a
  silent shortcut.

### 4. Test first

- Add a failing case to the component's `Td*.test.ts` before implementing.
- Cover default, focused, disabled, loading, error, and keyboard states.
- Accessibility is part of the contract: call `expectNoA11yViolations` from
  `tests/setup.ts`; `wcag2a/2aa/21a/21aa` must stay green.

### 5. Implement

- The SFC keeps behaviour, typing, slots, and ARIA; no `<style scoped>` and no
  inline visual styles.
- Visuals go in the component stylesheet, built only from `--td-*`.
- Popover-family panels teleport to `document.body` and position through
  `usePopover` (flip, shift, max-height) per Principle II.
- Export the component from `src/index.ts` and import its stylesheet there in the
  same change.

### 6. Update the contract surfaces together

`src/index.ts`, `src/styles.test.ts` (expected stylesheet list),
`packages/ui-component-registry.yaml`, `packages/ui-kit-web-vue3/README.md`,
`_ai/specs/` + `index.md`, `playground/src/App.vue`, and `CHANGELOG.md` under
`## [Unreleased]`. A visible behaviour without a playground entry is incomplete.

### 7. Verify

```bash
pnpm -r typecheck
pnpm -r test
pnpm -r build
pnpm dev    # playground at http://localhost:5181
```

Token work: `pnpm --filter @topdata-software-gmbh/design-tokens build` must resolve
every contract token for dark and light and fail on a missing one.

### 8. Report

Show the diff, affected components/tokens, SPEC/ADR ids, and gate results. Flag
drift you noticed, for example `.github/workflows/ui.yml` publishes
`@topdata-software-gmbh/ui` while the package is
`@topdata-software-gmbh/ui-kit-web-vue3`. Commit only when asked.

## References

- [references/governance.md](references/governance.md) - constitution principles and
  when SPEC vs ADR vs exemption applies.
- [references/token-pipeline.md](references/token-pipeline.md) - design manifest to
  semantic map to contract to build, and the token rules.
- [references/component-workflow.md](references/component-workflow.md) - file map,
  test/a11y pattern, style guard, and update checklist.
