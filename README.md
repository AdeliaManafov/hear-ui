# HEAR-UI - Cochlear Implant Success Prediction

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-183%20passed-brightgreen.svg)](#-testing-strategy)
[![Coverage](https://img.shields.io/badge/Coverage-83%25-green.svg)](#-testing-strategy)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> AI-powered decision support system for predicting Cochlear Implant success rates with explainable AI (SHAP).

---

##  What is HEAR-UI?

**HEAR-UI** (Hearing Enhancement AI Research) helps medical professionals make informed decisions about cochlear implant procedures by:

- **Predicting success probability** based on patient characteristics
- **Explaining predictions** using SHAP (SHapley Additive exPlanations)
- **Providing clinical insights** through feature importance analysis

### The Problem

Determining whether a hearing-impaired patient will benefit from a cochlear implant is complex. While the procedure can significantly improve hearing, it requires:

- Surgical intervention with associated risks
- Post-operative rehabilitation (relearning to hear)
- Time and financial investment

Medical professionals need data-driven insights to recommend the procedure only to patients who are likely to benefit.

### The Solution

HEAR-UI provides:

1. **Probability predictions** (0-100%) of successful implant outcomes
2. **Transparent explanations** showing which patient factors influence the prediction
3. **Clinical decision support** through an easy-to-use REST API

---

##  Quick Start

### Option 1: Interactive Demo (Recommended)

```bash
cd hear-ui
./demo.sh
```

This demonstrates:
 
Demo Script
`demo.sh` runs an end-to-end sequence (health check → prediction → SHAP → feedback).

### Option 2: Docker Compose

**Note:** Docker Compose files are located in the [`docker/`](docker/) directory. All commands must be run from the project root.

```bash
# Start all services (from project root)
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.override.yml \
  --env-file "$PWD/.env" up -d

# Verify backend is running
curl http://localhost:8000/api/v1/utils/health-check/
# Expected: {"status":"ok"}

# View logs
docker compose -f docker/docker-compose.yml logs -f backend

# Stop services
docker compose -f docker/docker-compose.yml down

# View API documentation
open http://localhost:8000/docs
```

**Available Services:**

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| **Backend API** | http://localhost:8000 | 8000 | FastAPI REST API |
| **API Docs (Swagger)** | http://localhost:8000/docs | 8000 | Interactive API documentation |
| **Frontend (Vite)** | http://localhost:5173 | 5173 | Vue.js development server |
| **pgAdmin** | http://localhost:5051 | 5051 | PostgreSQL admin interface |
| **PostgreSQL (Container)** | `db:5432` (internal) | 5432 (internal) | Database access from containers |
| **PostgreSQL (Host)** | `localhost:5434` | 5434 | Direct database access from host |

**Connection Details:**
- **pgAdmin Login:** `admin@example.com` / `admin` (from [docker/docker-compose.override.yml](docker/docker-compose.override.yml))
- **Database:** Host=`db` Port=`5432` (from containers) or Host=`localhost` Port=`5434` (from host)
- **Database Credentials:** Username=`postgres`, Password from `.env` (`POSTGRES_PASSWORD`)

---

## Documentation

- **Project documentation (German):** [docs/Projektdokumentation.md](docs/Projektdokumentation.md)
- **Project history & decisions:** [docs/PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md)
- **Literature & references:** [docs/REFERENCES.md](docs/REFERENCES.md)
- **Validation & presentation checklist:** [VALIDATION_REPORT.md](VALIDATION_REPORT.md)


## MVP Scope

### Included

- Backend KI-Predictions
- SHAP explanations
- REST API
- CSV test data
- Docker + Database
- Tests

### Not Included

- Full frontend UI
- CSV upload UI

---

##  How to Use

### 1. Make a Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "Alter [J]": 45,
    "Geschlecht": "w",
    "Primäre Sprache": "Deutsch",
    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
    "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
    "Symptome präoperativ.Tinnitus...": "ja",
    "Behandlung/OP.CI Implantation": "Cochlear"
  }'
```

**Response:**

```json
{
  "prediction": 0.9734,
  "explanation": {}
}
```

**Interpretation:** 97.34% probability of successful outcome.

### 2. Get SHAP Explanation

```bash
curl -X POST http://localhost:8000/api/v1/explainer/explain \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "gender": "w",
    "primary_language": "Deutsch",
    "hearing_loss_onset": "postlingual",
    "hearing_loss_duration": 5.0,
    "hearing_loss_cause": "Unknown",
    "tinnitus": "ja",
    "vertigo": "nein",
    "implant_type": "Cochlear"
  }'
```

**Response:**

```json
{
  "prediction": 0.9734,
  "feature_importance": {
    "postlingual": 0.173,
    "Alter [J]": -0.031,
    "..."
  },
  "top_features": [
    {"feature": "Diagnose...postlingual", "importance": 0.173, "value": "postlingual"},
    {"feature": "Alter [J]", "importance": -0.031, "value": 45}
  ],
  "base_value": 0.80
}
```

**Interpretation:**

- Postlingual hearing loss increases success probability by 17.3%
- Patient age slightly decreases it by 3.1%

### 3. Submit Feedback

```bash
curl -X POST http://localhost:8000/api/v1/feedback/ \
  -H "Content-Type: application/json" \
  -d '{
    "input_features": {"Alter [J]": 45},
    "prediction": 0.9734,
    "accepted": true,
    "comment": "Patient proceeded with surgery"
  }'
```

### 4. Batch Processing

Test multiple patients from a CSV file:

```bash
python3 backend/scripts/test_all_patients.py
```

### API Endpoints Overview

| Endpoint | Method | Description | Example |
|----------|--------|-------------|--------|
| `/api/v1/utils/health-check/` | GET | Backend health status | `curl http://localhost:8000/api/v1/utils/health-check/` |
| `/api/v1/predict/` | POST | ML prediction (0-100%) | See example in "Make a Prediction" |
| `/api/v1/explainer/explain` | POST | SHAP explanation | See example in "Get SHAP Explanation" |
| `/api/v1/feedback/` | POST | Submit feedback | See example in "Submit Feedback" |
| `/api/v1/feedback/` | GET | List feedback | `curl http://localhost:8000/api/v1/feedback/` |
| `/api/v1/patients/` | GET | List patients (paginated) | `curl http://localhost:8000/api/v1/patients/` |
| `/api/v1/patients/{id}` | GET | Get patient by ID | `curl http://localhost:8000/api/v1/patients/{uuid}` |
| `/docs` | GET | Interactive API docs (Swagger) | `open http://localhost:8000/docs` |

**Full API documentation:** http://localhost:8000/docs (interactive Swagger UI)

---

##  Architecture

### System Overview

```text
      REST API       
   Frontend   HTTP    Backend    
  (Vue.js)                          (FastAPI)   
                     
                                           
                       
                                                         
                               
                     ML               SHAP        Database 
                    Model           Explainer    (Postgres)
                               
```

### Directory Structure

```text
hear-ui/
 backend/
    app/
       api/
          routes/          # API endpoints (predict, shap, feedback)
       core/                # Core business logic
          model_wrapper.py     # ML model interface
          shap_explainer.py    # SHAP integration
          background_data.py   # Background sample generator
       models/              # Database models & trained ML models
          logreg_best_pipeline.pkl  # Main ML model (RandomForest)
          background_sample.csv     # SHAP background data (100 patients)
       tests/               # Test suite (36 tests)
    scripts/                 # Utility scripts
        calibrate_model.py       # Model calibration
        test_all_patients.py     # Batch testing
        generate_background_data.py
 frontend/                    # Vue.js frontend (in progress)
 docs/                        # Documentation
    Projektdokumentation.md      # Full project documentation (German)
    PRODUCTION_READINESS.md      # Production deployment checklist
    SHAP_INTEGRATION.md          # SHAP technical details
 data/                        # Test & training data
 .env.example                 # Environment variables template
 docker-compose.yml           # Container orchestration
 demo.sh                      # Interactive demo script
 README.md                    # This file
```

### Tech Stack

**Backend:**

- **Framework:** FastAPI (async, auto-docs)
- **ML:** scikit-learn (RandomForest, Pipeline)
- **Explainability:** SHAP (TreeExplainer)
- **Database:** PostgreSQL + SQLModel ORM
- **Migrations:** Alembic

**Frontend:**

- **Framework:** Vue.js 3 + TypeScript
- **Build:** Vite
- **UI Library:** Vuetify (Vue Material Design Components)
- **Testing:** Vitest + Playwright

**DevOps:**

- **Containers:** Docker + Docker Compose
- **Linting:** Ruff (Python), ESLint (JS/TS)
- **Testing:** Pytest (Backend), Vitest (Frontend)

---

##  Development

### Prerequisites

- **Docker Desktop** (recommended) or Docker + Docker Compose
- **Python 3.10+** (for local development)
- **Node.js 18+** (for frontend development)
- **Git**

### Setup for Development

#### 1. Clone Repository

```bash
git clone <repository-url>
cd hear-ui
```

#### 2. Environment Configuration

```bash
# Create environment file
cp .env.example .env

# Edit with your settings
nano .env
```

**Required variables:**

```env
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/app
```

**Optional variables:**

```env
MODEL_PATH=backend/app/models/logreg_best_pipeline.pkl
SHAP_BACKGROUND_FILE=backend/app/models/background_sample.csv
```

#### 3. Start Development Environment

```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d

# View logs
docker compose -f docker/docker-compose.yml logs -f backend

# Stop services
docker compose -f docker/docker-compose.yml down
```

#### 4. Run Database Migrations

```bash
docker compose -f docker/docker-compose.yml exec backend alembic upgrade head
```

### Running Tests

#### Backend Tests

```bash
# All tests (inside container)
docker compose -f docker/docker-compose.yml exec backend python -m pytest app/tests/ -v

# Specific test file
docker compose -f docker/docker-compose.yml exec backend python -m pytest app/tests/test_shap_explainer.py -v

# With coverage
docker compose -f docker/docker-compose.yml exec backend python -m pytest app/tests/ --cov=app --cov-report=html
```

#### Integration Tests with Real Data

```bash
# Test with 28 real patients from CSV
python3 backend/scripts/test_all_patients.py

# Test API endpoints
python3 backend/scripts/test_api.py
```

#### Code Quality

```bash
# Run linter
docker compose -f docker/docker-compose.yml exec backend python -m ruff check app/

# Auto-fix linting issues
docker compose -f docker/docker-compose.yml exec backend python -m ruff check app/ --fix

# Type checking (if mypy is configured)
docker compose -f docker/docker-compose.yml exec backend python -m mypy app/
```

### Adding New Features

#### 1. Backend API Endpoint

```python
# backend/app/api/routes/your_route.py
from fastapi import APIRouter

router = APIRouter(prefix="/your-endpoint", tags=["your-tag"])

@router.get("/")
def get_data():
    return {"data": "example"}
```

#### 2. Database Model

```python
# backend/app/models/your_model.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

class YourModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
```

Run migration:

```bash
docker compose -f docker/docker-compose.yml exec backend alembic revision --autogenerate -m "Add your_model"
docker compose -f docker/docker-compose.yml exec backend alembic upgrade head
```

#### 3. Unit Test

```python
# backend/app/tests/test_your_feature.py
def test_your_endpoint(client):
    response = client.get("/api/v1/your-endpoint/")
    assert response.status_code == 200
```

### Useful Commands

```bash
# Access running backend container
docker compose -f docker/docker-compose.yml exec backend bash

# Access PostgreSQL
docker compose -f docker/docker-compose.yml exec db psql -U postgres -d app

# View database with Adminer
open http://localhost:8080
# Server: db, Username: postgres, Password: [from .env], Database: app

# Rebuild containers
docker compose -f docker/docker-compose.yml build

# Reset database
docker compose -f docker/docker-compose.yml down -v
docker compose -f docker/docker-compose.yml up -d
```

---

##  Testing Strategy

### Test Coverage

```text
 183 tests passing (100%)
   - Backend (pytest): 165 tests
   - E2E API (Playwright): 18 tests
 83% code coverage
```

### CI/CD Pipeline

```text
          
  Linting     Backend Tests  E2E Tests  
  (Ruff)             (pytest)         (Playwright)
          
                                                
                                                
                                        
                                          CI Summary 
                                        
```

**GitHub Actions Workflows:**

- `ci.yml` - Combined CI pipeline (lint → test → e2e)
- `backend-tests.yml` - Backend tests with coverage
- `playwright.yml` - E2E API tests

**Test Categories:**

| Category | Tests | Coverage |
|----------|-------|----------|
| Health Checks | 5 |  Core |
| Model Integration | 15 |  ML Pipeline |
| SHAP Explainer | 12 |  Explanations |
| API Endpoints | 25 |  REST API |
| Database CRUD | 20 |  Persistence |
| Security | 10 |  Password Hashing |
| Integration | 80+ |  End-to-end |
| E2E (Playwright) | 18 |  API Workflows |

### Test Real Patient Data

Real-world validation with 5 patients from `Dummy Data_Cochlear Implant.csv`:

```bash
python3 backend/scripts/test_all_patients.py
```

**Results:**

-  5/5 patients processed successfully
-  Predictions range: 22.1% - 100.0%
-  Realistic distribution based on patient risk factors

---

##  Model Details

### LogisticRegression Model

**Architecture:**

1. **Preprocessor** (Custom preprocessing)
   - Numeric features: StandardScaler
   - Categorical features: OneHotEncoder (68 features after encoding)
2. **Classifier:** LogisticRegression (L1 penalty, C=10)

**Input Features (7 main categories):**

- Alter [J] (Age in years)
- Geschlecht (Gender)
- Primäre Sprache (Primary language)
- Diagnose...Beginn der Hörminderung (Hearing loss onset)
- Diagnose...Ursache (Cause of hearing loss)
- Symptome präoperativ.Tinnitus (Tinnitus symptoms)
- Behandlung/OP.CI Implantation (Implant type)

**Transformed Features:** 68 (after one-hot encoding)

### Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Prediction Range** | 22-100% | Realistic clinical range |
| **Model Type** | LogisticRegression | Binary classification with probability |
| **Feature Count** | 68 | After one-hot encoding |

### SHAP Explainability

- **Method:** Coefficient-based feature importance
- **Background Data:** Synthetic samples for stable explanations
- **Purpose:** Explain which patient factors influence predictions

**Top Predictive Features:**

1. **Hearing Loss Onset** (postlingual vs. prelingual) - High impact
2. **Duration of Deafness** - Longer duration = lower success probability
3. **Cause of Hearing Loss** (syndromal vs. other) - Significant impact
4. **Age** - Moderate impact
5. **Implant Type** - Minor impact

---

##  Deployment

### Production Readiness Checklist

** Ready:**

- [x] Backend API fully functional
- [x] ML model tested (28/28 real patients)
- [x] SHAP explanations working
- [x] Database schema migrated
- [x] Docker containers optimized
- [x] API documentation (Swagger)
- [x] Comprehensive test suite
- [x] Demo script for validation

**⏳ In Progress:**

- [ ] Frontend UI (Vue.js components)
- [ ] User authentication (JWT)
- [ ] Rate limiting
- [ ] Production logging (structured)
- [ ] Monitoring (Prometheus/Grafana)
- [x] CI/CD pipeline (GitHub Actions)
- [ ] TLS/HTTPS configuration

### Docker Production Deployment

```bash
# Build production images
docker compose -f docker/docker-compose.yml build

# Start in production mode
docker compose -f docker/docker-compose.yml up -d

# Verify deployment
curl https://your-domain.com/api/v1/utils/health-check/

# View logs
docker compose -f docker/docker-compose.yml logs --tail=100 -f backend
```

### Health Monitoring

```bash
# Backend health
curl http://localhost:8000/api/v1/utils/health-check/

# Database health
docker compose -f docker/docker-compose.yml exec backend python -c "from app.core.database import engine; engine.connect()"

# Model status
curl http://localhost:8000/api/v1/utils/model-info/
```

---

##  Further Documentation

| Document | Purpose |
|----------|---------|
| [Projektdokumentation.md](docs/Projektdokumentation.md) | Complete technical documentation (German) |
| [PROJECT_HISTORY.md](docs/PROJECT_HISTORY.md) | **Project management history, milestones, decisions, timeline** |
| [REFERENCES.md](docs/REFERENCES.md) | **Complete literature references & citations (scientific papers, frameworks)** |
| [VALIDATION_REPORT.md](VALIDATION_REPORT.md) | Validation report & presentation checklist |
| [PRODUCTION_READINESS.md](docs/PRODUCTION_READINESS.md) | Production deployment guide & checklist |
| [SHAP_INTEGRATION.md](docs/SHAP_INTEGRATION.md) | SHAP technical implementation details |
| [MODEL_CALIBRATION.md](docs/MODEL_CALIBRATION.md) | Model calibration guide & evaluation |
| [API Docs (Swagger)](http://localhost:8000/docs) | Interactive API documentation |

---

##  Contributing

Contributions are welcome! Please follow these guidelines:

### Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Standards

- **Python:** Follow PEP 8, use Ruff for linting
- **TypeScript:** Use ESLint with project config
- **Tests:** Write tests for new features (aim for 80%+ coverage)
- **Documentation:** Update README and relevant docs

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

##  Authors & Acknowledgments

**Authors:**

- Adelia Manafov
- Artem Mozharov

**Acknowledgments:**

- scikit-learn team - ML implementation
- SHAP library - Explainable AI
- FastAPI - Modern Python web framework
- Docker - Containerization

---

##  Support & Contact

**For Issues:**

-  Report bugs via [GitHub Issues](https://github.com/your-repo/issues)
-  Check documentation in `/docs` folder
-  Ask questions in [Discussions](https://github.com/your-repo/discussions)

**For Collaboration:**

-  Email: <your-email@example.com>
-  LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

##  Project Status & Roadmap

**Current Version:** 1.0.0 (Backend MVP)  
**Status:**  Production-Ready (Backend)  
**Last Updated:** November 30, 2025

Current focus: Backend complete with ML model integration. Frontend implementation is in progress.

### Version History

**v1.0.0 (Current)** - November 2025

-  REST API backend with FastAPI
-  LogisticRegression model integration (68 features)
-  SHAP explanations for explainable AI
-  PostgreSQL persistence with 33 patients
-  Comprehensive test suite (183 tests, 83% coverage)
-  Docker containerization
-  Pydantic V2 migration completed
-  FastAPI lifespan events (no deprecation warnings)
-  CI/CD Pipeline (GitHub Actions)
-  E2E Tests (Playwright - 18 API tests)
-  Pagination for /patients/ endpoint
-  persist=true error handling

**v1.1 (Planned)** - Q1 2026

- Frontend UI (Vue.js/React)
- User authentication
- Batch CSV upload UI
- SHAP visualizations
- PDF report generation

**v2.0 (Future)** - Q2-Q3 2026

- Multi-language support
- Real-time model updates
- Clinical trial integration
- Mobile application

---
