---
name: sw67-admin-module-navigation
description: Register a new admin module with page routes and a sidebar navigation entry in a Shopware 6.7 plugin, or debug a missing/flickering menu entry under a core group (e.g. Kunden, "Customers"). Use when adding a new admin page/module to a SW 6.7 plugin, when a navigation entry does not show in the admin sidebar, or when the admin console throws "Cannot read properties of undefined (reading 'href')" while the sidebar renders.
---

# SW 6.7 Admin Module Navigation

In Shopware 6.7 plugins register admin pages via `Shopware.Module.register('<module-id>', { routes, navigation })`. Two 6.7-specific facts make this area a frequent source of bugs:

1. **Route names are generated, not chosen.** The route name becomes `"<prefix>.<routeKey>"` where the prefix is `routePrefixName` if set, otherwise the module id with `-` replaced by `.`. If the module id already ends in the route key (e.g. id `topdata-contact-login-list` + route key `list`), the real route name is `topdata.contact.login.list.list` — easy to mismatch when writing the `navigation[].path`.
2. **The sidebar is a one-shot snapshot** of the module registry taken when `sw-admin-menu` mounts. A navigation entry whose `path` does not resolve in the router crashes during render — `TypeError: Cannot read properties of undefined (reading 'href')` — and the entry silently never appears under its parent group.

## Usage / Correct Patterns

```js
// src/Resources/app/administration/src/module/my-plugin-module/index.js
import './page/my-plugin-page';

const { Module } = Shopware;

Module.register('my-plugin-module', {
    type: 'plugin',
    name: 'MyPlugin.module.name',
    title: 'MyPlugin.module.title',
    icon: 'regular:user',

    routePrefixName: 'my.plugin',
    routePrefixPath: 'my/plugin',

    routes: {
        list: {
            component: 'my-plugin-page',
            path: 'list',
        },
    },

    navigation: [{
        id: 'my-plugin-module',
        label: 'MyPlugin.module.title',
        icon: 'regular:user',
        path: 'my.plugin.list',          // = routePrefixName + '.' + routeKey
        parent: 'sw-customer',           // id of the core group's navigation entry
        position: 110,
    }],
});
```

Rules to verify:
- `navigation[].path` must be a **route name that actually exists** — `router.resolve(path)` is called at render and crashes on a miss.
- The generated route name is always `<prefix>.<routeKey>`; prefix = `routePrefixName` if set, otherwise the module id with `-` → `.`.
- Set `routePrefixName`/`routePrefixPath` whenever the module id ends in the route key, or contains segments you don't want in the URL/route name.
- A working sibling module in the same plugin is the best reference: diff your module config against it (same Shopware version, same build).

## Anti-patterns (DO NOT USE)

```js
// WRONG: relying on the default route name when the module id ends in the route key
Module.register('topdata-contact-login-list', {
    routes: { list: { component: 'x', path: 'list' } },
    navigation: [{
        id: 'topdata-contact-login-list',
        label: 'Kontakte',
        path: 'topdata.contact.login.list', // actual route name is 'topdata.contact.login.list.list'
        parent: 'sw-customer',
    }],
});
```

Do not:
- "Fix" a missing entry with timers/polling that re-hydrate the admin menu store or force route loads — the true bug is the unresolvable `path` (or an aborted registration).
- Re-register core modules (e.g. `Module.register('sw-customer', …)`) — the 6.7 module factory aborts duplicate module ids (console warn only).
- Guess route names from the navigation config — compute the prefix from `routePrefixName`/module id and append the route key.
