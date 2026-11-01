# Consumption rules

## Packages

| Package | Role |
|---|---|
| `@topdata-software-gmbh/design-tokens` | generated `--td-*` CSS variables, `tokens.json`, Tailwind preset |
| `@topdata-software-gmbh/ui-kit-web-vue3` | Vue 3 components, composables, compiled `styles.css` |

## Surfaces and kits

From `packages/ui-component-registry.yaml`. One kit per surface.

| Kit | Status | Stack | Consumers |
|---|---|---|---|
| `topdata-vue` | active | Vue 3 + TypeScript + Tauri | repo-manager (desktop window), agent-composer (web) |
| `tradeguard-vue` | legacy | Vue + Vuetify + `Tdx*` | tradeguard-app; do not introduce the new kit |
| `docdeck-vanilla` | legacy | TypeScript + CSS (Catppuccin) | docdeck; grandfathered until migration |
| `topdata-tui-go` | planned | Go + bubbletea + lipgloss | none yet |

## Components

- Actions: `TdButton`
- Forms: `TdFormField`, `TdInput`, `TdSelect`, `TdTextarea`, `TdCheckbox`
- Feedback: `TdAlert`, `TdBadge`, `TdSpinner`, `TdToast`, `TdToastStack`
- Overlays: `TdModal`, `TdMenu`, `TdMenuItem`, `TdSegmentedControl`
- Navigation and chrome: `TdSidebar`, `TdSidebarHeader`, `TdSidebarBody`,
  `TdSidebarSection`, `TdSidebarItem`, `TdSidebarFooter`, `TdLanguageSwitcher`
- Icons: `TdIcon` (curated `lucide-vue-next` map)

Use slots as designed: `TdButton` takes `icon-left` and `icon-right`; an icon-only
button requires `aria-label` or `aria-labelledby`.

## Tokens and Tailwind

- Prefer the preset utilities: `bg-surface`, `text-fg-muted`, `border`,
  `rounded-lg`, `font-heading`, shadow and spacing utilities backed by tokens.
- Otherwise use `var(--td-*)` directly.
- Never use `slate-*`, `cyan-*`, `rose-*`, `emerald-*`, `amber-*`, or `sky-*` for
  brand surfaces.
- The global `.td-*` class names are the visual contract; a plain-HTML app may
  import `styles.css` and reuse them without Vue.

## Theming

```ts
import { useTheme } from "@topdata-software-gmbh/ui-kit-web-vue3";

const { mode, setMode, toggle } = useTheme();
```

Dark is the default; `data-theme="light"` on `<html>` selects light. Pass
`{ storage: { get, set } }` to persist in app config instead of `localStorage`.

## Localization

`useLanguage` syncs `<html lang>` and persists the preference;
`TdLanguageSwitcher` is the compact picker.

## Anti-patterns

| Don't | Do |
|---|---|
| `class="bg-slate-800 text-cyan-300"` | `class="bg-surface text-fg-muted"` or `var(--td-*)` |
| hand-rolled `<button class="...">` | `TdButton` |
| a chip/badge `<span>` | `TdBadge` |
| a custom dropdown with absolute positioning | `TdMenu` / `TdSelect` (teleported, collision-safe) |
| copying `button.css` into the app | import `styles.css` from the package |
| a new colour for a product | a token in `design.yaml` via the improve skill |
| a second kit in one surface | one kit per surface; ADR to migrate |

## Escalation

If the design system cannot express the need:

1. Check `packages/ui-component-registry.yaml` and the package README for an
   existing component or variant.
2. If it is genuinely missing, run `improve-topdata-design-system` to add it with a
   SPEC, tests, registry entry, and the pnpm gates.
3. Do not fork the component locally; a local fork becomes a second kit by
   accident.
