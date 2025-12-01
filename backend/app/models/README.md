# backend/app/models

SQLModel and Pydantic models for the database and API.

Notes:
- Models affect DB migrations (Alembic). After model changes: `alembic revision --autogenerate -m "..."` and `alembic upgrade head`
- Separate database models from Pydantic schemas when clarity about IO is needed

Conventions:
- One model per file is common (e.g., `user.py`, `item.py`)
- Tests for models belong in `backend/app/tests/`

ML Models:
- `logreg_best_model.pkl` — Trained LogisticRegression model for CI success prediction
