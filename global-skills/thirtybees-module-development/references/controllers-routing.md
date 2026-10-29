# Front Controllers, Routes, and Admin Controllers

Source anchors:

- `classes/controller/ModuleFrontController.php`
- `classes/controller/ModuleAdminController.php`
- `classes/controller/FrontController.php`, `AdminController.php`
- `classes/Link.php` (`getModuleLink()`)
- `classes/Dispatcher.php` (`moduleRoutes` handling)
- `modules/bankwire/controllers/front/` — payment front controllers
- `modules/beesblog/controllers/front/` — routes, pagination, ObjectModel use
- `modules/beesblog/controllers/admin/` — CRUD admin controllers and tabs

## 1. Front controller

File: `modules/mymodule/controllers/front/demo.php`
Class: `<ModuleName><ControllerName>ModuleFrontController`

```php
<?php

if (!defined('_TB_VERSION_')) {
    exit;
}

class MymoduleDemoModuleFrontController extends ModuleFrontController
{
    /** @var bool */
    public $ssl = true;                 // force HTTPS for this page

    /** @var bool */
    public $display_column_left = false;

    /** @var bool */
    public $display_column_right = false;

    public function initContent()
    {
        parent::initContent();

        $id = (int) Tools::getValue('id');
        $this->context->smarty->assign([
            'mymodule_id'   => $id,
            'mymodule_text' => Configuration::get('MYMODULE_TEXT'),
        ]);

        $this->setTemplate('demo.tpl');
    }
}
```

- Class naming is case-insensitive but convention is
  `<Module><Controller>ModuleFrontController` (e.g.
  `BankwirePaymentModuleFrontController` for module `bankwire`, controller
  `payment`).
- `$this->module` is populated automatically by `ModuleFrontController`.
- Templates resolve from `views/templates/front/` (and theme overrides).
- `initContent()` renders the page; `postProcess()` handles POST before render;
  `setMedia()` registers CSS/JS (`$this->addCSS()`, `$this->addJS()`).
- Add the controller name to the main class: `public $controllers = ['demo'];`
  (or `$this->controllers = ['demo']` in the constructor). TB uses this list to
  create/remove `meta` entries on install/uninstall.

URLs:

```php
$url = $this->context->link->getModuleLink(
    'mymodule',
    'demo',
    ['id' => 42],
    true // SSL
);
Tools::redirect($url);
```

In Smarty:

```smarty
<a href="{$link->getModuleLink('mymodule', 'demo', ['id' => 42], true)|escape:'htmlall':'UTF-8'}">
  {l s='Open demo' mod='mymodule'}
</a>
```

### Friendly routes (`moduleRoutes`)

Implement `hookModuleRoutes()` in the main module class, register the hook on
install, and return route definitions. `Dispatcher` merges them by route ID.

```php
public function hookModuleRoutes()
{
    return [
        'mymodule_demo' => [
            'controller' => 'demo',
            'rule'       => 'mymodule/{slug}',
            'keywords'   => [
                'slug' => ['regexp' => '[_a-zA-Z0-9-\pL]*', 'param' => 'slug'],
            ],
            'params'     => [
                'fc'     => 'module',
                'module' => $this->name,
            ],
        ],
    ];
}
```

Use the route ID with `getModuleLink()` when you want the friendly URL:
`$link->getModuleLink('mymodule', 'mymodule_demo', ['slug' => 'x'])`.
`modules/beesblog/beesblog.php` has an extensive, real example including
pagination and fallback `module/...` rules.

## 2. Admin controller + tab

File: `modules/mymodule/controllers/admin/AdminMyModuleController.php`
Class: `AdminMyModuleController extends ModuleAdminController`

```php
<?php

if (!defined('_TB_VERSION_')) {
    exit;
}

class AdminMyModuleController extends ModuleAdminController
{
    public function __construct()
    {
        $this->table = 'mymodule';                 // DB table WITHOUT prefix
        $this->className = 'MyModuleItem';         // ObjectModel class
        $this->identifier = 'id_mymodule';         // optional; defaults to id_<table>
        $this->bootstrap = true;
        $this->lang = true;                        // multilang fields
        $this->multishop_context = Shop::CONTEXT_SHOP;

        parent::__construct();

        $this->fields_list = [
            'id_mymodule' => ['title' => $this->l('ID'), 'type' => 'text'],
            'name'        => ['title' => $this->l('Name'), 'type' => 'text', 'lang' => true],
            'active'      => ['title' => $this->l('Active'), 'type' => 'bool', 'active' => 'status'],
        ];
    }

    public function renderList()
    {
        $this->addRowAction('edit');
        $this->addRowAction('delete');

        return parent::renderList();
    }

    public function renderForm()
    {
        $this->fields_form = [
            'legend' => ['title' => $this->l('Item')],
            'input'  => [
                [
                    'type'     => 'text',
                    'label'    => $this->l('Name'),
                    'name'     => 'name',
                    'lang'     => true,
                    'required' => true,
                ],
                [
                    'type'    => 'switch',
                    'label'   => $this->l('Active'),
                    'name'    => 'active',
                    'is_bool' => true,
                    'values'  => [
                        ['id' => 'on', 'value' => 1, 'label' => $this->l('Yes')],
                        ['id' => 'off', 'value' => 0, 'label' => $this->l('No')],
                    ],
                ],
            ],
            'submit' => ['title' => $this->l('Save')],
        ];

        return parent::renderForm();
    }
}
```

Key points:

- `ModuleAdminController` requires a matching `Tab` row whose `class_name` is
  the controller class name **without** the `Controller` suffix
  (`AdminMyModule`).
- `$this->table` excludes the `_DB_PREFIX_`. `$this->className` is the
  `ObjectModel` class (namespaced class names are allowed as strings).
- `$this->identifier` defaults to `id_<table>`; set it explicitly when the
  primary key differs.
- `$this->fields_list` drives `renderList()`; `$this->fields_form` drives
  `renderForm()`. `$this->lang = true` enables per-language fields.
- `multishop_context = Shop::CONTEXT_SHOP` limits the page to a single shop;
  call `Shop::addTableAssociation($this->table, ['type' => 'shop'])` before
  `parent::__construct()` for multishop ObjectModels.
- Admin templates go in `views/templates/admin/`.

### Register the tab on install

```php
protected function installTab()
{
    $tab = new Tab((int) Tab::getIdFromClassName('AdminMyModule'));
    $tab->class_name = 'AdminMyModule';
    $tab->module = $this->name;
    $tab->id_parent = (int) Tab::getIdFromClassName('AdminCatalog'); // or 0 for top level
    $tab->active = 1;

    foreach (Language::getLanguages() as $lang) {
        $tab->name[(int) $lang['id_lang']] = $this->l('My module');
    }

    return $tab->save();
}
```

Call it from `install()` after `parent::install()`, and delete the tab in
`uninstall()`:

```php
$tabId = (int) Tab::getIdFromClassName('AdminMyModule');
if ($tabId) {
    (new Tab($tabId))->delete();
}
```

`modules/beesblog/beesblog.php` creates a parent tab plus child tabs; use it as
the reference for multi-page admin sections.

## 3. Choosing the right controller

| Need | Use |
|---|---|
| Public page / form / provider callback | `ModuleFrontController` in `controllers/front/` |
| Configuration page from Module Manager | `getContent()` in the main class |
| CRUD over an `ObjectModel` | `ModuleAdminController` + `Tab` |
| One-off admin screen | `ModuleAdminController` with a `Tab`; or `getContent()` if it belongs under Configure |
| Payment selection/validation | `ModuleFrontController` + `PaymentModule` (see payment reference) |

## 4. Security and correctness

- Front controllers handling state changes must validate input, verify tokens
  where applicable, and use `$ssl = true` for checkout/payment/customer data.
- Provider callbacks (IPN/webhooks) cannot use the shop's CSRF token; verify the
  provider signature and amount/currency/order before calling `validateOrder()`.
- Admin controllers: do not build URLs manually; `AdminController` provides
  `$this->token` and `static::$currentIndex`. Use framework helpers for lists,
  filters, and bulk actions.
- Always `(int)` cast identifiers before loading objects or building SQL.
- Check `Validate::isLoadedObject($object)` before using it; redirect or add an
  error when the object is missing.
