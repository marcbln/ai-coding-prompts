---
name: sw67-storefront-plugin-bundle
description: |
  Never import Shopware core's plugin system into a plugin storefront bundle in SW 6.7. Importing `src/plugin-system/plugin.manager` compiles a second copy of core's singleton and overwrites `window.PluginManager` with an empty registry, breaking every storefront page.

  Use this when:
  - Writing or reviewing `src/Resources/app/storefront/src/main.js` or a `*.plugin.js`
  - Debugging `The plugin "X" is not registered. You might need to register it first.`
  - Debugging `TypeError: Cannot read properties of null (reading 'get')` at `_registerInstance`
---

# Never `import` from `src/` in a storefront bundle

In `src/Resources/app/storefront/src/`, use the globals Shopware publishes — never import them:

```js
window.PluginManager.register('MyPlugin', () => import('./my.plugin'), '.js-my-selector');
class MyPlugin extends window.PluginBaseClass { /* ... */ }
```

**Why:** Shopware builds plugin bundles with `src` aliased to the *core* storefront sources, so
`import PluginManager from 'src/plugin-system/plugin.manager'` compiles a **second copy** into your
bundle. That module ends with `window.PluginManager = PluginManager`, replacing core's singleton
with an **empty registry on every page**. Core plugins then fail with `The plugin "X" is not
registered` + `Cannot read properties of null (reading 'get')`.

For HTTP, use `fetch()` and keep the `X-Requested-With: XMLHttpRequest` header.

## Verify

```sh
node scripts/verify-plugin-bundle.mjs --dist <dist>/js/<technical-name> [--plugin <Name> --selector <sel>]
```

Non-zero exit on failure — it fails against a bundle with the bug.

## Build guard

Copy `src/Resources/app/storefront/build/webpack.config.js` from `topdata-cart-recovery-sw6`
(auto-detected by `bundle:dump`). It externalises the two safe core modules onto their globals
and fails the build for any other `src/...` import, so this cannot come back.
