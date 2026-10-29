# Source Map: ThirtyBees Core and Docs

Use this file to jump straight to the authoritative code or documentation.
Paths are the git-digest clones; registry names are for `git-digest` tooling.

## 1. Clones

| Content | Registry name | Local path |
|---|---|---|
| Core (1.7.0+) | `thirtybees-thirtybees` | `/home/marc/devel/git-digest/repos/thirtybees-thirtybees` |
| Docs source (Jekyll) | `thirtybees-docs` | `/home/marc/devel/git-digest/repos/thirtybees-docs` |

Both clones are full git repositories (not shallow). Refresh before relying on
them:

```bash
git -C /home/marc/devel/git-digest/repos/thirtybees-thirtybees pull --ff-only
git -C /home/marc/devel/git-digest/repos/thirtybees-docs pull --ff-only
```

The core's `modules/` entries are git submodules. The clone may show them as
uninitialized (`-` prefix in `git submodule status`). Initialize one or more:

```bash
CORE=/home/marc/devel/git-digest/repos/thirtybees-thirtybees
git -C "$CORE" submodule update --init modules/bankwire modules/blockbestsellers modules/beesblog
```

Useful native modules to initialize: `bankwire` (payment), `blockbestsellers`
(hooks/config/cache/upgrade), `blockcart` (hook/JS), `beesblog` (ObjectModel,
admin tabs, front routes, custom hooks), `coreupdater` (admin tooling),
`themeconfigurator`, `blocklayered`.

## 2. Core files that answer most questions

| Question | File |
|---|---|
| Module lifecycle, hooks, `display()`, `l()`, paths | `classes/module/Module.php` |
| Payment order creation, `validateOrder()` | `classes/module/PaymentModule.php` |
| Front controller base | `classes/controller/ModuleFrontController.php` |
| Admin controller base | `classes/controller/ModuleAdminController.php` |
| Front page lifecycle, media, redirects | `classes/controller/FrontController.php` |
| Admin list/form/token behavior | `classes/controller/AdminController.php` |
| ObjectModel fields, hydration, CRUD | `classes/ObjectModel.php` |
| DB connection, queries, insert/update/delete | `classes/db/Db.php` |
| Query builder | `classes/db/DbQuery.php` |
| Settings key/value API | `classes/Configuration.php` |
| Request helpers, validation, redirects, cache | `classes/Tools.php`, `classes/Validate.php` |
| Hook registration, aliases, dispatch | `classes/Hook.php` |
| Admin tabs | `classes/Tab.php` |
| Admin form rendering | `classes/helper/HelperForm.php` |
| Module URLs | `classes/Link.php` (`getModuleLink()`) |
| Friendly routes | `classes/Dispatcher.php` (`moduleRoutes`) |
| Hook aliases (`payment` ↔ `displayPayment`) | `install-dev/data/xml/hook_alias.xml` |
| Core hook list | `install-dev/data/xml/hook.xml` |
| Module release packaging | `tools/buildmodule.sh` |
| Core tests (Codeception) | `tests/`, `TESTING.md`, `codeception.yml` |

## 3. Native module examples

| Pattern | Module |
|---|---|
| Payment module, payment/validation front controllers | `modules/bankwire/` |
| Hook module, `HelperForm`, Smarty cache, upgrade script | `modules/blockbestsellers/` |
| Hook + JS/AJAX, cart interaction | `modules/blockcart/` |
| Namespaced ObjectModels, autoloader, admin CRUD/tabs, front routes, custom hooks | `modules/beesblog/` |
| Admin tooling/updater | `modules/coreupdater/` |

Read the main class first, then the controllers and `views/templates/`
directory. Native modules are the best working examples for 1.7, but they are
not uniformly lint-clean: `bankwire`'s validation controller and `blockcart`'s
standalone scripts lack the `_TB_VERSION_` guard, and older library files may
omit it. Follow SKILL.md's rules, not every historical omission.

## 4. Docs repository

The docs clone is the Jekyll source behind <https://docs.thirtybees.com>.
Content lives under `thirtybees/`:

| Path | Content |
|---|---|
| `thirtybees/developers-guide/classes.md`, `controllers.md` | Generated class/controller API pointers |
| `thirtybees/developers-guide/api-classes.md`, `api-controllers.md` | Large generated API lists |
| `thirtybees/api/1.0/*.md` | Per-class/controller API reference |
| `thirtybees/native-modules/*.md` | Native module descriptions (not development guides) |
| `thirtybees/overview/changelog/v1_0_x_release_notes.md` | Old release notes; no 1.7 notes |
| `thirtybees/installation/`, `merchants-guide/`, `troubleshooting/` | Operations/merchant docs |
| `_includes/api/1.0/` | Snippets used by the API pages |

Docs caveat: there is no complete "write a module" guide in the docs, and the
developer pages are partly generated/outdated. Use them for class/controller
lookups, then confirm behavior in `classes/` and `modules/`.

External references (verify APIs against the TB source):

- PrestaShop 1.6 module docs: <https://devdocs.prestashop-project.org/1.6/modules/>
- thirty bees forum: <https://forum.thirtybees.com>
- thirty bees store: <https://store.thirtybees.com>

## 5. Search recipes

```bash
CORE=/home/marc/devel/git-digest/repos/thirtybees-thirtybees
DOCS=/home/marc/devel/git-digest/repos/thirtybees-docs

# Module class examples
rg -n "class .* extends (Module|PaymentModule)" "$CORE/modules" --glob '*.php'

# Hook implementations
rg -n "function hook[A-Z]" "$CORE/modules/bankwire" --glob '*.php'
rg -n "registerHook\(" "$CORE/modules/beesblog" --glob '*.php'

# Controllers
rg -n "class .*ModuleFrontController" "$CORE/modules" --glob '*.php'
rg -n "class .*ModuleAdminController" "$CORE/modules" --glob '*.php'

# Lifecycle / helpers
rg -n "function (install|uninstall|getContent|display|registerHook)\(" "$CORE/classes/module/Module.php"
rg -n "function validateOrder" "$CORE/classes/module/PaymentModule.php"
rg -n "function getModuleLink" "$CORE/classes/Link.php"
rg -n "function (createDatabase|dropDatabase)" "$CORE/classes/ObjectModel.php"

# ObjectModel definitions and upgrade scripts
rg -n "public static \$definition" "$CORE/modules" --glob '*.php'
rg -n "function upgrade_module_" "$CORE/modules" --glob '*.php'

# Admin tabs
rg -n "class_name.*Admin|Tab::getIdFromClassName" "$CORE/modules" --glob '*.php'

# Docs search
rg -n "hook|module|controller" "$DOCS/thirtybees/developers-guide" --glob '*.md'
rg -n "displayPayment|paymentReturn" "$DOCS/thirtybees" --glob '*.md'
```

## 6. When the clone is missing

If a configured git-digest path does not exist, use the git-digest registry
first (`thirtybees-thirtybees`, `thirtybees-docs`), then fall back to cloning:

```bash
git clone https://github.com/thirtybees/thirtybees.git
git clone https://github.com/thirtybees/docs.git
```

Do not fetch from random forks or third-party mirrors; the official organization
is `thirtybees`.
