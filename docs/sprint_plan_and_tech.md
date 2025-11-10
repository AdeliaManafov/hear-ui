# HEAR — MVP, Technologies & Next Sprint

## 1️⃣ MVP Definition

Ziel: Schnelle, lauffähige Version, die Kliniker unterstützt

Funktionen (MVP Scope):

- Vorhersage: KI bewertet Erfolgswahrscheinlichkeit eines Cochlea‑Implantats anhand Patientendaten
- Erklärung: Einflussfaktoren verständlich visualisiert (SHAP / Barplot)
- Feedback: Zustimmung / Ablehnung durch Kliniker, Speicherung in DB

Beispiel‑Request (JSON):

```json
{
  "age": 45,
  "hearing_loss_duration": 10,
  "implant_type": "CI24"
}
```

Beispiel‑Response (Dummy):

```json
{
  "prediction": 0.65,
  "explanation": {
    "age": 0.2,
    "hearing_loss_duration": 0.3,
    "implant_type": 0.15,
    "other_feature": 0.1
  }
}
```

---

## 2️⃣ Technologies Chosen

Komponente | Technologie | Zweck
:---|:---|:---
Backend | FastAPI | API‑Server, OpenAPI / Swagger, JWT‑Auth
ORM / DB | SQLAlchemy + PostgreSQL | Datenpersistenz, Migrationen
Auth / Security | JWT + passlib/bcrypt | Benutzer‑Login / Schutz
Testing | Pytest | Unit‑ & Integrationstests
Frontend | Vue.js + TypeScript + Vite | Eingabeformulare & Visualisierung
Visualisierung | SHAP / Plotly / Chart.js | Erklärbare KI darstellen
Deployment | Docker + docker‑compose | Lokales Setup & reproduzierbare Umgebung
Codequalität | Ruff, Black, ESLint | Linting & Formatter

---

## 3️⃣ Plan for Next Sprint

### Backend Stabilisieren

- Health‑Check Endpoint grün → `/api/v1/utils/health-check` ✅
- User‑Management prüfen → Admin / Normaluser Fixtures ✅
- Dummy Predict‑Route vorbereiten → `/api/v1/predict` (aufgesetzt)

### KI‑Modell Integration

- Modell erhalten → Vorhersage & SHAP‑Explanation implementieren
- Unit‑Tests für Prediction + Explanation

### Feedback

- Feedback‑Tabelle in DB anlegen
- Endpoint `/api/v1/feedback` implementieren

### Frontend (Start)

- Projekt initialisieren (Vite + Vue.js)
- Formulare für Patientendaten + Anzeige Vorhersage + Erklärung

### Tests & Qualität

- Unit/Integration Tests Backend (Health‑Check, Login, Users)
- Linter / Formatter ausführen (Ruff, Black, ESLint)

### Später

- Docker + docker‑compose für Backend + DB + Frontend
- CI/CD Setup