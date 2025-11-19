# Apply Alembic Migrations (backend)

This small helper is provided for local development to run Alembic migrations
using the project's `.env` file.

Usage (from repository root):

```bash
cd hear-ui
./backend/scripts/apply_migrations.sh
```

Requirements:
- Python and project's dependencies installed (recommended in a virtualenv).
- A `.env` file present at `hear-ui/backend/.env` (copy from `.env.example` and fill DB credentials).

What it does:
- Sources `.env` into the environment.
- Runs `python -m alembic upgrade head` inside the `backend` folder.

Notes:
- For production or CI, prefer running Alembic inside the same environment/container
  as the backend (so the same DB driver/versions are used).
- This script is intended for local dev only.
