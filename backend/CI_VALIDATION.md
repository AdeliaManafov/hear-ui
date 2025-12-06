# CI Validation Guide

This document explains how to validate that the GitHub Actions CI workflows run successfully and how to diagnose issues.

## Overview

The backend has two main CI workflows:
- `.github/workflows/test-backend.yml` — comprehensive backend tests with coverage
- `.github/workflows/backend-tests.yml` — backend tests (alternative/redundant workflow)

Both workflows:
- Install dependencies including `testcontainers[postgres]`
- Run pytest with coverage (`--cov --cov-fail-under=80`)
- Print Python & Docker diagnostics for troubleshooting

## How to Trigger CI on GitHub

### Method 1: Push to a branch
```bash
# Make sure you're on a branch
git checkout -b test-ci-validation

# Commit your changes
git add .
git commit -m "test: validate CI with pinned sklearn and new tests"

# Push to GitHub
git push origin test-ci-validation
```

Then visit: `https://github.com/AdeliaManafov/hear-ui/actions`

### Method 2: Create a Pull Request
After pushing a branch, create a PR on GitHub. CI will run automatically.

### Method 3: Manual workflow dispatch (if enabled)
Some workflows support manual triggering via the GitHub Actions UI:
1. Go to `https://github.com/AdeliaManafov/hear-ui/actions`
2. Select the workflow (e.g., "Backend Tests")
3. Click "Run workflow" button (if available)

## What to Check in CI Logs

When a CI run completes, inspect the logs for:

### 1. Dependency Installation
Look for successful installation of key packages:
```
Successfully installed scikit-learn-1.6.1 shap-... testcontainers-...
```

### 2. Python & Docker Diagnostics
The workflows now print diagnostic info. Look for:
```
Python version: 3.10.x
Python executable: /path/to/python
Docker version: Docker version X.Y.Z
```

### 3. Test Execution
Check pytest output:
```
===== test session starts =====
...
===== X passed, Y warnings in Z.ZZs =====
```

Expected: All tests pass, coverage ≥80%.

### 4. Testcontainers Behavior
If integration tests run, logs should show:
```
INFO:     testcontainers starting postgres container...
```

If testcontainers fail to start (GitHub runner limitations), the test may skip or fail with a clear error from `conftest.py`.

### 5. Coverage Report
Check coverage meets threshold:
```
TOTAL ... 80%
```

If coverage < 80%, the CI step will fail (due to `--cov-fail-under=80`).

## Common CI Issues & Fixes

### Issue 1: Testcontainers cannot start Docker containers
**Symptom:** Integration tests fail with Docker socket errors.

**Fix:** Modify `app/tests/conftest.py` to set `USE_EXISTING_DB=true` in CI environment, or update workflow to use GitHub's service containers for Postgres.

Example workflow snippet:
```yaml
services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: testdb
    ports:
      - 5432:5432
```

### Issue 2: Coverage below threshold
**Symptom:** CI fails with "Coverage is below 80%".

**Fix:** Add more tests or adjust threshold in workflow (`--cov-fail-under=XX`).

### Issue 3: Sklearn version mismatch (now fixed)
**Symptom:** Warnings about sklearn version incompatibility.

**Fix:** Already applied — `requirements.txt` now pins `scikit-learn==1.6.1`.

## Running CI Locally with `act`

You can simulate GitHub Actions locally using [act](https://github.com/nektos/act):

### Install act
```bash
# macOS
brew install act

# Linux/WSL
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
```

### Run workflows locally
```bash
# Run all workflows
cd /path/to/hear-ui
act

# Run a specific workflow
act -W .github/workflows/test-backend.yml

# Run with a specific event (e.g., push)
act push

# Dry run (show what would execute)
act -n
```

**Note:** `act` requires Docker to be running. Some features (like GitHub service containers) may behave differently than on GitHub's runners.

## Quick Validation Checklist

Before considering CI stable:

- [ ] Push a branch and verify workflow runs on GitHub Actions
- [ ] Check all test steps pass (unit, integration if applicable)
- [ ] Verify coverage ≥ 80%
- [ ] Inspect diagnostic output (Python version, Docker info)
- [ ] Confirm no sklearn version warnings in logs
- [ ] Run `backend/scripts/run_all_tests.sh` locally and compare results
- [ ] (Optional) Run with `act` to simulate CI locally

## Next Steps

- If CI passes consistently, update README to reference this guide.
- Consider adding badges to README showing CI status.
- If testcontainers prove unreliable in CI, switch to GitHub service containers.
- Add E2E workflow that actually starts the server and calls endpoints.

## Useful Commands

```bash
# Trigger local test run matching CI
cd backend
pip install -r requirements.txt
pytest --cov --cov-report=html --cov-fail-under=80

# Check if Docker is available (CI diagnostic)
docker --version
docker info

# View GitHub Actions runs
gh run list --repo AdeliaManafov/hear-ui
gh run view <run-id> --log
```
