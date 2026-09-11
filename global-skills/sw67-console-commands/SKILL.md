---
name: sw67-console-commands
description: Patterns and conventions for Shopware 6.7 console commands in Topdata plugins (Symfony). Use when creating, editing, or renaming a CLI command (class `Command_Xxx`, noun-first command name like `topdata:enhanced-search:synonym-suggestion:generate`), wiring it in services.xml, adding list/pagination output with `UtilCliPagination`, formatting date columns at minute precision, running commands in the focus-* Docker setup, or sanity-checking with php -l/xmllint.
---

# Shopware 6.7 Console Command Patterns (Topdata)

## Naming

- **Class/file:** `Command_<Name>` prefix, NOT a `<Name>Command` suffix. Examples: `Command_ExportProducts`, `Command_TranslateDatabase`, `Command_TdmpImport`.
- **Command name (AsCommand):** noun-first, verb-last: `topdata:<plugin>:<noun>:<verb>`. Example: `topdata:enhanced-search:synonym-suggestion:generate`. Keep plural/singular noun consistent with the surrounding sub-namespace.

## Registration (services.xml)

Console commands are NOT auto-registered by `#[AsCommand]` alone — add a `<tag name="console.command"/>`. Either autowire, or use explicit `key="$..."` arguments:

```xml
<service id="Topdata\ExamplePluginSW6\Command\Command_Import">
    <argument type="service" id="Doctrine\DBAL\Connection" key="$connection"/>
    <tag name="console.command"/>
</service>
```

Extend `Topdata\TopdataFoundationSW6\Command\AbstractTopdataCommand` and call `parent::__construct()`.

## Options

- Provide a short alias for frequently used options: `--debug`/`-d`, `--strategy`/`-s` (`addOption('strategy', 's', …)`).
- Options are registered via `addOption()` in `configure()` (Symfony `InputOption`), not `getInputDefinition()->addOption()`.

## Output & logging

- Use the `Topdata\TopdataFoundationSW6\Util\CliLogger` static facade: `CliLogger::info/warning/error/success/note`.
- Tables: `CliLogger::getCliStyle()->table($headers, $rows)` or a plain Symfony `Table`.

## List commands / pagination

- Provide `--limit` (default `50`) and `--offset` (default `0`) options.
- Total count first via `COUNT(*)` + `fetchOne()`, then the paged query with `setMaxResults/setFirstResult`.
- Print the `Showing X-Y of Z total <label>.` line through the shared helper:

```php
use Topdata\TopdataFoundationSW6\Util\UtilCliPagination;
// ...
$total = (int) $countQb->executeQuery()->fetchOne();
$rows  = $qb->executeQuery()->fetchAllAssociative();
CliLogger::getCliStyle()->table([...], $rows);
UtilCliPagination::renderSummary($output, $offset, $limit, $total, 'suggestions');
```

- `UtilCliPagination::formatSummary()` returns the string; `renderSummary()` also writes it.

## Date columns

List-command date columns render `created_at` at **minute precision** (`Y-m-d H:i`, no seconds/millis): `substr((string) $row['created_at'], 0, 16)`.

## Running commands in the focus-* Docker setup

- DB-dependent Shopware CLI must run inside the web container: `docker exec focus-www php bin/console <command> …` (host shell cannot resolve `focus-mariadb`).
- ES lives in the `focus-es` container, HTTP auth enabled.

## Validation

There is no CI/lint config in Topdata plugins. Sanity checks are:
- `php -l <file>.php`
- `xmllint --noout <services.xml>`