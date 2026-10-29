# ObjectModel, Database, Settings, and Upgrades

Source anchors:

- `classes/ObjectModel.php` — `$definition`, `createDatabase()`, CRUD
- `classes/db/Db.php`, `classes/db/DbQuery.php` — query API
- `classes/Configuration.php` — key/value settings
- `modules/beesblog/classes/BeesBlogPost.php` — multilang/multishop model
- `modules/beesblog/classes/BeesBlogPost.php::createDatabase()` — extra table
- `modules/blockbestsellers/upgrade/upgrade-2.1.0.php` — upgrade script
- `modules/beesblog/upgrade/upgrade-1.8.0.php` — settings backfill upgrade

## 1. ObjectModel definition (TB 1.7)

```php
<?php

if (!defined('_TB_VERSION_')) {
    exit;
}

class MyModuleItem extends ObjectModel
{
    const PRIMARY = 'id_mymodule';
    const TABLE   = 'mymodule';

    public static $definition = [
        'table'     => self::TABLE,
        'primary'   => self::PRIMARY,
        'multilang' => true,     // creates <table>_lang
        'multishop' => true,     // creates <table>_shop (TB extension)
        'fields'    => [
            'active'      => ['type' => self::TYPE_BOOL,   'validate' => 'isBool',        'required' => true, 'db_type' => 'TINYINT(1) UNSIGNED'],
            'position'    => ['type' => self::TYPE_INT,    'validate' => 'isUnsignedInt', 'required' => true, 'db_type' => 'INT(11) UNSIGNED', 'default' => '0'],
            'date_add'    => ['type' => self::TYPE_DATE,   'validate' => 'isDate',        'required' => true, 'db_type' => 'DATETIME'],
            'date_upd'    => ['type' => self::TYPE_DATE,   'validate' => 'isDate',        'required' => true, 'db_type' => 'DATETIME'],
            'name'        => ['type' => self::TYPE_STRING, 'validate' => 'isString',      'required' => true, 'lang' => true, 'db_type' => 'VARCHAR(255)'],
            'description' => ['type' => self::TYPE_HTML,   'validate' => 'isCleanHtml',   'required' => false, 'lang' => true, 'db_type' => 'TEXT'],
        ],
    ];

    /** @var bool */
    public $active = true;

    /** @var int */
    public $position = 0;

    /** @var string */
    public $date_add;

    /** @var string */
    public $date_upd;

    /** @var string|string[] */
    public $name;

    /** @var string|string[] */
    public $description;
}
```

Rules:

- Declare every field as a typed/untyped public property. PHP 8.2 deprecates
  dynamic properties, and `ObjectModel::hydrate()` would otherwise create them.
- `table` and `primary` are **without** the `_DB_PREFIX_`.
- `'lang' => true` on a field makes it live in `<table>_lang`; the model
  hydrates an array keyed by language ID.
- `'multishop' => true` (TB) adds `<table>_shop` shop associations.
- `db_type` lets you keep control of the column type (TB uses it for schema
  creation). Without it, the type is inferred from `TYPE_*` and `size`.
- Field `validate` values are `Validate` method names (`isBool`,
  `isUnsignedInt`, `isString`, `isCleanHtml`, `isLinkRewrite`, ...).

Create/drop tables:

```php
MyModuleItem::createDatabase(MyModuleItem::class);
MyModuleItem::dropDatabase(MyModuleItem::class);
```

`ObjectModel::createDatabase()` creates the main table (and, for TB,
language/shop tables); it returns `bool` and throws `PrestaShopException`.
For join tables or custom schemas, extend the model's static methods as
`BeesBlogPost` does:

```php
public static function createDatabase($className = null)
{
    return parent::createDatabase($className)
        && static::createRelatedProductsTable();
}
```

## 2. Raw queries

Use `DbQuery` for SELECT/UPDATE/DELETE and `Db::getInstance()` for execution.

```php
$db = Db::getInstance();

$rows = $db->executeS(
    (new DbQuery())
        ->select('i.`id_mymodule`, i.`active`, il.`name`')
        ->from('mymodule', 'i')
        ->leftJoin('mymodule_lang', 'il', 'il.`id_mymodule` = i.`id_mymodule` AND il.`id_lang` = '.(int) $idLang)
        ->where('i.`active` = 1')
        ->orderBy('i.`position` ASC')
);

$row = $db->getRow(
    (new DbQuery())
        ->select('*')
        ->from('mymodule')
        ->where('`id_mymodule` = '.(int) $id)
);

$value = $db->getValue(
    (new DbQuery())
        ->select('`name`')
        ->from('mymodule')
        ->where('`id_mymodule` = '.(int) $id)
);
```

Insert/update/delete helpers:

```php
$db->insert('mymodule', [
    'active'   => 1,
    'position' => 0,
    'date_add' => date('Y-m-d H:i:s'),
    'date_upd' => date('Y-m-d H:i:s'),
]);

$db->update('mymodule', ['active' => 1], '`id_mymodule` = '.(int) $id);
$db->delete('mymodule', '`id_mymodule` = '.(int) $id);
$db->execute('CREATE TABLE IF NOT EXISTS `'._DB_PREFIX_.'mymodule_extra` (...) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci');
```

- `insert()`, `update()`, `delete()` add the table prefix automatically. `execute()`
  and `executeS()` do **not**; write `_DB_PREFIX_` yourself.
- Cast integers and floats. For strings, use `pSQL($value)` (or `DbQuery` value
  escaping where available). Never concatenate raw request data.
- `Db::readOnly()` exists in TB and routes reads to a replica when configured;
  use `Db::getInstance()` when maximum 1.5/1.6/1.7 compatibility matters.
- Use `Db::getInstance()->Insert_ID()` if you need the inserted ID; for
  `ObjectModel`, use `$model->add()` and read `$model->id`.

## 3. Configuration values

```php
Configuration::updateValue('MYMODULE_ENABLED', (int) Tools::getValue('MYMODULE_ENABLED'));
Configuration::updateValue('MYMODULE_TEXT', (string) Tools::getValue('MYMODULE_TEXT'), true); // true = HTML
Configuration::updateGlobalValue('MYMODULE_GLOBAL', $value); // all shops

$enabled = (int) Configuration::get('MYMODULE_ENABLED');
$text    = Configuration::get('MYMODULE_TEXT', (int) $idLang); // multilang value
Configuration::deleteByName('MYMODULE_ENABLED');
```

- `updateValue()` is shop-scoped; `updateGlobalValue()` applies globally.
- Pass `true` as the third argument only when the value is HTML (it changes
  storage/escaping expectations).
- For multilang settings, pass `[$idLang => $value, ...]` to `updateValue()` and
  read with the language ID.
- Delete every setting you create in `uninstall()`.
- Never use `Configuration` for large data or per-entity rows; use an
  `ObjectModel`.

## 4. Install and uninstall schema

```php
public function install()
{
    if (!parent::install()) {
        return false;
    }

    if (!MyModuleItem::createDatabase(MyModuleItem::class)) {
        return false;
    }

    Configuration::updateValue('MYMODULE_ENABLED', 1);

    return $this->registerHook('displayHome')
        && $this->installTab();
}

public function uninstall()
{
    $tabId = (int) Tab::getIdFromClassName('AdminMyModule');
    if ($tabId) {
        (new Tab($tabId))->delete();
    }

    return MyModuleItem::dropDatabase(MyModuleItem::class)
        && Configuration::deleteByName('MYMODULE_ENABLED')
        && parent::uninstall();
}
```

Dropping tables is destructive. For modules that offer "reset" without data
loss, follow the `BeesBlog::reset()` pattern: `uninstall(false)` then
`install(false)`, with boolean parameters that skip table creation/drop and
fixtures.

## 5. Upgrade scripts

Whenever you change the schema or need a data/settings backfill:

1. Bump `$this->version` in the main module class.
2. Add `upgrade/upgrade-<new-version>.php`.
3. Return `true` on success; TB disables the module on `false`.

```php
<?php

if (!defined('_TB_VERSION_')) {
    exit;
}

/**
 * @param Mymodule $module
 *
 * @return bool
 */
function upgrade_module_1_0_1($module)
{
    $db = Db::getInstance();

    if (!$db->execute(
        'ALTER TABLE `'._DB_PREFIX_.'mymodule`
         ADD COLUMN `active` TINYINT(1) UNSIGNED NOT NULL DEFAULT 1'
    )) {
        return false;
    }

    Configuration::updateValue('MYMODULE_ENABLED', 1);

    return true;
}
```

Naming and mechanics:

- File version uses dots: `upgrade-1.0.1.php`.
- Accepted function names: `upgrade_module_1_0_1($module)` (native convention)
  or `upgradeModule101($module)`. Prefer the first.
- TB runs files with `registered_version < file_version <= module_version`, in
  ascending version order (`Module::loadUpgradeVersionList()`).
- Do not edit an upgrade file that has already shipped; add the next one.
- Make upgrades idempotent where practical (`IF NOT EXISTS`, check
  `Configuration::get()` before overwriting user values).
- Keep the main class version and the last upgrade file aligned; a version bump
  without a file is valid only for code-only releases.

## 6. Multishop and multilang

- Multilang fields: declare `'lang' => true` and keep one property per field
  (array when hydrated across languages). In admin, set `$this->lang = true`
  and `'lang' => true` on form/list fields.
- Multishop: declare `'multishop' => true`; in admin call
  `Shop::addTableAssociation($this->table, ['type' => 'shop'])` before
  `parent::__construct()` and set `$this->multishop_context`.
- Save/validate through `ObjectModel::add()`/`update()` so language, shop, and
  validation handling stays consistent. Avoid hand-written INSERTs for
  multilang/multishop models.
- When querying, join `_lang` with the current `id_lang` and `_shop` with the
  current shop context, or use `Shop::addSqlAssociation()`.
