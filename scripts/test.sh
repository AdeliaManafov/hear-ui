#! /usr/bin/env bash
"""
Unified test runner for the project.

This script replaces the older `test.sh` / `test-local.sh` pair and supports
both CI-style runs and local developer runs using the `--local` flag.

Usage:
	./scripts/test.sh           # CI-style run: starts services, runs tests, tears down
	./scripts/test.sh --local   # Local run: starts services and opens tests in dev-friendly mode

The script automatically picks `docker compose` (recommended) or falls back
to `docker-compose` if the former is not available on the host.
"""

set -euo pipefail

show_usage() {
	cat <<EOF
Usage: $0 [--local] [--help]
	--local    Run the local-focused test flow (keeps containers running for inspection)
	--help     Show this help
EOF
}

# Parse args
LOCAL=false
while [[ $# -gt 0 ]]; do
	case "$1" in
		--local) LOCAL=true; shift ;;
		-h|--help) show_usage; exit 0 ;;
		*) echo "Unknown argument: $1"; show_usage; exit 2 ;;
	esac
done

# Choose compose command: prefer `docker compose`, fallback to `docker-compose`.
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
	DOCKER_COMPOSE=(docker compose)
else
	DOCKER_COMPOSE=(docker-compose)
fi

echo "Using compose command: ${DOCKER_COMPOSE[*]}"

# Stop and remove previous stacks to avoid conflicts
"${DOCKER_COMPOSE[@]}" down -v --remove-orphans || true

echo "Building images..."
"${DOCKER_COMPOSE[@]}" build

echo "Starting containers..."
"${DOCKER_COMPOSE[@]}" up -d

# Run backend test starter inside the backend container. Pass-through args.
echo "Executing backend test starter..."
"${DOCKER_COMPOSE[@]}" exec -T backend bash scripts/tests-start.sh

if [ "$LOCAL" = false ]; then
	echo "CI-style run finished — tearing down containers"
	"${DOCKER_COMPOSE[@]}" down -v --remove-orphans
else
	echo "Local run finished — containers left running for inspection"
	echo "Use '${DOCKER_COMPOSE[*]} ps' and '${DOCKER_COMPOSE[*]} logs -f' to inspect"
fi
