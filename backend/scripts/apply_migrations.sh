#!/usr/bin/env bash
# Helper script to apply Alembic migrations for the backend.
# Usage: from repository root: ./backend/scripts/apply_migrations.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  echo "ERROR: .env file not found in $ROOT_DIR"
  echo "Copy .env.example to .env and fill in DB credentials before running migrations."
  exit 1
fi

# Load environment variables from .env (simple, not for complex shells)
set -a
# shellcheck source=/dev/null
. ./.env
set +a

echo "Applying Alembic migrations using SQLALCHEMY_DATABASE_URI from settings..."

# Run alembic via python -m to ensure the virtualenv interpreter is used if active
python -m alembic upgrade head

echo "Migrations applied."