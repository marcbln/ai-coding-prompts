#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: archive-plan.sh <plan-filename>" >&2
    echo "  Marks the plan as completed and moves it from active/ to archive/." >&2
    exit 1
fi

PLAN_FILE="$1"

GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
BACKLOG_DIR="${GIT_ROOT}/_ai/backlog"
ACTIVE_DIR="${BACKLOG_DIR}/active"
ARCHIVE_DIR="${BACKLOG_DIR}/archive"

ACTIVE_PATH="${ACTIVE_DIR}/${PLAN_FILE}"
ARCHIVE_PATH="${ARCHIVE_DIR}/${PLAN_FILE}"

if [ ! -f "$ACTIVE_PATH" ]; then
    echo "Error: Plan not found in active folder: ${ACTIVE_PATH}" >&2
    exit 1
fi

if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
fi

TIMESTAMP="$(date '+%Y-%m-%d %H:%M')"

sed -i "s/^status: .*/status: completed/" "$ACTIVE_PATH"

if grep -q "^completedAt:" "$ACTIVE_PATH"; then
    sed -i "s/^completedAt:.*/completedAt: ${TIMESTAMP}/" "$ACTIVE_PATH"
else
    sed -i "/^status: completed/a completedAt: ${TIMESTAMP}" "$ACTIVE_PATH"
fi

mv "$ACTIVE_PATH" "$ARCHIVE_PATH"

echo "Plan archived: ${PLAN_FILE}"
echo "  status: completed"
echo "  completedAt: ${TIMESTAMP}"
echo "  moved to: ${ARCHIVE_PATH}"
