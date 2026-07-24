---
name: common-doctrine-dbal-4.x-pitfalls
description: >
  Fixes code that breaks on Doctrine DBAL 4.x. Covers ParameterType enum (not int),
  fetchAllAssociative returning strings, removed insert/update/delete methods,
  and Result vs Statement. Use when writing or debugging DBAL queries in any
  PHP project, when encountering ExpandArrayParameters type errors, or when
  porting code from DBAL 2.x/3.x to 4.x.
---

# Doctrine DBAL 4.x Common Pitfalls

DBAL 4.x introduced several breaking changes that commonly trip up AI-generated code
(which often targets 2.x or 3.x). The most frequent issues are:

1. `ParameterType` is a PHP enum, not integer constants.
2. `fetchAllAssociative` returns **all values as strings** — no native type casting.
3. `Connection::insert()`, `update()`, `delete()` are **removed**.
4. `executeQuery()` returns `Doctrine\DBAL\Result`, not `Statement`.
5. Named parameters with explicit types go through `ExpandArrayParameters` which
   rejects integer type values.

## Usage / Correct Patterns

### 1. ParameterType — use the enum, not PDO constants

```php
use Doctrine\DBAL\Connection;
use Doctrine\DBAL\ParameterType;

// CORRECT: enum cases
$this->connection->fetchFirstColumn(
    'SELECT id FROM t WHERE created_at < :margin LIMIT :limit',
    ['margin' => $date, 'limit' => 100],
    ['margin' => ParameterType::STRING, 'limit' => ParameterType::INTEGER]
);
```

### 2. ArrayParameterType — also an enum

```php
use Doctrine\DBAL\ArrayParameterType;

// CORRECT
$this->connection->executeStatement(
    'DELETE FROM t WHERE id IN (:ids)',
    ['ids' => $ids],
    ['ids' => ArrayParameterType::BINARY]
);
```

### 3. fetchAllAssociative / fetchOne return strings — cast explicitly

```php
// All values come back as strings in DBAL 4.x
$rows = $this->connection->fetchAllAssociative('SELECT id, price FROM products');
foreach ($rows as $row) {
    $id    = (int) $row['id'];
    $price = (float) $row['price'];
}

// Same for fetchOne
$count = (int) $this->connection->fetchOne('SELECT COUNT(*) FROM products');
```

### 4. Removed: insert(), update(), delete() — use executeStatement

```php
// REMOVED — will throw a runtime error:
//   $this->connection->insert('products', ['title' => 'foo']);

// CORRECT — write explicit SQL:
$this->connection->executeStatement(
    'INSERT INTO products (id, title, price) VALUES (:id, :title, :price)',
    ['id' => Uuid::randomBytes(), 'title' => 'Foo', 'price' => 9.99]
);
```

### 5. executeQuery() returns Result, not Statement

```php
// CORRECT — method chaining still works:
$result = $this->connection->executeQuery('SELECT * FROM products WHERE id = :id', ['id' => $id]);
$row    = $result->fetchAssociative();

// Iterate:
foreach ($result->iterateAssociative() as $row) { ... }
```

### 6. Named parameters with explicit types — every named param gets visited

When you pass an explicit `$types` array with named parameters, DBAL's
`ExpandArrayParameters` visitor processes **all** named parameters, not just
array/IN parameters. Every type value must be a valid `ParameterType` or
`ArrayParameterType` enum case — never an int.

```php
// This crashes even for non-array params:
$this->connection->fetchFirstColumn(
    'SELECT id FROM t WHERE x < :val',
    ['val' => 42],
    ['val' => \PDO::PARAM_INT]  // TypeError: int given, enum expected
);

// CORRECT:
$this->connection->fetchFirstColumn(
    'SELECT id FROM t WHERE x < :val',
    ['val' => 42],
    ['val' => ParameterType::INTEGER]
);
```

Also note that in many cases you can simply omit the `$types` array entirely —
DBAL handles type inference well for simple string/int values:

```php
// Often sufficient — DBAL infers types automatically:
$this->connection->fetchFirstColumn(
    'SELECT id FROM t WHERE created_at < :margin LIMIT :limit',
    ['margin' => $date, 'limit' => 100]
    // no $types array needed
);
```

## Anti-patterns (DO NOT USE)

```php
// 1. PDO integer constants — TypeError in DBAL 4.x
\PDO::PARAM_STR
\PDO::PARAM_INT
\PDO::PARAM_BOOL

// 2. Removed methods — will throw runtime exceptions
$conn->insert('table', $data);
$conn->update('table', $data, $where);
$conn->delete('table', $where);
$conn->executeUpdate($sql);   // renamed to executeStatement in 3.x, removed in 4.x

// 3. fetch() / fetchAll() on Statement — Statement no longer has these
$stmt = $conn->executeQuery($sql);
$stmt->fetch();               // Fatal error: method does not exist
$stmt->fetchAll();            // Fatal error: method does not exist

// Use Result methods instead:
$result = $conn->executeQuery($sql);
$result->fetchAssociative();
$result->fetchAllAssociative();

// 4. Assuming fetchAllAssociative returns int/float for numeric columns
$row = $conn->fetchAllAssociative('SELECT price FROM products')[0];
$price = $row['price'];       // string "9.99", not float
$total = $price + 5;          // works but fragile; cast explicitly

// 5. Doctrine\DBAL\FetchMode constants — removed entirely
$conn->executeQuery($sql)->fetch(FetchMode::ASSOCIATIVE);  // class not found
```
