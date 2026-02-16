---
name: docker-mariadb-query
description: |
  Executes SQL SELECT queries against MariaDB databases running inside local Docker containers.
  Typically used with containers following the naming pattern {shortName}-mariadb.
  Use this skill when a user asks questions requiring database queries.
---

# Docker MariaDB Query Skill

This skill allows the agent to execute SQL queries against MariaDB instances
running inside local Docker containers.

## Container Naming Convention

Most databases follow this pattern:

{shortName}-mariadb

Examples:

- focus-mariadb
- shop-mariadb
- crm-mariadb

When a user references a project name, assume:

project → {shortName}-mariadb

Example:

"focus database" → container `focus-mariadb`

If the container name is explicitly provided by the user, use that directly.

If ambiguity exists, ask the user for clarification.

---

## Agent Responsibilities

When using this skill:

1. Identify the correct container name
2. Convert the user's request into a SQL SELECT query
3. Execute the query via helper script
4. Return the results

---

## Invocation

Call:

scripts/query-db.sh <containerName> "<SQL query>"

Example:

scripts/query-db.sh focus-mariadb "SELECT * FROM users LIMIT 10;"

---

## Query Rules

- Prefer SELECT queries
- Never modify data unless explicitly requested
- Use LIMIT for large datasets
- If schema unknown, inspect first

Schema helpers:

SHOW TABLES;
DESCRIBE table_name;

---

## Errors

- If container not running → notify user
- If query fails → return SQL error
- If table unknown → inspect schema
