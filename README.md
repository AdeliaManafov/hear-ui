# HEAR UI - Cochlea-Implantat Entscheidungsunterstützung

**KI-gestützte Webanwendung zur Unterstützung bei Cochlea-Implantat-Entscheidungen**

---

## 🎯 Projektübersicht

### Problemstellung
Für hörgeschädigte Patient:innen stellt sich die Frage, ob ihnen ein Cochlea-Implantat helfen würde. Man möchte unnötige Eingriffe vermeiden, aber gleichzeitig den Patient:innen eine Operation empfehlen, die davon profitieren können.

### Lösung
HEAR nutzt KI, um basierend auf Patientendaten (Alter, Hörverlust-Dauer, Implantat-Typ) eine Erfolgswahrscheinlichkeit zu berechnen und diese durch SHAP-Erklärungen verständlich zu machen.

---

## ✅ Implementierte Features

### Backend (FastAPI)
- ✅ `POST /api/v1/predict/` - Vorhersage mit SHAP-Erklärungen
- ✅ `POST /api/v1/feedback/` - Feedback speichern
- ✅ PostgreSQL-Datenbank mit Alembic Migrations
- ✅ 25 automatisierte Tests (alle bestanden)

### Frontend (Vue.js 3)
- ✅ Eingabeformular für Patientendaten
- ✅ Vorhersage-Anzeige mit Farbcodierung
- ✅ SHAP Feature Importance Visualisierung
- ✅ Feedback-System

### Infrastructure
- ✅ Docker Compose Setup (4 Container)
- ✅ Automatische Datenbank-Initialisierung
- ✅ Health-Checks

---

## 🚀 Quick Start

### Voraussetzungen
- Docker & Docker Compose
- Git

### Installation

```bash
# 1. Repository klonen
git clone <repository-url>
cd hear-ui

# 2. Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeite .env und setze sichere Werte

# 3. Anwendung starten
docker-compose up -d

# 4. Status prüfen
docker-compose ps
```

### Zugriff
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/docs
- **Adminer (DB):** http://localhost:8080

---

## 📡 API Endpoints

### Vorhersage
```bash
curl -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "age": 65,
    "hearing_loss_duration": 5.5,
    "implant_type": "type_a"
  }'
```

**Response:**
```json
{
  "prediction": 0.75,
  "explanation": {
    "age": 0.2,
    "hearing_loss_duration": 0.3,
    "implant_type": 0.15
  }
}
```

### Feedback
```bash
curl -X POST http://localhost:8000/api/v1/feedback/ \
  -H "Content-Type: application/json" \
  -d '{
    "input_features": {"age": 65, "hearing_loss_duration": 5.5, "implant_type": "type_a"},
    "prediction": 0.75,
    "accepted": true,
    "comment": "Stimme zu"
  }'
```

---

## 🧪 Tests

### Backend-Tests ausführen
```bash
cd backend
pytest -v
```

**Ergebnis:** 25/25 Tests bestanden ✅

### Alle Tests in Docker
```bash
docker-compose exec backend pytest
```

---

## 🛠️ Technologie-Stack

**Backend:**
- Python 3.10
- FastAPI
- SQLModel + PostgreSQL
- SHAP (Explainable AI)
- Pytest

**Frontend:**
- Vue.js 3
- TypeScript
- Vite

**Infrastructure:**
- Docker & Docker Compose

---

## 📁 Projektstruktur

```
hear-ui/
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── api/routes/
│   │   │   ├── predict.py    # Vorhersage-Endpoint
│   │   │   └── feedback.py   # Feedback-Endpoint
│   │   ├── models/           # Datenbank-Modelle
│   │   └── tests/            # 25 Tests
│   └── Dockerfile
├── frontend/             # Vue.js Frontend
│   ├── src/components/   # Vue-Komponenten
│   └── Dockerfile
├── docker-compose.yml    # Container-Orchestrierung
└── .env.example          # Umgebungsvariablen
```

---

## 🔧 Entwicklung ohne Docker

### Backend
```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Status

- ✅ **Backend:** Vollständig funktionsfähig
- ✅ **Frontend:** Alle Komponenten implementiert
- ✅ **Datenbank:** PostgreSQL mit Migrations
- ✅ **Tests:** 25/25 bestanden
- ✅ **Docker:** Alle Container laufen stabil

**Projekt-Status:** ✅ **ABGABEBEREIT**

---

## 📚 Weitere Dokumentation

- **API-Dokumentation:** http://localhost:8000/docs (Swagger UI)
- **Projektdokumentation:** `docs/Projektdokumentation.md`

---

## 🔒 Sicherheitshinweise

⚠️ **Vor Deployment:**
```bash
# Sichere Secrets generieren:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Ändere in `.env`:
- `SECRET_KEY`
- `POSTGRES_PASSWORD`
- `FIRST_SUPERUSER_PASSWORD`

---

## 📝 License

MIT License - siehe [LICENSE](./LICENSE)

---

**Erstellt:** November 2025  
**Version:** 1.0.0 (MVP)
