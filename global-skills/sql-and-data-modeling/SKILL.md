---
name: sql-and-data-modeling
description: Relational database design, safe zero-downtime migrations, query optimization, indexing strategies, and concurrency control for PostgreSQL and MySQL.
---

# SQL & Relational Data Modeling Skill

Guidelines for building robust, performant, and safe relational persistence layers.

---

## 1. Relational Schema Design Rules
- **Explicit Primary Keys**: Use `BIGINT GENERATED ALWAYS AS IDENTITY` (PostgreSQL) or `UUIDv7` (time-ordered sequential UUIDs) to prevent B-Tree fragmentation.
- **Strict Data Types**:
  - Use `TIMESTAMPTZ` (UTC timestamps with time zone) over naive timestamps.
  - Use `NUMERIC(18, 4)` / `DECIMAL` for financial calculations; **never use FLOAT/DOUBLE for money**.
  - Use `VARCHAR(n)` or `TEXT` with `CHECK` constraints over arbitrary unconstrained columns.
- **Foreign Keys**: Always define foreign keys with appropriate `ON DELETE` behavior (`RESTRICT` / `NO ACTION` by default; avoid cascading deletes on core business entities).
- **Soft Deletes**: Use `deleted_at TIMESTAMPTZ NULL`. When using soft deletes, ensure unique indexes include `WHERE deleted_at IS NULL` (partial index).

---

## 2. Zero-Downtime Schema Migrations (Expand & Contract)

Never execute destructive or blocking DDL in a single release.

### 2.1 Renaming a Column / Table
1. **Expand**: Add the new column (`new_name`). Dual-write to both `old_name` and `new_name` in application code.
2. **Backfill**: Backfill historical rows asynchronously in batches.
3. **Switch**: Update application reads to use `new_name`. Stop writing to `old_name`.
4. **Contract**: Drop `old_name` in a subsequent release.

### 2.2 Adding `NOT NULL` Columns Safely
1. Add column as `NULLABLE`.
2. Deploy application code that populates the column for new records.
3. Backfill existing `NULL` rows with default values.
4. Add check constraint `CHECK (column IS NOT NULL) NOT VALID;` (instant, no long lock).
5. Validate constraint: `ALTER TABLE t VALIDATE CONSTRAINT ...;`

---

## 3. Indexing & Query Optimization
- **B-Tree Indexing Order (Left-to-Right Rule)**:
  - In a composite index `(status, created_at)`, queries filtering by `status` or `(status AND created_at)` will use the index. A query filtering only by `created_at` **cannot** use the index effectively.
  - Rule: Put **equality columns first**, followed by **range/sort columns**.
- **Covering Indexes (Index-Only Scans)**:
  - Include frequently selected columns: `CREATE INDEX idx_orders_user ON orders(user_id) INCLUDE (total_amount, status);`
- **Avoid Common Anti-Patterns**:
  - `SELECT *`: Always project only the columns needed by the driven adapter.
  - **Functions on Indexed Columns**: `WHERE DATE(created_at) = '2026-08-31'` prevents index usage. Use range queries: `WHERE created_at >= '2026-08-31 00:00:00' AND created_at < '2026-09-01 00:00:00'`.
  - **N+1 Queries**: Eager-load associations with batch queries (`IN (?, ?, ?)`) or joins rather than issuing a query inside a loop.

---

## 4. Concurrency & Locking

### 4.1 Optimistic Locking (Recommended for Low Contention)
- Add a `version INT NOT NULL DEFAULT 1` column to the aggregate root table.
- Mutation query:
  ```sql
  UPDATE orders 
  SET status = 'PAID', version = version + 1 
  WHERE id = :id AND version = :current_version;
  ```
- If rows affected == 0, throw a `ConcurrencyConflictException` and retry/abort.

### 4.2 Pessimistic Locking (High Contention / Critical Balance Changes)
- Acquire lock explicitly:
  ```sql
  SELECT * FROM bank_accounts WHERE id = :id FOR UPDATE;
  ```
- Keep transaction duration as short as possible to avoid connection starvation and deadlocks.
- Acquire locks on multiple resources in a **deterministic order** (e.g., sorted by ID) to eliminate deadlocks.

---

## 5. Language-Specific Persistence Conventions

* **Go (`database/sql`, `pgx`)**:
  * Always pass `context.Context` with query timeouts (`context.WithTimeout`).
  * Never leave rows unclosed: `defer rows.Close()` and check `rows.Err()`.
  * Set connection pool limits: `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`.
* **PHP (Doctrine DBAL / ORM)**:
  * Keep ORM entities inside infrastructure if practicing pure Clean Architecture, or map pure Domain Entities using DBAL.
  * Use `clear()` / `detach()` when processing large batches to prevent memory leaks in the Unit of Work.
* **Python (SQLAlchemy / asyncpg)**:
  * Use explicit async sessions: `async with session.begin(): ...`.
  * Set statement execution timeouts on the engine to avoid hung connections.
