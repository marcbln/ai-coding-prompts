---
name: sw67-admin-entity-listing
description: |
  Patterns and gotchas for creating admin entity listing pages in Shopware 6.7 plugins. Use when creating a new admin list page, debugging a listing that loads forever, or fixing SQL errors about missing updated_at columns.

  Use this when:
  - Creating a new admin list page with `sw-entity-listing` and the `listing` mixin
  - Debugging an admin list page that "loads forever" (skeleton shows but no data)
  - Fixing SQL errors about missing `updated_at` column on a custom entity
  - Building admin assets for a plugin that aren't picked up by the build system
  - Creating entity definitions with the auto-added `UpdatedAtField` in SW 6.7
  - Creating migrations to add `updated_at` columns to custom entity tables
  - Adding modal-based edit/create with a reusable form component
  - Adding custom context menu actions (Edit/Delete) via the `#actions` slot
  - Debugging why the Edit button is missing from the context menu
  - Debugging why the Edit button navigates away instead of opening a modal
  - Debugging why `$t()` interpolation with `{variable}` shows empty strings
---

# SW67 Admin Entity Listing

Patterns for creating admin entity listing pages in Shopware 6.7 plugins. Covers the full stack: PHP entity definition, migration, administration component, and build.

## Quick Start

```
php bin/console make:administration:...        # SW CLI, if available
# Or manually:
src/Entity/Foo/FooEntityDefinition.php          # entity definition
src/Migration/Migration1753000000AddFoo.php     # migration
src/Resources/app/administration/src/module/... # admin component
```

## Entity Definition — The `updated_at` Gotcha

Shopware 6.7 auto-adds `CreatedAtField` and `UpdatedAtField` to **all** entity definitions (`EntityDefinition.php:445-448`). The DAL generates SELECT queries including `updated_at` for every read — even if your definition doesn't define it explicitly.

**Always add a migration** to add `updated_at` to your table:

```php
// Migration/Migration1752590000AddUpdatedAtToFooTable.php
public function update(Connection $connection): void
{
    $connection->executeStatement('
        ALTER TABLE `topdata_es_foo`
        ADD COLUMN `updated_at` DATETIME(3) NULL AFTER `created_at`
    ');
}
```

Without this migration, your list page crashes with:
`SQLSTATE[42S22]: Column not found: 1054 Unknown column 'topdata_es_foo.updated_at'`

## Admin Component — The `getList()` Pitfall

The `listing` mixin provides a **no-op stub** for `getList()`. You must implement it yourself.

See `references/component-patterns.md` for the full pattern.

## Admin Build

If `bin/build-administration.sh` doesn't pick up your plugin:

1. Check `var/plugins.json` — your plugin must be listed
2. If `bin/console bundle:dump` fails (DB unavailable), manually add the entry
3. The `basePath` must point to the directory containing `Resources/`, e.g. `custom/plugins/my-plugin/src/`
4. Run plugin build separately: `VITE_MODE=production npx ts-node -T build/plugins.vite.ts`

## Context Menu Actions — The `#actions` Slot

In SW 6.7's `sw-entity-listing`, the **`#actions` slot replaces all default context menu items**. When you use it, you must provide both Edit and Delete manually.

**Do NOT use `:detail-route` for modal editing** — it triggers `$router.push()` and navigates away. Instead, use `#actions` slot with custom `<sw-context-menu-item>` elements.

See `references/component-patterns.md` for:
- Full `#actions` slot pattern with modal-based Edit and custom Delete confirmation
- The `deleteConfirmText` computed property pattern (uses `$t()`, not `$tc()`)
- The `repository.get(id)` pattern for fetching writable entity proxies before editing

## Reusable Form Component

Extract inline modal forms into a reusable component to avoid code duplication:

```
component/my-form/
├── index.ts          # Component.register('topdata-es-my-form')
└── my-form.html.twig # Modal with form fields
```

The component accepts `entity` and `repository` as props, handles save internally, and emits `save`/`cancel` events.

See `references/component-patterns.md` for the full pattern.

## Snippet Gotcha — `$t()` vs `$tc()`

In SW 6.7 (Vue 3 / Vue I18n v9):
- **Use `$t(key, { variable: value })`** for message interpolation with named `{variable}` placeholders
- **Use `$tc()` only for pluralization** — its replacements parameter is not handled the same way

```ts
// ✅ Correct - interpolation works
this.$t('MyFancyPluginSW6.my-module.deleteConfirmText', { term: item.name })

// ❌ Wrong - replacements parameter may not be consumed
this.$tc('MyFancyPluginSW6.my-module.deleteConfirmText', 0, { term: item.name })

// ❌ Wrong - $tc already consumed {term} before .replace()
this.$tc('MyFancyPluginSW6.my-module.deleteConfirmText').replace('{term}', item.name)
```

```json
// Snippet — {term} is the named parameter
"MyFancyPluginSW6": {
    "my-module": {
        "deleteConfirmText": "Delete \"{term}\"?"
    }
}
```

## Related

- `_ai/lessons-learned.md` in this plugin — captures real debugging session
