# Backend dependencies and locking

This file documents how to produce a reproducible, pinned Python dependency file for the `backend/` service.

## Recommended (pip-tools)

### 1. Install pip-tools in a clean virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate

# Pin pip to a version compatible with pip-tools
pip install "pip<25.3"

# Install pip-tools
pip install pip-tools

```

### 2. Compile a pinned `requirements.txt` from `requirements.in`:

```bash
pip-compile requirements.in --output-file requirements.txt
```

### 3. Install pinned deps when you develop or in CI:

```bash
pip-sync requirements.txt
```

## Alternative (poetry/hatch)

If you manage dependencies with poetry or hatch, produce a lockfile and export a requirements.txt for container builds:

```bash
poetry lock && poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Notes

The repository's `pyproject.toml` remains the source of truth for development tooling (mypy, ruff, etc.). `requirements.in` mirrors the runtime constraints so teams can generate fully pinned `requirements.txt` files per environment.
