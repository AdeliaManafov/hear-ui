# HEAR‑UI — Projektstatus & MVP‑Zusammenfassung

Datum: 2025-11-21

## Ziel des MVP

Kernziel: Ein reproduzierbares, end‑to‑end Demo, das zeigt, wie die KI bei der Entscheidung zur Cochlea‑Implantat‑Empfehlung unterstützt.

Minimaler Funktionsumfang (MVP):

- Ein valides Eingabeformular im Frontend zur Eingabe/Selektion von Patientendaten
- `POST /api/v1/predict` Endpoint: liefert Wahrscheinlichkeit + Label
- SHAP‑Erklärungen (strukturierte SHAP‑Werte als JSON oder base64‑Plot)
- `POST /api/v1/feedback` Endpoint: persistiert Feedback in PostgreSQL
- Reproduzierbare Umgebung via `docker-compose`

---

## Aktueller Projektstatus (Was erledigt wurde)

- Repo‑Struktur mit Frontend (Vite, Vue/React artifacts vorhanden) und Backend (FastAPI) ist angelegt.
- Docker‑Compose ist vorhanden und enthält Dienste für Backend und Postgres.
- SHAP ist als Backend‑Dependency installiert bzw. vorgesehen; es gibt einen Fallback‑Mechanismus.
- Linter/Formatter und Test‑Frameworks sind eingerichtet: Ruff / Pytest (Backend) und Vitest / Playwright (Frontend).
- Alembic ist im Backend vorhanden (DB‑Migrationen vorbereitet).

---

## Offene Punkte (Was noch fehlt / Sollte geprüft werden)

- Frontend: Ein klarer, getesteter Formular‑Flow zum Erstellen/Selektieren einer Person (inkl. Validierung, Fehler‑Handling).
- Backend: Sicherstellen, dass `POST /api/v1/predict` existiert, Input/Output Schema (Pydantic) definiert und das Modell geladen wird.
- SHAP: Implementierung eines stabilen Explainability‑Outputs — strukturierte JSON‑SHAP oder base64‑Plot; Performance/Asynchronität bedenken.
- Feedback: DB‑Tabelle `feedback` (oder ähnlich) anlegen + Endpoint `POST /api/v1/feedback` implementieren und persistieren.
- Tests: Unit‑Tests für Endpoints, Integrationstests mit Postgres, E2E Tests (Playwright) für den Frontend‑Flow.
- CI: GitHub Actions so konfigurieren, dass Linting, Tests und ggf. Docker‑Build automatisch laufen.

---

## Vorschlag: API‑Spezifikation (MVP)

1) Predict

- Methode: `POST /api/v1/predict`
- Body (Beispiel, Pydantic):

```
{
  "patient_id": "optional|string",
  "age": 67,
  "hearing_measure_1": 45.0,
  "feature_x": "...",
  // weitere Features entsprechend Modell
}
```

- Response (200):

```
{
  "probability": 0.82,
  "label": "recommend",
  "explanation": { /* optional: strukturierte SHAP Werte oder base64 */ }
}
```

2) Feedback

- Methode: `POST /api/v1/feedback`
- Body (Beispiel):

```
{
  "patient_id": "string|optional",
  "predicted_label": "recommend|not_recommend",
  "user_feedback": "agree|disagree",
  "comment": "optional string",
  "timestamp": "ISO8601 optional (server kann setzen)"
}
```

- Response (201): `{ "status": "saved", "id": 123 }`

DB‑Schema Vorschlag (minimal, PostgreSQL):

```
CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  patient_id TEXT,
  predicted_label TEXT,
  user_feedback TEXT,
  comment TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

Optional: `patients` Tabelle zum langfristigen Speichern von Patienten (sinnvoll für Demo‑Daten).

---

## Explainability (SHAP) — Optionen für MVP

- Strukturierte SHAP JSON: { feature: value, shap_value: x } — leicht zu visualisieren im Frontend.
- Base64‑encodiertes Plot: schneller für Demo/Präsentation in UI (Bild einbetten), aber weniger interaktiv.
- Empfehlung: Beide unterstützen; MVP: strukturierte JSON + einfache Barplot als base64 (für UI‑Preview).

---

## Tests & Qualitätssicherung

- Backend: Pytest Unit‑Tests für Pydantic‑Modelle, Endpoint Tests (TestClient) und Integrationstests gegen Postgres (Testcontainers oder dev‑postgres).
- Frontend: Unit‑Tests für Formular/Components mit Vitest; E2E Tests with Playwright für kompletten Flow.
- CI: GitHub Actions Pipeline für Lint → Unit Tests → Integration/E2E (optional, ggf. in separaten Jobs).

---

## Docker / Reproduzierbarkeit

- Die vorhandene `docker-compose.yml` sollte folgende Dienste enthalten: `backend`, `frontend`, `postgres`, optional `adminer`.
- Für Demos: dev‑Compose mit seeded DB (CSV Import beim Start) und exposed ports (Backend 8000, Frontend 5173, Adminer 8080).

Empfohlene Dev‑Start Befehle (lokal, im Repo‑Root):

```bash
docker compose up --build
# oder (wenn legacy) docker-compose up --build
```

---

## Roadmap / Nächste Schritte (konkret)

1. Implementiere/prüfe `POST /api/v1/predict` im Backend (inkl. Modell‑Wrapper und Pydantic Schemas).
2. Implementiere SHAP‑Erklärungen: strukturierte JSON und optional base64 Barplot.
3. Erstelle Feedback‑Table + `POST /api/v1/feedback` Endpoint und Alembic Migration.
4. Frontend: Formular + Hook zum Aufruf von `/predict` und Darstellung der Erklärung; Feedback UI (agree/disagree).
5. Tests: Unit & Integration; E2E Playwright Test für End‑to‑End Flow.
6. CI: GitHub Actions Jobs für Lint, Tests, Build.

---

## Werkzeuge — Kurzübersicht (für Team‑Onboarding)

- Frontend: Vue 3 (oder React‑Artefakte vorhanden), TypeScript, Vite, Vitest, Playwright, pnpm
- Backend: FastAPI, Pydantic, SQLModel/SQLAlchemy, Alembic, Pytest, Ruff
- DB: PostgreSQL (persistentes Feedback, optional Patienten)
- Explainability: SHAP (strukturierte Werte + Plots)
- DevOps: Docker + docker‑compose, GitHub Actions

---

Wenn ihr möchtet, kann ich jetzt:

- 1) die `feedback`‑Tabelle + eine erste Alembic‑Migration als Patch anlegen,
- 2) einen minimalen `POST /api/v1/feedback` Endpoint in `backend/app` anlegen,
- 3) oder das `predict` Endpoint‑Schema / Beispiel‑Response in der `MVP_Summary.md` erweitern.

Bitte sagt mir, welchen der nächsten Schritte ich direkt umsetzen soll.

---

## Kurzüberblick / MVP (konkret)

Für das MVP konzentrieren wir uns auf einen klaren End-to-End-Flow:

- Frontend: Formular zum Eingeben einer Person (Patientendaten).
- Backend:
    - Predict‑Endpoint (POST /api/v1/predict) → gibt Wahrscheinlichkeit + Label zurück.
    - SHAP‑Erklärungen → strukturierte SHAP‑Werte (JSON) oder base64‑Plot.
    - Feedback‑Endpoint (POST /api/v1/feedback) → persistiert Feedback in Postgres.
- Datenpersistenz: Postgres speichert Feedback + ggf. Patienten/Tabelle. CSV‑Import nur fürs initiale Seeding möglich.
- Reproduzierbarkeit: komplette Umgebung per docker-compose.

=> Ziel: Damit können wir bereits echte Ergebnisse zeigen, auch wenn noch nicht alle Features ausgebaut sind.

**Zusammenfassung:**

Der minimale Funktionsumfang enthält:

- ein valides Eingabeformular im Frontend
- einen funktionierenden Predict-Endpoint
- eine einfache Erklärung (z. B. SHAP-Ranking oder Barplot)
- eine Feedback-Tabelle mit Storage in PostgreSQL
- ein reproduzierbares Setup über Docker-Compose

---

## Was noch fehlt (konkret für das MVP)

Die folgenden Punkte sind noch umzusetzen, damit das MVP vollständig funktioniert:

- Frontend
  - Validiertes Eingabeformular (Formularfelder, clientseitige Validation, Fehleranzeigen)
  - Anzeige der Vorhersage (Wahrscheinlichkeit + Label)
  - Anzeige der Erklärung (SHAP‑Ranking oder simpler Barplot)
  - Feedback‑UI (agree/disagree + optionaler Kommentar), das `POST /api/v1/feedback` aufruft

- Backend
  - Modell‑Wrapper für Laden und Vorverarbeitung des bereitgestellten Modells
  - Implementierung von `POST /api/v1/predict` mit Pydantic‑Schemata und Tests
  - SHAP‑Erzeugung: strukturierte SHAP‑JSON und optional base64‑Plot (inkl. Timeouts/Fallback)
  - Implementierung von `POST /api/v1/feedback` und Persistierung in Postgres

- Datenbank & Seeding
  - Alembic‑Migration(en) für `feedback` (und optional `patients`) Tabelle
  - CSV‑Importskript zum initialen Befüllen der DB für Demos

- Infrastruktur & Tests
  - `docker-compose` sicherstellen (backend, frontend, postgres, optional adminer)
  - Unit‑ und Integrationstests (pytest) für Backend, Vitest für Frontend, Playwright E2E‑Tests
  - CI‑Jobs (Lint → Tests → Build)

- Betrieb & Qualität
  - Logging, Error‑Handling, Health‑Checks
  - CORS, env/secret management, minimale Sicherheitsmaßnahmen

Diese Liste beschreibt die minimalen verbleibenden Arbeiten, geordnet nach Priorität für das MVP.
