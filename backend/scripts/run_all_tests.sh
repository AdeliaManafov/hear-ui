#!/usr/bin/env bash
set -euo pipefail

# Helper script to run the full backend tests with coverage.
# It will:
#  - activate .venv if present
#  - install test deps (pytest, pytest-cov, testcontainers)
#  - check Docker availability
#  - run pytest (full suite, including integration)

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Activate venv if present
if [ -f ".venv/bin/activate" ]; then
  echo "Activating .venv..."
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "No .venv found. Continuing with current python environment." >&2
fi

echo "Updating pip and installing test dependencies..."
python -m pip install --upgrade pip
pip install pytest pytest-cov || true
pip install "testcontainers[postgres]" || true

# Check Docker
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker CLI not found. Testcontainers requires Docker to start Postgres containers." >&2
  echo "If you want to use an existing DB instead, set USE_EXISTING_DB=true and ensure DATABASE_URL is set." >&2
  exit 2
fi

if ! docker info >/dev/null 2>&1; then
  echo "Docker daemon does not appear to be running. Start Docker and retry." >&2
  exit 3
fi

echo "Running pytest (full test suite with coverage)..."
pytest -v --cov=app --cov-report=term-missing --cov-report=html

echo "Coverage HTML generated at backend/htmlcov/index.html"

# On macOS, optionally open the HTML report automatically
if [[ "$(uname)" == "Darwin" ]]; then
  if [ -f backend/htmlcov/index.html ]; then
    open backend/htmlcov/index.html || true
  fi
fi
