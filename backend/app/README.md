# backend/app

This folder contains the main backend application code.

Key subdirectories:
- `api/` — API endpoints (routes, router modules)
- `core/` — Core configurations, auth, settings, and helper functions
- `models/` — SQLModel/Pydantic models and trained ML models
- `tests/` — Backend unit and integration tests

See also: `../README.md` for general backend instructions and development workflows.

Quick reference:
- Dependencies: see `backend/README.md`
- Tests: `bash ./scripts/test.sh` (from the `backend/` directory)
- Migrations: Alembic is configured under `backend/app/alembic/`
