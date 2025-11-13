# backend/app/models

SQLModel- und Pydantic-Modelle für die Datenbank und API.

Hinweise:
- Modelle beeinflussen DB-Migrationen (Alembic). Nach Modelländerungen: `alembic revision --autogenerate -m "..."` und `alembic upgrade head`.
- Trenne Datenbank-Modelle von Pydantic-Schemas, wenn Klarheit über IO nötig ist.

Konventionen:
- Ein Modell pro Datei ist üblich (z. B. `user.py`, `item.py`).
- Tests für Modelle gehören nach `backend/app/tests/`.
