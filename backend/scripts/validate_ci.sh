#!/usr/bin/env bash
# CI Validation Helper Script
# Provides quick commands to check CI readiness and trigger validation.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# The script lives in `backend/scripts`, so REPO_ROOT already points to the
# `backend` directory. Use that directly as BACKEND_DIR to avoid duplicating
# the `backend` segment in generated paths.
BACKEND_DIR="$REPO_ROOT"

echo "=== CI Validation Helper ==="
echo "Repo root: $REPO_ROOT"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."
if ! command_exists docker; then
    echo "❌ Docker not found. Install Docker to run integration tests."
else
    echo "✅ Docker found: $(docker --version)"
fi

if ! command_exists gh; then
    echo "⚠️  GitHub CLI (gh) not found. Install it for easy CI monitoring."
    echo "   Install: brew install gh (macOS) or https://cli.github.com/"
else
    echo "✅ GitHub CLI found: $(gh --version | head -n1)"
fi

if ! command_exists act; then
    echo "⚠️  act not found. Install it to simulate CI locally."
    echo "   Install: brew install act (macOS) or https://github.com/nektos/act"
else
    echo "✅ act found: $(act --version)"
fi

echo ""
echo "=== Available Commands ==="
echo ""
echo "1) Run local tests (unit only):"
echo "   cd $BACKEND_DIR && ./scripts/run_unit_tests.sh"
echo ""
echo "2) Run local tests (full suite with coverage):"
echo "   cd $BACKEND_DIR && ./scripts/run_all_tests.sh"
echo ""
echo "3) Simulate CI locally with act:"
echo "   cd $REPO_ROOT && act push"
echo ""
echo "4) Check CI status on GitHub:"
echo "   gh run list --repo AdeliaManafov/hear-ui"
echo ""
echo "5) View latest CI run logs:"
echo "   gh run view --repo AdeliaManafov/hear-ui --log"
echo ""
echo "6) Trigger CI by pushing current branch:"
echo "   git push origin \$(git branch --show-current)"
echo ""
echo "7) Create test branch and push to trigger CI:"
echo "   git checkout -b test-ci-\$(date +%Y%m%d-%H%M%S)"
echo "   git add ."
echo "   git commit -m 'test: validate CI setup'"
echo "   git push origin \$(git branch --show-current)"
echo ""
echo "=== Quick Diagnostics ==="
echo ""

# Python version check
if command_exists python3; then
    echo "Python version: $(python3 --version)"
    echo "Python executable: $(which python3)"
fi

# Check if in venv
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "✅ Virtual environment active: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment active. Activate one before running tests."
fi

# Check backend dependencies
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    echo ""
    echo "Backend dependencies (first 5 lines):"
    head -n 5 "$BACKEND_DIR/requirements.txt"
    echo "..."
    
    # Check if scikit-learn is pinned
    if grep -q "scikit-learn==1.6.1" "$BACKEND_DIR/requirements.txt"; then
        echo "✅ scikit-learn pinned to 1.6.1 (matches model)"
    else
        echo "⚠️  scikit-learn not pinned to 1.6.1 — check version mismatch warnings"
    fi
fi

echo ""
echo "=== Next Steps ==="
echo "1. Run local tests to verify everything works"
echo "2. Push to GitHub to trigger CI"
echo "3. Monitor CI at: https://github.com/AdeliaManafov/hear-ui/actions"
echo "4. Check $BACKEND_DIR/CI_VALIDATION.md for detailed guide"
echo ""
