---
name: use-topdata-design-system
description: >-
  Consume the TopData design system correctly in a Vue 3 or Tauri app: design
  tokens, `Td*` components, theming, and the no-raw-palette rule. Use when
  building or reviewing UI in a TopData app (repo-manager, agent-composer,
  TradeGuard, docdeck), adding a screen or form control, styling with Tailwind,
  or when asked "how should this look", "use the design system", "are we
  on-brand", or "why is this off-brand".
---

# Use TopData Design System

Apply the published packages in a consumer app. Do not edit the design-system
monorepo from here; if the kit is missing or wrong, route to
`improve-topdata-design-system`.

## Install and import

```bash
pnpm add @topdata-software-gmbh/design-tokens @topdata-software-gmbh/ui-kit-web-vue3 @vue/runtime-dom
```

```ts
import "@topdata-software-gmbh/design-tokens/tokens.css";
import "@topdata-software-gmbh/ui-kit-web-vue3/styles.css";
import { TdButton, TdInput, TdFormField, TdModal } from "@topdata-software-gmbh/ui-kit-web-vue3";
```

Import order matters: tokens first, then kit styles, then app styles. `vue` is a
peer dependency (`^3.4.30`). The kit ships compiled CSS; do not run its source
through your bundler or Tailwind pass.

## Hard rules

- **Use `Td*` components before hand-rolling.** Available: `TdButton`, `TdInput`,
  `TdFormField`, `TdSelect`, `TdTextarea`, `TdCheckbox`, `TdBadge`, `TdAlert`,
  `TdSpinner`, `TdModal`, `TdToast`/`TdToastStack`, `TdMenu`/`TdMenuItem`,
  `TdSegmentedControl`, `TdLanguageSwitcher`, `TdSidebar*`, and `TdIcon`.
- **No raw Tailwind palette and no hard-coded hex.** Use kit components, the token
  Tailwind preset (`bg-surface`, `text-fg-muted`, `rounded-lg`, `font-heading`), or
  `var(--td-*)`.
- **One kit per surface.** Do not add `ui-kit-web-vue3` to a surface registered to
  another kit (TradeGuard is legacy Vuetify/`Tdx*`; docdeck is legacy vanilla).
  Migrating a surface needs an ADR.
- **Theme through `useTheme`.** It writes `data-theme` on `<html>`, follows the OS
  preference, and persists the choice under `topdata.theme.v1`. Do not hand-set
  theme attributes.
- **Brand values come from `designs/<brand>/design.yaml`**, never from previews,
  screenshots, or invoices.
- **Never copy kit CSS** into the app or edit anything under `dist/`.

## Workflow

1. Identify the surface and its registered kit in
   `packages/ui-component-registry.yaml`.
2. Compose from existing `Td*` components and token-backed utilities.
3. If a component is missing, a variant is wrong, or a token is absent, stop and
   route to `improve-topdata-design-system` (SPEC/ADR) instead of forking styles.
4. Verify in the app: typecheck, tests, and a visual check of light and dark.

## References

- [references/consumption-rules.md](references/consumption-rules.md) - component
  map, token utilities, theming, migration notes, and anti-patterns.
