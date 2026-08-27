---
name: sw67-theme-plugin-decoupling
description: |
  Shopware 6.7 rule for including another plugin's templates from a theme (or another plugin) without creating a hard dependency. Use when a theme references `@OtherPlugin/...` templates, when extracting a feature out of a theme into its own plugin, when a storefront page crashes after a plugin is deactivated/uninstalled, or when deciding how a theme should degrade gracefully if an optional plugin is missing.

  Use this when:
  - A theme (or plugin) includes/extends a template owned by another plugin
  - Extracting a feature out of a theme into a dedicated plugin (e.g. moving a controller/form/modal out of topdata-theme-focus-sw6)
  - A storefront page throws "template not found" / crashes after deactivating or uninstalling a plugin
  - You need a theme to keep working when an optional plugin is off
  - Deciding between `sw_include ... ignore missing` and a hard `sw_extends` of another plugin's template
---

# SW67 Theme ↔ Plugin Template Decoupling

Rule: **whenever a theme (or any plugin) renders a template that lives in another plugin, use `ignore missing`.**

```twig
{% sw_include '@OtherPluginSW6/storefront/component/foo.html.twig' ignore missing %}
```

## The Hard Dependency Trap

The `@PluginName` Twig namespace is registered only while that plugin's bundle is active. If the plugin is
deactivated/uninstalled, both the namespace and the template vanish. A plain include then throws
`template not found` and **crashes the whole storefront** — not just the one feature.

With `ignore missing`, the include renders nothing. The feature degrades gracefully (e.g. a button/modal simply
doesn't appear) and the theme keeps compiling and rendering.

## Rules

1. **No hard dependency.** The theme must not require the other plugin. Keep the *decision* logic (e.g.
   "show when `tdg_props_verfuegbarkeit == 4`") in the theme; only move the markup/partial into the plugin.
2. **Move logic, not control.** The theme keeps the branch that decides *when* to show the UI; the plugin supplies
   the *what* (the template + controller + routes + snippets).
3. **No dangling POST.** A form whose `action` route is provided by the plugin also disappears when the plugin is off.
   Since the form markup comes from the same plugin (and is absent when off), there is no dead POST target.
4. **Prefer `sw_include ... ignore missing` over `sw_extends`.** Optional UI should be included, not extended, so the
   parent can be missing without breaking the includer.
5. **Verify the degradation.** After implementing, deactivate the target plugin and reload the affected page — it must
   render without error (no button shown).

## Real-World Precedent

This pattern is already used in the Topdata codebase, e.g. in
`topdata-theme-focus-sw6` `buy-widget-form.html.twig`:

```twig
{% sw_include '@BilobaAdGoogleGtagsjs/storefront/biloba/ad-google-gtagsjs/cart.html.twig' ignore missing %}
```

## Applying It to a Feature Extraction

When moving a feature out of `topdata-theme-focus-sw6` into its own plugin:

- The new plugin owns: controller, routes, the feature's own Twig partials, snippets, entity/migration, admin module.
- The theme keeps: the `availability == 4` branch and the `sw_include` points, now pointing at
  `@NewPluginSW6/...` **with `ignore missing`**.
- Delete the feature's templates/snippets/controller from the theme.

Result: theme compiles and renders fine with the plugin on **or off**; the only loss when off is that the feature's UI
is not offered.

## Related

- `sw67-admin-entity-listing` — admin list pages for the extracted feature's stored records
- `sw67-entity-definition` — entity + `updated_at` migration gotcha when persisting requests to the DB
