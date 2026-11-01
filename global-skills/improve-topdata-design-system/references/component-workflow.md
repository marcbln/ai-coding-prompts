# Component workflow

## File map

```text
packages/ui-kit-web-vue3/src/
  components/TdFoo.vue           behaviour, props, slots, ARIA (no style block)
  components/TdFoo.test.ts       vitest + axe
  components/TdFooBar.vue        subcomponent (e.g. TdMenuItem, TdSidebarItem)
  styles/components/foo.css      global .td-foo rules, --td-* only
  index.ts                       export + stylesheet import
  styles.test.ts                 expected stylesheet list + no-raw-colour guard
playground/src/App.vue           visible example
```

## Test pattern

```ts
import { mount } from "@vue/test-utils";
import { expectNoA11yViolations } from "../../tests/setup";
import TdFoo from "./TdFoo.vue";
import source from "../styles/components/foo.css?raw";

it("has no WCAG A/AA violations", async () => {
  const wrapper = mount(TdFoo, { props: {}, attachTo: document.body });
  await expectNoA11yViolations(wrapper.element);
  wrapper.unmount();
});
```

The stylesheet is imported raw so style assertions can run without a browser. Use
`mount(..., { attachTo: document.body })` for focus, teleport, and keyboard tests.
`expectNoA11yViolations` runs `wcag2a`, `wcag2aa`, `wcag21a`, and `wcag21aa` with
the `region` rule disabled.

## Rules

- SFC: behaviour, typing, slots, and ARIA only. Use
  `defineOptions({ inheritAttrs: false })` when forwarding attributes deliberately.
- Styles: global `.td-*` classes built only from `--td-*`; no hex/rgb/hsl and no
  scoped or inline visual styles. The sidebar and icon guards allow only `1px` and
  `2px` raw lengths.
- Popovers: teleport to `document.body`, position through `usePopover` (flip,
  shift, max-height with inner scroll), reposition on resize and scroll.
- Shared behaviour: extend the existing composable instead of copying it.
- Icons: add new icons to the curated map in the kit; do not import ad-hoc icons
  in a component.
- Every visible component gets a playground entry and a SPEC.

## Update checklist (one change)

1. `components/TdFoo.vue` + `TdFoo.test.ts`
2. `styles/components/foo.css`
3. `src/index.ts`: export the component and import its stylesheet
4. `src/styles.test.ts`: expected stylesheet list
5. `packages/ui-component-registry.yaml`: kit version/notes when the public kit
   changes
6. `packages/ui-kit-web-vue3/README.md`
7. `_ai/specs/SPEC__YYMMDD-N__td-foo.md` + `_ai/specs/index.md`
8. `playground/src/App.vue`
9. `CHANGELOG.md` under `## [Unreleased]`
10. `pnpm -r typecheck && pnpm -r test && pnpm -r build`

## Review questions

- Does the component keep native semantics and forward non-prop attributes?
- Is every interaction state covered by a test and by axe?
- Does the CSS resolve entirely from tokens, including focus rings and borders?
- Would a second component duplicate any behaviour that belongs in a composable?
