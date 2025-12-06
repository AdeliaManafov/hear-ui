#!/usr/bin/env bash
set -euo pipefail

# Quick unit tests script - runs only unit tests (no DB, no server required)
# This is the fastest way to test locally without external dependencies

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Activate venv if present
if [ -f ".venv/bin/activate" ]; then
  echo "Activating .venv..."
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "Running unit tests only (skipping integration and e2e)..."
pytest -m "not integration and not e2e" -v --cov=app --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Unit tests completed!"
echo "📊 Coverage HTML report: backend/htmlcov/index.html"

# On macOS, optionally open the HTML report
if [[ "$(uname)" == "Darwin" ]]; then
  if [ -f htmlcov/index.html ]; then
    echo "Opening coverage report..."
    open htmlcov/index.html || true
  fi
fi
