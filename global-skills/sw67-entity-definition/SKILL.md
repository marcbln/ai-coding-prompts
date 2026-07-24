---
name: sw67-entity-definition
description: Patterns and gotchas for creating entity definitions in Shopware 6.7 plugins. Use when creating new entities, migrating entities to SW 6.7, or debugging "Unknown column 'updated_at'" errors in DAL queries.
---

# Shopware 6.7 Entity Definition Patterns

## Context: Why This Skill Exists

Shopware 6.7 (via Symfony 6/7) introduces breaking changes to the Data Abstraction Layer (DAL):

1. **Mandatory `updated_at` column**: The base `Entity` class now has `$updatedAt` property. The ORM auto-selects `updated_at` in ALL queries. If your table lacks this column, you get `SQLSTATE[42S22]: Column not found: 1054 Unknown column 'updated_at'`.

2. **Use dedicated field types**: Replace plain `DateTimeField` with `CreatedAtField` and `UpdatedAtField` for auto-managed timestamps. These fields handle `DEFAULT CURRENT_TIMESTAMP` and `ON UPDATE CURRENT_TIMESTAMP` automatically.

3. **Migration timing matters**: The column must exist BEFORE the entity is loaded. Run migrations early in deployment.

## Usage / Correct Patterns

### 1. Entity Definition with Correct Field Types

```php
<?php declare(strict_types=1);

namespace YourPlugin\Entity\YourEntity;

use Shopware\Core\Framework\DataAbstractionLayer\EntityDefinition;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\PrimaryKey;
use Shopware\Core\Framework\DataAbstractionLayer\Field\Flag\Required;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IdField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\StringField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\IntField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\CreatedAtField;
use Shopware\Core\Framework\DataAbstractionLayer\Field\UpdatedAtField;
use Shopware\Core\Framework\DataAbstractionLayer\FieldCollection;

class YourEntityDefinition extends EntityDefinition
{
    public const ENTITY_NAME = 'your_plugin_entity';

    public function getEntityName(): string
    {
        return self::ENTITY_NAME;
    }

    public function getEntityClass(): string
    {
        return YourEntity::class;
    }

    protected function defineFields(): FieldCollection
    {
        return new FieldCollection([
            (new IdField('id', 'id'))->addFlags(new PrimaryKey(), new Required()),
            (new StringField('name', 'name'))->addFlags(new Required()),
            (new IntField('count', 'count'))->addFlags(new Required()),
            new CreatedAtField(),  // handles created_at automatically
            new UpdatedAtField(),  // handles updated_at automatically
        ]);
    }
}
```

### 2. Migration Adding Both Timestamp Columns

```php
<?php declare(strict_types=1);

namespace YourPlugin\Migration;

use Doctrine\DBAL\Connection;
use Shopware\Core\Framework\Migration\MigrationStep;

class MigrationAddTimestamps extends MigrationStep
{
    public function getCreationTimestamp(): int
    {
        return 1753380000; // current timestamp
    }

    public function update(Connection $connection): void
    {
        // For existing tables: add columns with defaults
        $connection->executeStatement('
            ALTER TABLE `your_plugin_entity`
            ADD COLUMN `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
            ADD COLUMN `updated_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3)
        ');
    }

    public function updateDestructive(Connection $connection): void
    {
        $connection->executeStatement('ALTER TABLE `your_plugin_entity` DROP COLUMN `updated_at`, DROP COLUMN `created_at`');
    }
}
```

### 3. For New Tables: Include in CREATE TABLE

```php
$connection->executeStatement('
    CREATE TABLE `your_plugin_entity` (
        `id` BINARY(16) NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        `count` INT NOT NULL,
        `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
        `updated_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
        PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
');
```

## Anti-patterns (DO NOT USE)

```php
// ❌ WRONG: Plain DateTimeField - ORM still expects updated_at column
(new DateTimeField('created_at', 'createdAt'))->addFlags(new Required()),
// missing UpdatedAtField entirely

// ❌ WRONG: Forgetting UpdatedAtField - causes "Unknown column 'updated_at'" error
new CreatedAtField(),
// UpdatedAtField missing!

// ❌ WRONG: Migration without ON UPDATE for updated_at
$connection->executeStatement('
    ALTER TABLE `your_table` ADD COLUMN `updated_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
    // Missing: ON UPDATE CURRENT_TIMESTAMP(3)
');

// ❌ WRONG: Making columns nullable (breaks DAL expectations)
new UpdatedAtField(), // NOT nullable - DAL expects value on every write
```

## Quick Checklist for New Entities

- [ ] Extend `EntityDefinition`
- [ ] Use `CreatedAtField` (not `DateTimeField` for created_at)
- [ ] Use `UpdatedAtField` (mandatory in SW 6.7+)
- [ ] Migration adds both columns with `DEFAULT CURRENT_TIMESTAMP(3)` and `ON UPDATE CURRENT_TIMESTAMP(3)`
- [ ] Run migration before deploying code that uses the entity
- [ ] Verify with `DESCRIBE your_table` that both columns exist with correct defaults