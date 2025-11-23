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

- Repo‑Struktur mit Frontend (Vite, Vue/React artifacts vorhanden -> Frontend muss entsprechend noch angepasst werden (dort ist meine Testversion)) und Backend (FastAPI) ist angelegt.
- Docker‑Compose ist vorhanden und enthält Dienste für Backend und Postgres.
- SHAP ist als Backend‑Dependency installiert bzw. vorgesehen; es gibt einen Fallback‑Mechanismus.
- Linter/Formatter und Test‑Frameworks sind eingerichtet: Ruff / Pytest (Backend) und Vitest / Playwright (Frontend).
- Alembic ist im Backend vorhanden (DB‑Migrationen vorbereitet).

---

## Offene Punkte (Was noch fehlt / Sollte geprüft werden)

- Frontend: Ein klarer, getesteter Formular‑Flow zum Erstellen/Selektieren einer Person (inkl. Validierung, Fehler‑Handling). + neues Frontend
- Backend: Sicherstellen, dass `POST /api/v1/predict` existiert, Input/Output Schema (Pydantic) definiert und das Modell geladen wird.
- SHAP: Implementierung eines stabilen Explainability‑Outputs — strukturierte JSON‑SHAP; Performance/Asynchronität bedenken.
- Feedback: DB‑Tabelle `feedback` (oder ähnlich) anlegen + Endpoint `POST /api/v1/feedback` implementieren und persistieren.
- Tests: Unit‑Tests für Endpoints, Integrationstests mit Postgres, E2E Tests (Playwright) für den Frontend‑Flow.
- CI: GitHub Actions so konfigurieren, dass Linting, Tests und ggf. Docker‑Build automatisch laufen.

---

## Werkzeuge — Kurzübersicht 

- Frontend: Vue 3 (oder React‑Artefakte vorhanden), TypeScript, Vite, Vitest, Playwright, pnpm
- Backend: FastAPI, Pydantic, SQLModel/SQLAlchemy, Alembic, Pytest, Ruff
- DB: PostgreSQL (persistentes Feedback, optional Patienten)
- Explainability: SHAP (strukturierte Werte + Plots)
- DevOps: Docker + docker‑compose, GitHub Actions

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


---

## Was entfernt werden muss (aus vorherigem Testen), nicht zu MVP:
    - komplette Datenbank mit Postgres: SQLite reicht → kein Adminer, kein Docker-DB-Setup
    
    - Alembic-Migrationen → Für MVP komplett unnötig?
    
    - CSV-Import, Seed-Daten?

    - Logging, Monitoring, Deploy-Pipelines

    - Architektur wie DDD, Services
