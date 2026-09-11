---
name: sw67-migrations
description: |
  Patterns and gotchas for creating Shopware 6.7 plugin migrations. Use when adding a migration in a Topdata SW 6.7 plugin (new entity table, schema change, data backfill), or when deciding whether the plugin version needs a bump. MANDATORY rule covered here: every new migration class requires a `version` bump in `composer.json` in the same change, otherwise the plugin update lifecycle never fires and the migration silently never runs.

  Use this when:
  - Creating a new migration (`src/Migration/...`)
  - Adding/editing `composer.json` `version` for an sw67 plugin
  - Bumping the plugin version because a migration was added
  - Debugging why a migration never executed after deploy
  - Porting migration code to DBAL 4.x / SW 6.7 helpers
---

# Shopware 6.7 Plugin Migration Patterns

## The Rule: Every New Migration Requires a `composer.json` Version Bump

**Whenever a migration is created in an sw67 plugin, bump `version` in `composer.json` in the SAME commit/change.**

```jsonc
// composer.json
{
    "name": "topdata/topdata-example-plugin-sw6",
    "version": "1.2.4",   // ← bump this (1.2.4 → 1.3.0 or at least a patch bump)
    // ...
}
```

### Why mandatory

Shopware runs pending plugin migrations during the plugin install/update lifecycle
(`PluginLifecycleService`, triggered by `bin/console plugin:update <Plugin>` or the combined
update command in the Topdata setup). The update lifecycle is only triggered when the installed
version (stored in the `plugin` table) differs from the `version` in `composer.json`.

If you ship a new migration **without** bumping the version:

1. Deploy pushes the new code (which depends on the new column/table/data).
2. The update step sees "plugin already at this version" → skips the migration.
3. The `migration` table still lacks the new class → it will not run later on its own.
4. Runtime SQL errors (`Unknown column ...`, `Table ... doesn't exist`, missing backfilled rows).

The matching code and the migration **must ship atomically with the version bump**, or the shop
can end up with new code against an un-migrated schema.

### Mechanics after the bump

- The migration runs on the next `plugin:update`/`cpup` for the plugin.
- Executed migrations are tracked per class in the `migration` table; a new class (not recorded)
  is executed in creation-timestamp order.
- In the focus-* Docker setup, run from the web container: `docker exec focus-www php bin/console plugin:update <TechnicalName>` (host shell cannot resolve `focus-mariadb`).

## Migration Scaffolding

```
src/Migration/Migration<unixTimestamp><CamelCaseDescription>.php
```

```php
<?php declare(strict_types=1);

namespace Topdata\TopdataExamplePluginSW6\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class Migration1753000000AddFoo extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1753000000; // unique, ascending unix timestamp
    }

    public function update(Connection $connection): void
    {
        $connection->executeStatement('CREATE TABLE ...');
    }

    public function updateDestructive(Connection $connection): void
    {
        $connection->executeStatement('DROP TABLE ...');
    }
}
```

- Class/file name: `Migration` + timestamp merged with a CamelCase description (`Migration1753000000AddFoo`).
- `getCreationTimestamp()`: use a **unique, ascending** unix timestamp — it determines execution order.

## Gotchas

- **SW 6.7 validates the timestamp**: `getCreationTimestamp()` must be between `1` and `2147483647`
  (max int on 32-bit systems). Higher values silently collapse to max_int, so multiple migrations can
  end up with the same timestamp and execution order becomes random.
- **Never edit an executed migration.** Once a migration class is in the `migration` table it will not
  re-run. Ship a NEW migration (with another version bump) instead of fixing a shipped one.
- **SW 6.7 clears plugin migrations before `uninstall()`**: the plugin can be reinstalled and its
  migrations re-run, so keep `updateDestructive()` symmetric with `update()`.
- **SW 6.5 removed the trigger helpers**: `addForwardTrigger()`, `addBackwardTrigger()` and
  `addTrigger()` are gone — use `createTrigger()` instead (mind 6.5-era `system_config.value` → `configuration_value` renames).
- **6.6/6.7 renamed helper parameters**: `dropColumnIfExists($column)` → `$columnName`,
  `dropForeignKeyIfExists($column)` → `$foreignKeyName`, `dropIndexIfExists($index)` → `$indexName`.
  A positional call still works, named-argument call sites must use the new names.
- **DBAL 4.x**: `Connection` value binding, `executeStatement()`/`fetch*()` return types and the
  `ParameterType` enum (not int) follow DBAL 4.x rules — see the `common-doctrine-dbal-4.x-pitfalls` skill.
- **Removed CLI**: `CreateSchemaCommand`/`SchemaGenerator` are gone in 6.7 — use
  `CreateMigrationCommand`/`MigrationQueryGenerator` instead.

## Anti-patterns

- ❌ Adding a migration class but NOT bumping `version` in `composer.json` — the migration silently never runs.
- ❌ Bumping the version several commits AFTER the migration/update call lands — the first deploy skips it.
- ❌ Editing an already-executed migration to "fix" it — it won't re-run; add a new migration.
- ❌ Reusing a timestamp from an existing migration — execution order becomes non-deterministic.
- ❌ Skipping a version bump "because the migration is trivial" (`ADD COLUMN`, backfill, index) — the lifecycle fires per version, not per change size.

## Quick Checklist When Adding a Migration

- [ ] New class: `src/Migration/Migration<timestamp><Description>.php` extends `MigrationStep`
- [ ] `getCreationTimestamp()` is unique, ascending, within `1 .. 2147483647`
- [ ] `update()` and `updateDestructive()` are symmetric
- [ ] `version` in `composer.json` is bumped in the same change as the migration
- [ ] Migrations run via plugin update in the focus-* Docker: `docker exec focus-www php bin/console plugin:update <TechnicalName>`
- [ ] `php -l` on the migration class

## Related

- `sw67-entity-definition` — entity definitions + the mandatory `updated_at` column migration
- `sw67-admin-entity-listing` — list pages that crash when the `updated_at` migration is missing
- `common-doctrine-dbal-4.x-pitfalls` — DBAL 4.x query patterns used inside migrations
- `update-plugin-to-sw67` — full 6.6/6.7 upgrade workflow and UPGRADE-6.x references