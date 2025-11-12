# HEAR‑UI — Projektstatus & TODO

Datum: 2025-11-12

Dieses Dokument fasst zusammen, was bereits erledigt wurde und welche Arbeiten noch offen sind. Es ist als single source of truth für den aktuellen Stand im Branch `feature/backend-setup` gedacht.

## Kurzüberblick
- Branch: `feature/backend-setup`
- Hauptziele: Predict‑Endpoint vorhanden (Dummy), SHAP‑like Erklärung, Repo‑Hygiene (scripts, .env.example), Dokumentation. Modellintegration, Persistenz und Tests noch offen.

## Bereits erledigt (gehört committed & gepusht)
- API
  - `backend/app/api/routes/predict.py` — kanonischer Predict‑Router mit `POST /predict` (response_model `PredictResponse`) und Dummy‑Vorhersage / SHAP‑like Erklärung.
  - `backend/app/api/api.py` — zentraler `api_router` importiert und inkludiert `predict.router`.
  - Doppelte predict‑Implementierungen archiviert unter `backend/app/api/archived/`.

- Core
  - `backend/app/core/predict.py` — `dummy_predict()` helper vorhanden.
  - `backend/app/core/config.py` — `PROJECT_NAME` konsolidiert (`hear ui`).

- Repo & Devops Hygiene
  - `scripts/init-dev.sh` — sicherer, idempotenter Bootstrap von `.env.example` → `.env` (ausführbar).
  - `.env.example` erstellt; `.gitignore` so angepasst, dass `.env` ignoriert wird.
  - `backend/SCRIPTS.md` hinzugefügt (Dokumentation wo Skripte liegen und wie `init-dev.sh` zu benutzen ist).
  - Top‑Level docs in `docs/` verschoben / ergänzt (z. B. `docs/ci-cd.md` falls vorhanden).

- Git
  - Alle Änderungen committed und gepusht in `feature/backend-setup`.

## Was noch gemacht werden soll (priorisiert)

### H1 — Unmittelbar / kritisch
1. Verlässliche lokale Laufumgebung starten (Docker Compose mit Backend + Postgres) — damit Tests und OpenAPI verlässlich geprüft werden können.
2. Predict API: vorbereitende Tests + Contract (unit + integration) — damit das reale Modell am Freitag einfach integriert werden kann.
3. Feedback Persistence: `Feedback` SQLModel + CRUD + `POST /api/v1/feedback` + Alembic‑Migration oder Migration Skeleton.

### H2 — Nach Modelllieferung (kurzfristig)
4. Modellintegration: Modell‑Wrapper (`app/core/model.py`) mit `load`, `predict` und Feature‑Schema.
5. SHAP‑Explainer: Explainer Wrapper, effiziente Erklärungsstrategie (TreeExplainer / approximativ für teure Modelle).
6. Tests erweitern: Integrationstests, API‑Tests; E2E (Playwright) für Frontend‑Flows.

### H3 — Stabilisierung / Delivery
7. CI/CD: GitHub Actions für lint & tests (ruff + pytest + optional mypy).
8. Code quality: Ruff + Black + pre-commit hooks.
9. Dockerfile Optimierung & Production readiness (healthchecks, env handling).
10. Frontend (Vue) – UI, Anbindung an `/api/v1/predict` und Feedback‑UI.

## Detaillierte Aufgaben / Vorschläge

- Feedback Model (Beispiel):
  - Datei: `backend/app/models/feedback.py` (SQLModel)
  - Felder: id, predict_input (JSON), prediction, user_agree (bool), comment, created_at
  - CRUD: `backend/app/crud.py` → `create_feedback` + tests
  - Endpoint: `backend/app/api/routes/feedback.py` → `POST /api/v1/feedback`

- Predict Contract (empfohlen):
  - Request: Pydantic `PatientData` (definiere Felder sobald Modell geliefert wird)
  - Response: `PredictResponse` = { prediction: float, explanation: Dict[str,float] }

## How to verify (Schnelle Schritte)
- Docker Compose (empfohlen):
```
docker compose up --build -d
curl -sS http://127.0.0.1:8000/api/v1/openapi.json | jq -r '.paths | keys[]' | grep predict || true
open http://127.0.0.1:8000/docs
```
- Lokal (venv) — falls Docker nicht möglich:
```
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -e .
PYTHONPATH=$(pwd) .venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Hinweis: beim lokalen Start können Abhängigkeiten fehlen (psycopg2, passlib, pydantic-settings, emails, …). Docker Compose vermeidet diese Probleme.

## Modelllieferung (Fr., Datum)
- Wenn du das Modell am Freitag bekommst, liefere bitte kurz das Format (pickle/joblib/ONNX/pytorch/etc.) und die Liste der Input‑Features. Ich schreibe dann den Model‑Adapter und die Tests so, dass Integration schnell möglich ist.

## Branches / Commits & Verantwortlichkeit
- Branch für Feature‑Arbeiten: `feature/backend-setup` (aktuell die Änderungen dort).
- Vorschlag: Öffne für jedes H1‑Item einen separaten Feature‑Branch (z. B. `feature/feedback-model`, `feature/predict-tests`) und mache PRs gegen `develop` oder `main` je nach Workflow.

## Offen / Entscheidungen nötig
- Soll `backend/.env` aus der Historie entfernt werden (es enthält reale Werte) oder reicht ein Commit, das `.env` künftig ignoriert? (Empfohlen: History bereinigen oder Datei entfernen, `.env.example` nutzen)
- Format für `PROJECT_NAME` (klein: `hear ui` vs. `Hear UI` vs. `Hear-UI`) — zur einheitlichen Darstellung in UI/Docs.

---

Wenn du willst, kann ich jetzt direkt eines der H1‑Items umsetzen: z.B. A) Docker Compose Start + OpenAPI‑Check, B) Test‑Scaffold für Predict, oder C) Feedback‑Model scaffolding. Schreibe A, B oder C — ich erledige das und commite die Änderungen.
