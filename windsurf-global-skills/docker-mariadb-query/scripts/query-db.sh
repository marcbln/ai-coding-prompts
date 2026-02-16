#!/usr/bin/env bash
# query-db.sh - Execute a SQL query against a MariaDB Docker container
# 2026-02-16 created
#
# This script accepts:
#   $1 = container name (e.g. focus-mariadb)
#   $2 = SQL query
#
# The script executes the SQL inside the specified container
# using the mariadb client.

set -euo pipefail

CONTAINER="$1"
SQL="$2"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
    echo "Error: container '${CONTAINER}' is not running" >&2
    exit 1
fi

docker exec -i "$CONTAINER" mariadb -e "$SQL"
