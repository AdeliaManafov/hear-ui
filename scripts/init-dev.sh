# Purpose: It automatically creates a .env file from .env.example, but only if no .env file exists.

#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/init-dev.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
EXAMPLE_FILE="$ROOT_DIR/.env.example"
TARGET_FILE="$ROOT_DIR/.env"

if [ -f "$TARGET_FILE" ]; then
	echo "[init-dev] $TARGET_FILE already exists — not overwriting."
	exit 0
fi

if [ ! -f "$EXAMPLE_FILE" ]; then
	echo "[init-dev] No .env.example found at $EXAMPLE_FILE. Create one first or copy manually."
	exit 1
fi

cp "$EXAMPLE_FILE" "$TARGET_FILE"
echo "[init-dev] Created $TARGET_FILE from $EXAMPLE_FILE"
echo "[init-dev] Edit $TARGET_FILE to set local secrets and configuration."
