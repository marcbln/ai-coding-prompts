# Module Lifecycle, Hooks, Templates, and Configuration

Source anchors (in the git-digest core clone):

- `classes/module/Module.php` — lifecycle, hooks, `display()`, `l()`, paths
- `classes/helper/HelperForm.php` — admin form rendering
- `modules/blockbestsellers/blockbestsellers.php` — hooks, config form, cache
- `modules/bankwire/bankwire.php` — payment module variant
- `modules/beesblog/beesblog.php` — custom hooks, tabs, multilang settings

## 1. Directory layout

```
modules/mymodule/
├── mymodule.php                 # main class, MUST match folder name
├── index.php                    # guard
├── config.xml                   # optional; TB auto-generates it from the class
├── controllers/
│   ├── front/                   # <module><Controller>ModuleFrontController
│   ├── admin/                   # Admin<Controller>Controller
│   └── index.php
├── classes/                     # ObjectModel classes / services
├── upgrade/
│   └── upgrade-1.0.1.php        # upgrade_module_1_0_1($module)
├── translations/                # generated <iso>.php translation files
├── views/
│   ├── css/ js/ img/
│   └── templates/
│       ├── hook/                # hook templates
│       ├── front/               # module front controller templates
│       └── admin/               # module admin controller templates
```

`config.xml` is optional. `Module::getModulesOnDisk()` instantiates the class and
generates/refreshes `config.xml` when it is missing or older than the main PHP
file. `.tbstore.yml` is only needed to publish to the thirty bees store; it is
not read by the shop runtime.

## 2. Main class contract

The main file must be `modules/<name>/<name>.php`, and its class name must equal
the module name case-insensitively. `Module::instantiateModule()` calls
`class_exists($moduleName, false)`; `Validate::isModuleName()` permits only
`[a-zA-Z0-9_-]+`. A hyphen is a valid folder name but not a valid PHP class name,
so use lowercase letters/digits/underscore.

```php
<?php
/**
 * Example module for thirty bees.
 *
 * @author    Your Company
 * @copyright 2026 Your Company
 * @license   AFL-3.0
 */

if (!defined('_TB_VERSION_')) {
    exit;
}

class Mymodule extends Module
{
    public function __construct()
    {
        $this->name = 'mymodule';
        $this->tab = 'front_office_features';
        $this->version = '1.0.0';
        $this->author = 'Your Company';
        $this->need_instance = 0;   // 1 if the constructor needs a DB/context
        $this->bootstrap = true;    // modern admin UI
        $this->controllers = ['demo']; // front controller names

        parent::__construct();      // loads id/active/version from DB

        $this->displayName = $this->l('My module');
        $this->description = $this->l('Short description shown in the module list.');
        $this->confirmUninstall = $this->l('Remove all module settings?');
        $this->tb_min_version = '1.5.0';
        $this->tb_versions_compliancy = '>= 1.5.0';
    }
}
```

Set `$this->name` **before** `parent::__construct()`. Set user-facing strings
after it. `$need_instance = 0` keeps the module list fast when the constructor
has no side effects. `$this->bootstrap = true` enables the Bootstrap admin skin.

Useful metadata properties (all optional): `$tb_min_version`,
`$tb_versions_compliancy` (e.g. `'>= 1.5.0 < 2.0.0'`), `$ps_versions_compliancy`,
`$dependencies` (array of module names that must be installed first),
`$limited_countries`, `$currencies`, `$currencies_mode`, `$is_eu_compatible`,
`$badges`, `$warning`, `$description_full`, `$additional_description`.

## 3. Install / uninstall

`Module::install()` already does the heavy lifting: name validation, TB
compliancy, dependency checks, override installation, controller registration
(from `$this->controllers`), the `module` DB row, shop enablement, permissions,
and group restrictions. Your `install()` adds hooks, tables, settings, and tabs.

```php
public function install()
{
    if (!parent::install()) {
        return false;
    }

    if (!$this->registerHook('displayHome')
        || !$this->registerHook(['displayHeader', 'actionFrontControllerSetMedia'])
    ) {
        return false;
    }

    Configuration::updateValue('MYMODULE_ENABLED', 1);
    Configuration::updateValue('MYMODULE_TEXT', $this->l('Hello'));

    return true;
}

public function uninstall()
{
    return Configuration::deleteByName('MYMODULE_ENABLED')
        && Configuration::deleteByName('MYMODULE_TEXT')
        && parent::uninstall();
}
```

`registerHook()` accepts one name or an array. It returns `false` only in edge
cases; a typo in the hook method is logged and **skipped silently**, so run
`scripts/check-module.sh`.

`parent::uninstall()` unregisters hooks, deletes controller meta entries,
disables the module, deletes permissions/restrictions, and removes the module
row. It does **not** remove `Configuration` values, custom hooks, tabs, or
tables — clean those up yourself, before or after `parent::uninstall()`.

If a module creates admin tabs, delete them in `uninstall()`:

```php
$tabId = (int) Tab::getIdFromClassName('AdminMyModule');
if ($tabId) {
    (new Tab($tabId))->delete();
}
```

If a module supports reset-without-data-loss, expose a `reset()` method that
calls `$this->uninstall(false)` then `$this->install(false)`
(mirror the pattern in `modules/beesblog/beesblog.php`).

## 4. Hooks

Hook method naming is `hook` + hook name. PHP method names are
case-insensitive, but match the canonical camelCase for readability:

```php
public function hookDisplayHome()
{
    $this->context->smarty->assign([
        'mymodule_text' => Configuration::get('MYMODULE_TEXT'),
    ]);

    return $this->display(__FILE__, 'display_home.tpl');
}
```

`display($file, $template, $cacheId = null, $compileId = null)` uses
`basename($file, '.php')` as the module name. Template resolution order:

1. `themes/<theme>/modules/<module>/<template>`
2. `themes/<theme>/modules/<module>/views/templates/hook/<template>`
3. `themes/<theme>/modules/<module>/views/templates/front/<template>`
4. `modules/<module>/views/templates/hook/<template>`
5. `modules/<module>/views/templates/front/<template>`
6. `modules/<module>/<template>`

Keep hook templates in `views/templates/hook/` and front templates in
`views/templates/front/`.

Common hook return shapes:

- `display*` (e.g. `displayHome`, `displayHeader`, `displayFooter`) — HTML string.
- `action*` — side effect, usually no return (some expect an array).
- `displayPayment` (legacy alias `payment`) — HTML string; `displayPaymentEU` — array with
  `cta_text`, `logo`, `action`.
- `paymentReturn` — HTML string; receives `objOrder`, `total_to_pay`,
  `currencyObj`.
- `moduleRoutes` — array of route definitions (see controllers reference).

Custom hooks: create a `Hook` row on install and delete it on uninstall.

```php
$hook = new Hook();
$hook->name = 'displayMyModuleExtra';
$hook->title = 'My module extra content';
$hook->description = 'Rendered on the product page';
$hook->position = 1;
$hook->live_edit = false;
$hook->add();
```

Then `registerHook('displayMyModuleExtra')` and implement
`hookDisplayMyModuleExtra()`.

### Hook caching

```php
public function hookDisplayHome()
{
    $cacheId = $this->getCacheId('mymodule-home');

    if (!$this->isCached('display_home.tpl', $cacheId)) {
        $this->context->smarty->assign('items', $this->getItems());
    }

    return $this->display(__FILE__, 'display_home.tpl', $cacheId);
}
```

Invalidate with `Tools::clearCache($this->context->smarty, $this->getTemplatePath('display_home.tpl'), $cacheId)`
when the underlying data changes. `modules/blockbestsellers/blockbestsellers.php`
shows the full pattern, including clearing on product/order changes.

## 5. Templates and translations

Templates are Smarty `.tpl` files (no Twig in TB 1.7).

```smarty
<div class="block mymodule">
  <h4>{l s='My module' mod='mymodule'}</h4>
  <p>{$mymodule_text|escape:'htmlall':'UTF-8'}</p>
  <a href="{$link->getModuleLink('mymodule', 'demo', [], true)|escape:'htmlall':'UTF-8'}">
    {l s='Open demo page' mod='mymodule'}
  </a>
</div>
```

- `{l s='...' mod='mymodule'}` in templates; `$this->l('...')` in PHP.
- `{$module_dir}` is assigned by `display()`; it points at the module URI.
- Escape all dynamic output. Use `|intval` for IDs, `|escape:'htmlall':'UTF-8'`
  (or `:'html':'UTF-8'`) for text and URLs.
- Translation files live in `modules/<module>/translations/<iso>.php` (or a
  theme override). Generate/update them with TB's translation tooling or
  `Language::updateModulesTranslations([$module])`; do not hand-edit generated
  files unless the project already does.
- `Tools::getValue()` returns request data; validate with `Validate` and cast
  before using it in SQL or output.

## 6. Admin configuration page (`getContent`)

`getContent()` is what the Module Manager's **Configure** button renders. The
standard pattern is `Tools::isSubmit()` → validate → `Configuration::updateValue()`
→ `HelperForm`.

```php
public function getContent()
{
    $output = '';

    if (Tools::isSubmit('submitMymodule')) {
        $text = Tools::getValue('MYMODULE_TEXT');

        if (!is_string($text) || trim($text) === '') {
            $output .= $this->displayError($this->l('Text is required.'));
        } else {
            Configuration::updateValue('MYMODULE_TEXT', $text);
            $output .= $this->displayConfirmation($this->l('Settings updated.'));
        }
    }

    return $output.$this->renderForm();
}

protected function renderForm()
{
    $fieldsForm = [
        'form' => [
            'legend' => [
                'title' => $this->l('Settings'),
                'icon'  => 'icon-cogs',
            ],
            'input' => [
                [
                    'type'     => 'text',
                    'label'    => $this->l('Text'),
                    'name'     => 'MYMODULE_TEXT',
                    'required' => true,
                ],
                [
                    'type'    => 'switch',
                    'label'   => $this->l('Enabled'),
                    'name'    => 'MYMODULE_ENABLED',
                    'is_bool' => true,
                    'values'  => [
                        ['id' => 'on', 'value' => 1, 'label' => $this->l('Yes')],
                        ['id' => 'off', 'value' => 0, 'label' => $this->l('No')],
                    ],
                ],
            ],
            'submit' => ['title' => $this->l('Save')],
        ],
    ];

    $helper = new HelperForm();
    $helper->show_toolbar = false;
    $helper->table = $this->table;
    $helper->default_form_language = (int) Configuration::get('PS_LANG_DEFAULT');
    $helper->allow_employee_form_lang = (int) Configuration::get('PS_BO_ALLOW_EMPLOYEE_FORM_LANG');
    $helper->identifier = $this->identifier;
    $helper->submit_action = 'submitMymodule';
    $helper->currentIndex = $this->context->link->getAdminLink('AdminModules', false)
        .'&configure='.$this->name.'&tab_module='.$this->tab.'&module_name='.$this->name;
    $helper->token = Tools::getAdminTokenLite('AdminModules');
    $helper->tpl_vars = [
        'fields_value' => [
            'MYMODULE_TEXT'    => Tools::getValue('MYMODULE_TEXT', Configuration::get('MYMODULE_TEXT')),
            'MYMODULE_ENABLED' => (int) Tools::getValue('MYMODULE_ENABLED', Configuration::get('MYMODULE_ENABLED')),
        ],
        'languages'   => $this->context->controller->getLanguages(),
        'id_language' => $this->context->language->id,
    ];

    return $helper->generateForm([$fieldsForm]);
}
```

For multi-language settings, pass an array keyed by language ID to
`Configuration::updateValue($key, $values)` and set `'lang' => true` on the form
field. `HelperOptions` + `generateOptions($optionList)` is available for grouped
checkbox/radio/select option pages (see `BeesBlog::renderDisqusOptions()`);
`bankwire` and `blockbestsellers` show the simpler `HelperForm` style.

## 7. Security checklist

- Add the `_TB_VERSION_` guard to every entry-point PHP file; prefer it for
  library/class files too, and add `index.php` guards to web-facing directories.
- Use `Tools::getValue()` / `Tools::isSubmit()`; never read `$_GET`/`$_POST`
  directly when a framework helper exists.
- Cast numeric values: `(int)`, `(float)`, `(bool)`.
- Escape output in Smarty; use `pSQL()` for string literals and prefer
  `DbQuery`/prepared-style helpers for SQL.
- Admin forms: keep the `HelperForm` token/currentIndex logic for CSRF
  protection. Front forms: validate tokens/hashes for state-changing requests.
- Do not expose secrets in templates, logs, or `Configuration` values printed
  in the admin UI.
