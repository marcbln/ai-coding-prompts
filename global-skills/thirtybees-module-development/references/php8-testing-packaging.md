# PHP 8.x Compatibility, Testing, and Packaging

Source anchors:

- `README.md` in the core clone — supported PHP versions
- `classes/module/Module.php` — install/upgrade mechanics
- `tests/`, `TESTING.md`, `codeception.yml` — core test harness (not a module harness)
- `tools/buildmodule.sh` — release packaging
- `modules/bankwire`, `modules/beesblog` — modern PHP 8-compatible module code

## 1. Supported runtimes

- TB 1.7: PHP 7.4 – 8.3 (verified in the 1.7.0 `README.md`).
- TB 1.6: PHP 7.4 – 8.3.
- TB 1.5: PHP 7.4 – 8.1.
- The shop-hotfixes project targets PHP 8.2+; a module that must also run on TB
  1.5 should stay within PHP 7.4 syntax (no union types, `mixed`, `never`,
  enums, readonly properties, or constructor property promotion).

Use `declare(strict_types=1);` only in new files when the whole call path is
type-clean. In legacy modules it can turn previously-coerced values into
`TypeError`s. Typed properties (PHP 7.4) are fine; uninitialized typed
properties throw on read, so initialize them.

## 2. PHP 8.0–8.3 pitfalls

| Removed / deprecated | Replacement |
|---|---|
| `create_function()` (8.0 removed) | closure / arrow function |
| `each()` (8.0 removed) | `foreach` |
| `get_magic_quotes_gpc()`, `set_magic_quotes_runtime()` (8.0 removed) | remove |
| `money_format()` (8.0 removed) | `NumberFormatter` / `sprintf` |
| `$str{0}` curly offsets (8.0 removed) | `$str[0]` |
| `define('X', ..., true)` case-insensitive constants (8.0 removed) | normal constants |
| `strftime()` (8.1 deprecated) | `date()` / `IntlDateFormatter` |
| Passing `null` to non-nullable internal params (8.1 deprecation) | coalesce/cast before the call |
| `utf8_encode()` / `utf8_decode()` (8.2 deprecated) | `mb_convert_encoding()` |
| `${var}` string interpolation (8.2 deprecated) | `{$var}` |
| Dynamic properties (8.2 deprecation) | declare properties |
| `FILTER_SANITIZE_STRING` (8.1 deprecated) | `htmlspecialchars()` / `strip_tags()` |
| `get_class()` / `get_parent_class()` without argument (8.3 deprecation) | pass the object/class |
| `Serializable` interface without `__serialize`/`__unserialize` (8.1) | implement both |

Practical checks:

- Declare every `ObjectModel` field as a public property; otherwise hydration
  creates dynamic properties and PHP 8.2 logs deprecations.
- Cast request data before using it: `(int) Tools::getValue('id')`,
  `(float) Tools::getValue('amount')`. `Tools::getValue()` returns `false` when
  missing, which becomes `0`/`''` under casts.
- Check `Validate::isLoadedObject()` before using an object; do not rely on
  truthiness of an ID.
- Avoid `@` error suppression; handle the failure path.
- Do not use `Tools::displayError()` for new user-facing errors; use
  `$this->displayError()` in config pages, `$this->errors[]` in admin
  controllers, and `Logger::addLog()` for diagnostics.

## 3. Validate module structure

Run the bundled checker first:

```bash
scripts/check-module.sh /path/to/shop/modules/mymodule
```

It checks:

- main file exists and class name matches the folder (case-insensitive),
- entry-point PHP files have the `_TB_VERSION_` guard (library files are warned),
- web-facing directories have an `index.php` guard (missing ones are warned),
- `php -l` passes for every PHP file,
- every registered hook has a matching `hook<Name>` method,
- versions and upgrade files are ordered/consistent.

Then run the broader PHP 8 scan if the shop-hotfixes tools are available:

```bash
/topdata/shop-hotfixes/tools/php8-tools/scan.sh /path/to/shop/modules/mymodule
```

## 4. Install and smoke-test in a shop

Do not install or upgrade modules on production unless the user explicitly asks.

1. Copy or symlink the module into the shop's modules directory:
   - default layout: `<shop>/modules/mymodule/`
   - shop-hotfixes Docker layout: `<shop>/vol/www/public/modules/mymodule/`
2. Clear cache. Use the shop's helper if present, otherwise TB admin →
   Advanced Parameters → Performance → Clear cache, or remove the generated
   Smarty/cache directories in a dev copy:
   ```bash
   rm -rf <shop>/cache/smarty/cache/* <shop>/cache/smarty/compile/* <shop>/cache/cachefs/*
   ```
   In shop-hotfixes checkouts, `scripts/clear-cache.sh` does this.
3. Install from the admin Module Manager, or on a development bootstrap:
   ```php
   $module = Module::getInstanceByName('mymodule');
   if (!$module || !$module->install()) {
       // inspect $module->_errors
   }
   ```
4. Smoke-test the full matrix:
   - module appears with correct display name/description/version,
   - install → configure/save → hooks render on the expected pages,
   - front controller URL works (HTTP and HTTPS if `$ssl = true`),
   - admin tab loads, list/filter/edit/delete work,
   - uninstall removes hooks/settings/tables (and does not fatal),
   - reinstall works,
   - upgrade from the previous version runs and keeps data,
   - module disabled / user without permission / empty cart / bad request
     paths behave gracefully,
   - no new warnings or deprecations in the log with dev mode enabled on a dev
     copy.
5. Repeat on the lowest supported TB/PHP combination if 1.5/1.6 compatibility
   is claimed. APIs can differ; check the tag's source with
   `git -C <core> show 1.5.1:classes/module/Module.php`.

## 5. Versioning and upgrades

- Bump `$this->version` in the main class for every release.
- Add `upgrade/upgrade-<version>.php` for schema data or settings changes; see
  [database-objectmodel.md](database-objectmodel.md).
- The installed version in the `module` table is compared to the class version;
  TB runs only upgrade files with `file_version > registered_version` and
  `file_version <= module_version`.
- A failed upgrade returns `false`, which disables the module and records the
  failing version — always test upgrades on a copy of the data.
- Do not edit or renumber shipped upgrade files.

## 6. Packaging

From the module's git repository root:

```bash
/home/marc/devel/git-digest/repos/thirtybees-thirtybees/tools/buildmodule.sh
# or, outside the core clone, copy tools/buildmodule.sh into the module repo
# and run it from there
```

- Defaults to the latest git tag; pass a tag/branch/commit to package another
  revision.
- Creates `<module>-v<version>.zip` containing a `<module>/` prefix.
- Excludes `.gitignore`, `.gitmodules`, `composer.json`, `composer.lock`,
  `README.md`, `LICENSE.md`, `build.sh`, `.tbstore.yml`, `.tbstore/`, `docs/`,
  `tests/`, `examples/`, `unitTests/`, `vagrant/`.
- `config.xml` is generated by TB from the module class; do not hand-maintain it
  unless the project already does.
- `.tbstore.yml` and `.tbstore/` describe the store listing (name, category,
  tags, images, PHP versions) and are excluded from the ZIP.
- The release ZIP is what merchants upload/install; verify it contains the main
  class, `controllers/`, `views/`, `upgrade/`, `translations/`, and any
  assets/vendor files the module loads at runtime.

## 7. Compatibility checklist

- [ ] `_TB_VERSION_` guard in entry-point PHP files; `index.php` guards in web-facing directories.
- [ ] Main class name matches folder, extends `Module`/`PaymentModule`.
- [ ] `parent::install()` / `parent::uninstall()` used correctly.
- [ ] All hooks registered and implemented.
- [ ] `$this->controllers` matches `controllers/front|admin` files.
- [ ] Templates in the correct `views/templates/{hook,front,admin}` directory.
- [ ] `$this->l()` / `{l s='...' mod='...'}` used, output escaped.
- [ ] SQL uses casts/`pSQL`/`DbQuery`; no raw request interpolation.
- [ ] Settings deleted on uninstall; tables dropped only when intended.
- [ ] Version bumped + upgrade script for schema/data changes.
- [ ] `scripts/check-module.sh` passes; `php -l` passes; smoke test passed on
      the target TB/PHP versions.
