# Token pipeline

```text
designs/<brand>/design.yaml          source of truth (authoritative values)
packages/tokens/semantic-map.yaml    brand values -> semantic token names
packages/tokens/src/contract.ts      canonical token name list
        |
        +-- build --> dist/tokens.css, dist/tokens.json, tailwind-preset
```

`design.yaml` is the only source of token values. `resources/`, `previews/`, and
`examples/` may inform a human; never copy a value out of them. `dist/` is
generated; never edit it.

## Manifest rules

- Token values are objects with dot-separated paths:
  `tokens.colors.core.primary.hex`.
- Every group carries `_source` (provenance) and optionally `_note` (something a
  reader must not get wrong). Keys starting with `_` are metadata and are skipped
  by resolution.
- Surfaces inherit brand tokens; `overrides` is a sparse deep-merge:
  `resolve(tokens, surface, path) = dig(surface.overrides, path) or dig(tokens, path)`.
  A surface that agrees declares no colours. Retire a deviation by deleting its
  `overrides` block.
- `entry` is a repo path; `url` is a live property paired with `captured_at` and a
  `preview` screenshot.
- `designs.yaml` is a discovery index only; it must not duplicate tokens.
- Upstream mirrors (`resources/logo/*`, `resources/themes/*` from `topdata-assets`)
  are edited upstream, not here.

## Adding or changing a token

1. Add the value (or override) in `designs/<brand>/design.yaml`.
2. Add the semantic name in `packages/tokens/semantic-map.yaml`.
3. Add the name to the canonical list in `packages/tokens/src/contract.ts`.
4. Rebuild; update the SPEC and `CHANGELOG.md`.

## Checks

```bash
pnpm --filter @topdata-software-gmbh/design-tokens build
pnpm --filter @topdata-software-gmbh/design-tokens test
```

The build resolves every contract token for dark and light and fails when one is
missing. Derived values are `color-mix()` over other tokens, so a brand change
propagates everywhere. Token tests cover contract completeness, determinism, and
contrast.

## Theming

`:root` carries the dark theme; `data-theme="light"` on `<html>` selects the light
theme. `useTheme` in `@topdata-software-gmbh/ui-kit-web-vue3` manages the attribute
and the stored preference. Do not duplicate token values in app CSS; consume
`tokens.css`, the Tailwind preset, or `var(--td-*)`.
