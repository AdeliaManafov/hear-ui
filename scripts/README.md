# Scripts

Helper scripts for development, build and tests used in the HEAR UI project.

This file documents the most important scripts in the repository (`scripts/` and
`backend/scripts/`) and explains how to use them safely.

Prerequisites
-------------
- Docker and Docker Compose (or Docker Engine with `docker compose`).
- Node/npm or pnpm for frontend tasks (if you run frontend commands locally).
- Python (recommended inside a virtualenv) for backend tasks.
- Make scripts executable if needed: `chmod +x scripts/*.sh backend/scripts/*.sh`.

Safety note
-----------
- Review `deploy.sh` and `build-push.sh` before running — they may push images
	or interact with remote systems.
- Do not commit real secrets. The repository contains `*.example` env files that
	should be copied to `.env` and edited locally.

Common workflows (examples)
---------------------------
- Initialize local dev environment:
```bash
./scripts/init-dev.sh
```
- Run tests (CI-style, teardown at the end):
```bash
./scripts/test.sh
```
- Run tests locally (keep containers running for inspection):
```bash
./scripts/test.sh --local
# or the wrapper
./scripts/test-local.sh
```

Scripts overview
----------------
Top-level `scripts/`
- `init-dev.sh` — Bootstrap local `.env` from `.env.example`. Safe: does not overwrite an
	existing `.env`.
	Usage: `./scripts/init-dev.sh`

- `test.sh` — Unified test runner. Supports `--local` for developer friendly runs
	(keeps containers running). Default is CI-style (teardown after run).
	Usage: `./scripts/test.sh [--local]`

- `test-local.sh` — Lightweight wrapper for backwards compatibility that calls
	`./scripts/test.sh --local`.
	Usage: `./scripts/test-local.sh`

- `build.sh` — Build frontend and/or images locally (project-specific behaviour).
	Usage: `./scripts/build.sh`

- `build-push.sh` — Build images and push to registry. Requires Docker and
	registry credentials. Review before running.
	Usage: `./scripts/build-push.sh`

- `generate-client.sh` — Generate frontend API client from OpenAPI spec (if used).
	Usage: `./scripts/generate-client.sh`

Backend `backend/scripts/`
- `format.sh` — Format and sort imports (black/isort/ruff or similar).
	Usage: `./backend/scripts/format.sh`

- `test.sh` — Run backend tests (pytest). Typically used inside CI or dev.
	Usage: `./backend/scripts/test.sh`

- `apply_migrations.sh` — Load `.env` and run Alembic migrations (important for
	schema changes). Only run against a test/local DB unless you intend to
	migrate production.
	Usage: `./backend/scripts/apply_migrations.sh`

- `tests-start.sh` — Setup helper used by `docker compose exec` to run tests
	inside the backend container (e.g. start test DB, mailcatcher, etc.).

- `lint.sh` — Run linters (ruff/flake8 or similar). Useful to keep code quality.

- `prestart.sh` — Prestart checks executed before starting the backend service
	(DB availability, migrations, initial data). Used by container entrypoints.

Permissions
-----------
Make sure executable scripts have the execute bit set. From the repository root:
```bash
chmod +x scripts/*.sh backend/scripts/*.sh
```

Troubleshooting
---------------
- If docker-compose fails, check your Docker daemon and available resources.
- If a script behaves differently on Windows developers, ensure line endings
	are normalized (the repo contains `.gitattributes` enforcing `LF` for `*.sh`).