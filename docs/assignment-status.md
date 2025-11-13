## HEAR — Projektstatus (Aufgabenstellung & Fortschritt)

Datum: 2025-11-12

Ziel (Kurz):
Für hörgeschädigte Patient:innen soll eine Webanwendung (Frontend + Backend) entwickelt werden, die die Vorhersage eines vorliegenden KI-Modells anzeigt, Ergebnisse mit erklärbarer KI (z. B. SHAP) visualisiert und Nutzerfeedback sammelt. Frontend und Backend kommunizieren über eine RESTful API. Die App läuft in Docker-Containern und wird durch Tests und CI abgesichert.

Aufgabenstellung (ausgeschrieben):
- Frontend: Eingabe oder Auswahl einer Person, Anzeige der KI-Vorhersage, Visualisierung erklärbarer KI-Ergebnisse, Nutzerfeedback (zustimmen/ablehnen).
- Backend: Aufruf des KI-Modells (Prediction), Aufruf des Erklärers (Explanation), Verwaltung von Nutzerfeedback.
- Technologien (Empfehlung): Frontend: Vue, TypeScript, Vite, Playwright; Backend: FastAPI, SQLAlchemy, Pytest; DB: Postgres. Containerisierung (Docker Compose). Tests: Unit/Integration/E2E, CI-Integration. Linter/Formatter (ruff/eslint).

---

Was bereits umgesetzt wurde (Stand branch `feature/backend-setup`)

- Backend:
  - `POST /api/v1/predict/` implementiert in `backend/app/api/routes/predict.py` (dummy prediction + SHAP-ähnliche Erklärung).
  - Router-Registrierung korrigiert (`backend/app/api/api.py`) — doppelte `/api/v1`-Prefix-Probleme behoben, Healthcheck erreichbar.
  - Alembic / Migrations: `alembic/env.py` angepasst, `asyncpg` zur Kompatibilität hinzugefügt.
  - Temporärer Kompatibilitäts-Shim `backend/app/db.py` existiert (sichert Imports/Alembic beim Umsortieren der Paketstruktur).
  - Dev scripts & docs: `backend/requirements.in`, `backend/requirements.txt` (gepinned), `backend/README-DEPS.md` hinzugefügt.
  - Compose & Runtime: `docker-compose.yml` + override angepasst; Host-Port-Konflikt für Postgres gelöst (host 5433 -> container 5432). Fehlendes externes Netzwerk `traefik-public` automatisiert/erzeugt beim Start.
  - Engine: Docker läuft unter Colima (macOS/ARM) — erfolgreich getestet.
  - Git: Änderungen committed und gepusht auf `feature/backend-setup`.

- Infrastruktur / Test-run:
  - Docker Compose-Stack startet, DB ist `healthy`, `backend` startet und `openapi.json` enthält `/api/v1/predict/`.
  - Ein smoke-test POST an `/api/v1/predict/` gab eine gültige Dummy-Antwort (HTTP 200).

---

Was noch fehlt / offene Punkte (Priorisiert)

1. High priority
   - Remove temporary shim: `backend/app/db.py` (aktuelle Kompatibilitäts-Schicht) und konsolidiere das DB-Paket (`app/db/`) mit sauberer `__init__.py` — dann Alembic/Imports testen.
   - Stabilize dependencies: review & pin (done partially) — aktuell ist `backend/requirements.txt` gepinnt; empfehle regelmäßiges `pip-compile`-Update und CI-Check.
   - Tests: Unit-Tests für `predict`-Route (pytest), Integrationstests (DB + Alembic) und E2E-Tests (Playwright or similar) — Tests müssen in CI laufen.

2. Medium priority
   - Dev DX: `docker-compose.override.dev.yml` mit bind-mounts und `uvicorn --reload` für schnellere Iteration.
   - CI: GitHub Actions (or other) to run linters (ruff), unit tests, and E2E (playwright) on PRs.
   - Add `.dockerignore` and optimize production Dockerfiles for smaller images and non-root runtime.

3. Low priority / Nice-to-have
   - Frontend: implement UI for selecting/entering patient data, display prediction + SHAP plots, and send feedback to backend.
   - Store feedback in DB + add admin view to export/inspect feedback.
   - Add monitoring (Sentry/snippets) and documentation for deployment.

---

Konkrete nächste Schritte (empfohlen, in Reihenfolge)

1. (High) Entferne den temporären Shim und führe Migrationen/Importtests aus. Wenn Probleme auftauchen, rolle die Änderung zurück und protokolliere die notwendigen `__init__.py`-Exports.
2. (High) Schreibe pytest-Unit-Tests für `backend/app/api/routes/predict.py` (happy path + validation error), füge die Tests zu CI hinzu.
3. (Med) Erstelle `docker-compose.override.dev.yml` (mount `./backend` und run `uvicorn --reload`) und dokumentiere `Makefile` oder `scripts/dev.sh` zum schnellen Start.
4. (Med) Erstelle minimalen Frontend-Prototyp (eine Seite), die JSON an `/api/v1/predict/` sendet und die Antwort anzeigt (z. B. `src/components/PredictForm.vue`).

Wie du die Arbeit lokal prüfen kannst (Kurzbefehle)

1. Stack hochfahren / Logs:
```bash
docker compose up -d --build
docker compose ps
docker compose logs --follow --tail=200 backend
```

2. OpenAPI / Smoke test:
```bash
curl http://127.0.0.1:8000/api/v1/openapi.json | jq .paths["/api/v1/predict/"]
curl -X POST -H 'Content-Type: application/json' -d '{"age":45,"hearing_loss_duration":5.2,"implant_type":"typeA"}' http://127.0.0.1:8000/api/v1/predict/
```

3. Tests (lokal mit venv oder innerhalb container):
```bash
# mit requirements.txt (empfohlen):
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
pip install pytest
pytest -q
```

Dateien, die bereits geändert/erstellt wurden (Auszug)
- `backend/app/api/routes/predict.py` — predict endpoint (dummy)
- `backend/app/api/api.py` — router aggregator, duplicate prefix fix
- `backend/app/alembic/env.py` — alembic DB URL adjustment
- `backend/app/db.py` — temporary shim (compatibility)
- `backend/requirements.in`, `backend/requirements.txt`, `backend/README-DEPS.md` — pinned deps + doc
- `docker-compose.override.yml` — fixed port mapping (host 5433 -> container 5432)

Branch mit Änderungen: `feature/backend-setup`

---