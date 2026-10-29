---
name: thirtybees-module-development
description: |
  Build, modify, debug, and package thirty bees (ThirtyBees) modules — called
  plugins outside PrestaShop circles — against TB 1.7, while staying compatible
  with TB 1.5+. Use when creating a module, adding hooks, an admin config page,
  front/admin controllers, ObjectModel tables, payment modules, upgrade scripts,
  Smarty templates or translations, or fixing PHP 8.x compatibility. Covers
  naming, lifecycle, security, packaging, and verifying APIs against the
  git-digest copies of thirtybees/thirtybees and thirtybees/docs.

  Use this when:
  - Creating a new module under `modules/`
  - Adding hooks or debugging a hook that never fires
  - Building `getContent()` configuration pages
  - Adding front controllers, routes, or payment flows
  - Adding admin controllers and `Tab` entries
  - Creating ObjectModels, DB tables, or upgrade scripts
  - Porting a PrestaShop 1.6 module or fixing PHP 8.2/8.3 issues

---

# ThirtyBees Module (Plugin) Development

## Overview

ThirtyBees is a maintained fork of PrestaShop 1.6.1.11. Its "plugins" are still
called **modules**: a directory under `modules/<name>/` with a main
`<name>.php` class extending `Module` (or `PaymentModule`). Most PrestaShop 1.6
module knowledge applies, but the 1.7 source is the authority — verify every API
before using it.

## Source of truth (git-digest)

Read the real code before writing any module. Do not trust memory or old
tutorials for method signatures.

| Repo | Registry name | Local path |
|---|---|---|
| Core source (1.7.0+) | `thirtybees-thirtybees` | `/home/marc/devel/git-digest/repos/thirtybees-thirtybees` |
| Docs source (Jekyll) | `thirtybees-docs` | `/home/marc/devel/git-digest/repos/thirtybees-docs` |

Core module examples live in the core clone under `modules/`. They are git
submodules; initialize the ones you need:

```bash
CORE=/home/marc/devel/git-digest/repos/thirtybees-thirtybees
git -C "$CORE" submodule update --init modules/bankwire modules/blockbestsellers modules/beesblog
```

Already-initialized reference modules: `bankwire` (payment), `blockbestsellers`
(hooks/config/cache/upgrade), `blockcart` (hook/JS), `beesblog` (ObjectModel,
admin controllers, front routes, custom hooks, multilang/multishop),
`coreupdater` (admin tooling).

Refresh the clones before a long task:
```bash
git -C /home/marc/devel/git-digest/repos/thirtybees-thirtybees pull --ff-only
git -C /home/marc/devel/git-digest/repos/thirtybees-docs pull --ff-only
```

Docs caveat: `thirtybees/developers-guide/` and `thirtybees/api/1.0/` are useful
class/controller references, but the docs are incomplete and partly outdated
(no 1.7 release notes). When docs and source disagree, **source wins**.

See [references/source-map.md](references/source-map.md) for key files and
search recipes.

## Workflow

1. **Pick the module type and name.** Lowercase module name; no hyphens (the
   class name must match the folder name case-insensitively). Decide between a
   display/hook module, admin configuration module, CRUD/admin module, or
   payment module.
2. **Scaffold** with `scripts/new-module.sh <name> [modules-dir]` or copy
   `assets/module-skeleton/` manually. Replace every `__PLACEHOLDER__`.
3. **Implement the main class** — constructor metadata, `install()`,
   `uninstall()`, hook methods, `getContent()`. Follow
   [references/module-lifecycle.md](references/module-lifecycle.md).
4. **Add surface area as needed:**
   - Front controllers / routes:
     [references/controllers-routing.md](references/controllers-routing.md)
   - Admin controllers and `Tab` entries: same reference
   - `ObjectModel`, tables, upgrades:
     [references/database-objectmodel.md](references/database-objectmodel.md)
   - Payment flow: [references/payment-modules.md](references/payment-modules.md)
5. **Validate:** `scripts/check-module.sh <module-dir>`, `php -l` on touched
   files, then install and smoke-test in a TB shop. See
   [references/php8-testing-packaging.md](references/php8-testing-packaging.md).
6. **Bump the module version and add an upgrade script** for every schema or
   settings change: `upgrade/upgrade-<version>.php` containing
   `upgrade_module_<version_underscored>($module)`.
7. **Package** with the core's `tools/buildmodule.sh` (run from the module git
   repo root), or copy the directory for a local install.

## Non-negotiable rules

- **Class name = folder name**, case-insensitively (`modules/foo/foo.php`,
  `class Foo extends Module`). `Module::instantiateModule()` does
  `class_exists($moduleName)`, so a mismatched or hyphenated name fails to load.
- **Guard entry-point PHP files** (main class, controllers, upgrade scripts,
  standalone AJAX/CLI scripts) with:
  ```php
  if (!defined('_TB_VERSION_')) {
      exit;
  }
  ```
  Add the same guard to library/class files where practical, and an `index.php`
  guard to web-facing directories. Native modules are inconsistent here; follow
  the rule, not every historical omission.
- **Call `parent::install()` first**, then register hooks / create tables /
  settings. Check every return value; return `false`, do not throw.
- **Register every hook you implement** and implement every hook you register.
  `registerHook()` logs an error and silently skips registration when the
  `hook<Name>` method is missing.
- **Do not edit core.** Use hooks, module overrides (`override/` via
  `installOverrides()`) only as a last resort.
- **Escape and validate.** Smarty: `|escape:'htmlall':'UTF-8'`; PHP: cast IDs to
  `(int)`, use `pSQL()`/`DbQuery` parameters, never interpolate request data into
  SQL. Admin forms use the framework's token helpers.
- **No Composer autoload by default.** TB does not load a module's
  `vendor/autoload.php`. Use `require_once` or a small
  `spl_autoload_register` (see `modules/beesblog/classes/autoload.php`).
- **Keep 1.5+ compatibility** unless the user explicitly targets 1.7 only.
  Prefer APIs present across TB 1.5–1.7; avoid PS 1.6-only or 1.7-only helpers.

## Reference index

| File | Contents |
|---|---|
| [references/module-lifecycle.md](references/module-lifecycle.md) | Main class, metadata, install/uninstall, hooks, templates, translations, caching, `getContent()` |
| [references/controllers-routing.md](references/controllers-routing.md) | Front controllers, `getModuleLink`, `moduleRoutes`, admin controllers, `Tab` registration |
| [references/database-objectmodel.md](references/database-objectmodel.md) | `ObjectModel` definitions, `Db`/`DbQuery`, tables, multishop/multilang, upgrade scripts |
| [references/payment-modules.md](references/payment-modules.md) | `PaymentModule`, payment/validation controllers, `validateOrder`, hooks, provider callbacks |
| [references/php8-testing-packaging.md](references/php8-testing-packaging.md) | PHP 8.2/8.3 pitfalls, install/smoke tests, packaging, 1.5–1.7 compatibility |
| [references/source-map.md](references/source-map.md) | Exact core/docs paths, key files, grep recipes, docs coverage |

## Bundled resources

- `assets/module-skeleton/` — working generic module with hook, front controller,
  config form, templates, guards, and upgrade directory.
- `scripts/new-module.sh` — copies the skeleton, substitutes placeholders, and
  validates the generated PHP.
- `scripts/check-module.sh` — validates class/folder naming, `_TB_VERSION_`
  guards, `index.php` guards, `php -l`, hook registration, and upgrade/version
  consistency.

## Validation

```bash
# Syntax + structure checks
scripts/check-module.sh /path/to/shop/modules/mymodule

# Quick syntax-only pass
find /path/to/shop/modules/mymodule -name '*.php' -exec php -l {} \;

# Optional PHP 8 compatibility scan (shop-hotfixes repo)
tools/php8-tools/scan.sh /path/to/shop/modules/mymodule
```

Installing a module changes the shop database. Do not install on production
unless the user explicitly asks. Use a local/dev shop and clear the Smarty
cache after code or template changes.
