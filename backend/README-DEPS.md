# Backend dependencies and locking

This file documents how to produce a reproducible, pinned Python dependency file for the `backend/` service.

Recommended (pip-tools)

1. Install pip-tools in a clean virtualenv:

   python -m venv .venv
   source .venv/bin/activate
   pip install pip-tools

2. Compile a pinned `requirements.txt` from `requirements.in`:

   pip-compile requirements.in --output-file requirements.txt

3. Install pinned deps when you develop or in CI:

   pip-sync requirements.txt

Alternative (poetry/hatch)

- If you manage dependencies with poetry or hatch, produce a lockfile and export a requirements.txt for container builds:

  poetry lock && poetry export -f requirements.txt --output requirements.txt --without-hashes

Notes
- The repository's `pyproject.toml` remains the source of truth for development tooling (mypy, ruff, etc.). `requirements.in` mirrors the runtime constraints so teams can generate fully pinned `requirements.txt` files per environment.
