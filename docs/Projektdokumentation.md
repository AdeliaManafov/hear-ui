# HEAR‑Projekt — Projektdokumentation

> **Cochlea-Implantat Entscheidungsunterstützung** — Eine Webanwendung zur Unterstützung ärztlicher Entscheidungen bei Cochlea-Implantaten mit KI-gestützter Erfolgsvorhersage und SHAP-Erklärungen.

## Quick Start

```bash
cd hear-ui
docker compose up -d --build     # Alle Services starten
docker compose down              # Services stoppen
docker compose logs -f backend   # Logs verfolgen
```

Tests per Docker ausführen: 

```bash
docker compose build backend
docker compose run --rm backend pytest app/api/tests/ -v
```

**URLs nach dem Start:**
| Service | URL | Beschreibung |
|---------|-----|--------------|
| Frontend | http://localhost:5173 | Vue 3 Benutzeroberfläche |
| Backend API | http://localhost:8000 | FastAPI REST-Endpunkte |
| Swagger Docs | http://localhost:8000/docs | Interaktive API-Dokumentation zum Testen |
| Adminer (DB GUI) | http://localhost:8080 | PostgreSQL Datenbank-Verwaltung |

---

## Inhaltsverzeichnis

- [Projektstand](#projektstand)
- [Architektur](#architektur)
- [API-Endpunkte](#api-endpunkte)
- [Tech-Stack](#tech-stack)
- [Zeitplan](#zeitplan)
- [Demo-Anleitung](#demo-anleitung)
- [Entwicklung](#entwicklung)

---

## Projektstand

**Stand: 30. November 2025 | Branch: `model-integration`**

###  Abgeschlossen

| Komponente | Status | Details |
|------------|--------|---------|
| **Backend API** |  | FastAPI mit Predict, SHAP, Feedback, Patients Endpoints |
| **ML-Modell** |  | LogisticRegression (`logreg_best_model.pkl`) mit 68 Features |
| **SHAP Explainability** |  | Koeffizient-basierte Feature-Importance, Top-5 Features |
| **Datenbank** |  | PostgreSQL mit Alembic-Migrationen |
| **Frontend** |  | Vue 3 mit PatientForm, PredictionResult, ShapExplanation, FeedbackForm |
| **Docker Setup** |  | docker-compose mit Backend, Frontend, DB, Adminer |
| **Tests** |  | ~161 Backend-Tests vorhanden (pytest) |
| **Pydantic V2** |  | Migration abgeschlossen |
| **FastAPI Lifespan** |  | Moderne Event-Handling ohne Deprecation-Warnings |

###  Testdaten
- Patienten mit vollständigen Daten für SHAP-Erklärungen vorhanden
- Echte Patienten aus `Dummy Data_Cochlear Implant.csv` importierbar
- Vorhersage-Bereich: ca. 22% - 100%

###  Nächste Schritte (Priorisiert)

1. **Feature-Name-Mapping** — Technische Feature-Bezeichnungen (`cat__...`, `num__...`) in klinische Labels übersetzen
2. **E2E-Tests** — Playwright-Szenarien für Formular → Predict → SHAP → Feedback
3. **SHAP Background erweitern** — Mehr echte Patienten für stabilere Erklärungen

---

## Architektur

```
          
    Frontend          Backend        PostgreSQL    
   Vue 3 + TS             FastAPI              + Alembic     
   Port: 5173            Port: 8000            Port: 5433    
          
                                 
                        
                           ML Pipeline   
                          LogReg + SHAP  
                        
```

### Frontend-Komponenten

| Komponente | Datei | Beschreibung |
|------------|-------|--------------|
| PatientForm | `PatientForm.vue` | Eingabeformular für Patientendaten |
| PredictionResult | `PredictionResult.vue` | Anzeige der Vorhersage (Wahrscheinlichkeit) |
| ShapExplanation | `ShapExplanation.vue` | Visualisierung der Feature-Importance |
| FeedbackForm | `FeedbackForm.vue` | Klinisches Feedback erfassen |

### Backend-Module

| Modul | Pfad | Beschreibung |
|-------|------|--------------|
| `model_wrapper.py` | `app/core/` | ML-Modell laden und Predictions |
| `shap_explainer.py` | `app/core/` | SHAP-Erklärungen generieren |
| `preprocessor.py` | `app/core/` | Feature-Transformation |
| `background_data.py` | `app/core/` | SHAP Background-Samples |

---

## Tech-Stack

### Frontend

| Tool | Version | Zweck |
|------|---------|-------|
| Vue 3 | ^3.3.4 | UI-Framework |
| TypeScript | ^5.2.2 | Typisierung |
| Vite | ^5.4.14 | Build-Tool |
| Vue Router | ^4.2.5 | Routing |
| Vitest | ^1.3.0 | Unit-Tests |
| Playwright | ^1.45.2 | E2E-Tests |
| pnpm | - | Package Manager |
| ESLint | ^8.44.0 | Linting |

### Backend

| Tool | Version | Zweck |
|------|---------|-------|
| FastAPI | >=0.114.2 | Web-Framework |
| Pydantic | >2.0 | Validierung |
| SQLModel | >=0.0.21 | ORM |
| Alembic | >=1.12.1 | DB-Migrationen |
| SHAP | >=0.41.0 | Explainability |
| pytest | >=7.4.3 | Tests |
| Ruff | >=0.2.2 | Linting |
| testcontainers | >=3.7.0 | Integrationstests |

### Infrastruktur

| Tool | Zweck |
|------|-------|
| Docker Compose | Container-Orchestrierung |
| PostgreSQL 12 | Datenbank |
| Adminer | DB-GUI |
| Traefik | Reverse Proxy (Produktion) |
| GitHub Actions | CI/CD |

---

## API-Endpunkte

### Vorhersage & Erklärung

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `POST` | `/api/v1/predict/` | Direkte Vorhersage (optional: `?persist=true`) |
| `POST` | `/api/v1/explainer/explain` | Ad-hoc SHAP-Erklärung |

### Patienten

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `GET` | `/api/v1/patients/` | Patientenliste |
| `GET` | `/api/v1/patients/{id}` | Patient-Details |
| `GET` | `/api/v1/patients/{id}/predict` | Vorhersage für Patient |
| `GET` | `/api/v1/patients/{id}/explainer` | SHAP-Erklärung für Patient |
| `GET` | `/api/v1/patients/{id}/validate` | Patientendaten validieren |
| `POST` | `/api/v1/patients/upload` | CSV-Upload |

### Feedback

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `POST` | `/api/v1/feedback/` | Feedback erstellen |
| `GET` | `/api/v1/feedback/{id}` | Feedback abrufen |

### Utils

| Methode | Pfad | Beschreibung |
|---------|------|--------------|
| `GET` | `/api/v1/utils/health-check/` | Gesundheitscheck |
| `GET` | `/api/v1/utils/model-info/` | Modell-Informationen |
| `GET` | `/api/v1/utils/feature-names/` | Feature-Namen |
| `GET` | `/api/v1/utils/feature-categories/` | Feature-Kategorien |

---

## Zeitplan

| Meilenstein | Datum | Status |
|-------------|-------|--------|
| Setup Meeting | 2025-10-29 |  |
| MS1 (MVP) | 2025-11-14 |  |
| MS2 (Prototype 1) | 2025-11-26 |  Backend fertig |
| **MS3 (Prototype 2)** | 2025-12-19 |  Aktuell — SHAP & Frontend |
| MS4 (Release Prep) | 2026-01-23 | ⏳ Frontend-Erweiterungen |
| Final Deliverable | 2026-02-27 | ⏳ Abgabe |

---

## Demo-Anleitung

### 1. Services starten

```bash
cd hear-ui
docker compose up -d --build
docker compose ps  # Prüfen: backend, db, frontend sind Up
```

### 2. Health-Check

```bash
curl -sS http://localhost:8000/api/v1/utils/health-check/ | jq
# Erwartung: {"status":"ok"}
```

### 3. Vorhersage testen

```bash
curl -sS -X POST "http://localhost:8000/api/v1/predict/" \
  -H "Content-Type: application/json" \
  -d '{"age":55, "hearing_loss_duration":12.5, "implant_type":"type_b"}' | jq
```

### 4. SHAP für Patient abrufen

```bash
# Validiere Patient zuerst
curl -sS "http://localhost:8000/api/v1/patients/9c4408e6-2aef-44c1-ae95-dd409141f647/validate" | jq

# SHAP-Erklärung
curl -sS "http://localhost:8000/api/v1/patients/9c4408e6-2aef-44c1-ae95-dd409141f647/explainer" | jq
```

### 5. Feedback erstellen

```bash
curl -sS -X POST "http://localhost:8000/api/v1/feedback/" \
  -H "Content-Type: application/json" \
  -d '{"input_features": {"age": 55}, "prediction": 0.85, "accepted": true}' | jq
```

### Wichtige Patienten-IDs (SHAP-geeignet)

| Patient | ID | Vorhersage |
|---------|----|-----------:|
| Patient 1 (prälingual) | `9c4408e6-2aef-44c1-ae95-dd409141f647` | 97.3% |
| Patient 2 (postlingual) | `86bab602-7ffc-4663-aced-567905bed3bd` | 100% |
| Patient 3 (syndromal) | `2b7414f6-471a-4bf8-8998-1385543a40b3` | 22.1% |
| Patient 4 (perilingual) | `21bfdee0-4207-4ac2-925d-b557f14ab39e` | 81.1% |
| Patient 5 (prälingual) | `a9e0736c-05fb-490b-940b-b275be3158e3` | 97.3% |

---

## Entwicklung

### Lokale Entwicklung

```bash
# Backend
cd backend
pip install -e .
uvicorn app.main:app --reload

# Frontend
cd frontend
pnpm install
pnpm dev
```

### Migrationen

```bash
# Im Container
docker compose exec backend alembic upgrade head

# Neue Migration erstellen
docker compose exec backend alembic revision --autogenerate -m "description"
```

### Tests

```bash
# Backend-Tests
docker compose exec backend pytest -v

# Mit Coverage
docker compose exec backend pytest --cov=app --cov-report=term-missing

# Frontend-Tests
cd frontend && pnpm test
```

### Logs & Debugging

```bash
# Backend-Logs
docker compose logs -f backend

# DB-Zugang
docker compose exec db psql -U postgres -d hear_db
```

### DB-Zugang via Adminer

1. Öffne http://localhost:8080
2. System: PostgreSQL
3. Server: `db`
4. Username: `postgres`
5. Password: siehe `.env`
6. Database: `hear_db`

---

## Beispiel-Responses

### Predict Response

```json
{
  "prediction": 0.772,
  "explanation": {}
}
```

### SHAP Response

```json
{
  "prediction": 0.736,
  "feature_importance": {
    "num__Alter [J]": 0.039,
    "cat__Diagnose...postlingual": -0.089
  },
  "top_features": [
    {"feature": "postlingual", "importance": -0.089},
    {"feature": "Alter [J]", "importance": 0.039}
  ],
  "base_value": 0.846
}
```

### Feedback Response

```json
{
  "id": "e7c6cadb-05bf-4c3b-986e-dc2881845251",
  "input_features": {"age": 55},
  "prediction": 0.85,
  "accepted": true,
  "created_at": "2025-11-30T10:00:00"
}
```

---

## Projektstruktur

```
hear-ui/
 backend/
    app/
       api/routes/      # API-Endpoints
       core/            # ML, SHAP, Config
       models/          # DB-Modelle + ML-Pipeline
       tests/           # Backend-Tests
    alembic.ini
    pyproject.toml
 frontend/
    src/
       components/      # Vue-Komponenten
       routes/          # Routing
       App.vue
    package.json
    vite.config.ts
 docs/
    Projektdokumentation.md
    api-examples/
 docker-compose.yml
 .env
```

---

*Letzte Aktualisierung: 30.11.2025*