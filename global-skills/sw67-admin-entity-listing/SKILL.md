---
name: sw67-admin-entity-listing
description: |
  Patterns and gotchas for creating admin entity listing pages in Shopware 6.7 plugins.

  Use this when:
  - Creating a new admin list page with `sw-entity-listing` and the `listing` mixin
  - Debugging an admin list page that "loads forever" (skeleton shows but no data)
  - Fixing SQL errors about missing `updated_at` column on a custom entity
  - Building admin assets for a plugin that aren't picked up by the build system
  - Creating entity definitions with the auto-added `UpdatedAtField` in SW 6.7
  - Creating migrations to add `updated_at` columns to custom entity tables
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

## Related

- `_ai/lessons-learned.md` in this plugin — captures real debugging session
