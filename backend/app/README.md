# backend/app

Dieser Ordner enthält den Hauptcode der Backend-Anwendung.

Wichtige Unterordner:
- `api/` — API-Endpunkte (Routes, Router-Module).
- `core/` — Kernkonfigurationen, Auth, Settings und Hilfsfunktionen.
- `models/` — SQLModel-/Pydantic-Modelle.
- `routes/` — Routen-Module, die die Endpunkte zusammenstellen.
- `tests/` — Backend-Tests für Unit- und Integrationstests.

Siehe auch: `../README.md` für allgemeine Backend-Anweisungen und Entwicklungs-Workflows.

Kurzanleitung:
- Abhängigkeiten: siehe `backend/README.md`.
- Tests: `bash ./scripts/test.sh` (vom `backend/`-Ordner aus).
- Migrationen: Alembic ist unter `backend/app/alembic/` konfiguriert.
