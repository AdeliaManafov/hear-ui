# HEAR Backend

> FastAPI backend for Cochlear Implant success prediction with ML model and SHAP explanations.

For general project information, see the main [README](../README.md).

---

## Overview

The backend provides a REST API for:
- **ML predictions:** Probability of successful cochlear implant outcomes (0-100%)
- **SHAP explanations:** Feature importance analysis for transparency
- **Feedback management:** Store and retrieve clinical feedback
- **Patient data:** CRUD operations for patient records

---

## Architecture

```
Backend (FastAPI)
 app/
    api/routes/          # REST endpoints (predict, explainer, feedback, patients)
    core/                # Business logic (model_wrapper, shap_explainer)
    models/              # Database models + trained ML model (.pkl)
    db/                  # Database session and utilities
    tests/               # Test suite (pytest)
 alembic/                 # Database migrations
```

---

## Tech Stack

- **Framework:** FastAPI 0.115+
- **Database:** PostgreSQL 12 + SQLModel ORM
- **ML:** scikit-learn (LogisticRegression pipeline, 68 features)
- **Explainability:** SHAP (coefficient-based feature importance)
- **Migrations:** Alembic
- **Testing:** pytest (165 tests, 83% coverage)
- **Code Quality:** Ruff (linter), mypy (type checking)

---

## Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)

### Quick Start

```bash
# From project root
cd hear-ui

# Start all services
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.override.yml \
  --env-file "$PWD/.env" up -d

# Verify backend is running
curl http://localhost:8000/api/v1/utils/health-check/
# Expected: {"status":"ok"}

# View logs
docker compose -f docker/docker-compose.yml logs -f backend
```

### Local Development (without Docker)

```bash
cd backend

# Install dependencies (using uv or pip)
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://postgres:password@localhost:5434/app
export MODEL_PATH=app/models/logreg_best_pipeline.pkl

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Apply migrations
docker compose -f docker/docker-compose.yml exec backend alembic upgrade head

# Create new migration
docker compose -f docker/docker-compose.yml exec backend alembic revision --autogenerate -m "Description"

# Rollback
docker compose -f docker/docker-compose.yml exec backend alembic downgrade -1
```

### Access Database

```bash
# Via psql (from host)
PGPASSWORD=your_password psql -h localhost -p 5434 -U postgres -d app

# Via pgAdmin (web UI)
# Open: http://localhost:5051
# Login: admin@example.com / admin
# Add server: Host=db, Port=5432, User=postgres, Password from .env
```

---

## Testing

### Run All Tests

```bash
# Inside container
docker compose -f docker/docker-compose.yml exec backend python -m pytest app/tests/ -v

# With coverage
docker compose -f docker/docker-compose.yml exec backend python -m pytest app/tests/ --cov=app --cov-report=html

# Specific test file
docker compose -f docker/docker-compose.yml exec backend python -m pytest app/tests/test_predict.py -v

# Quick test script
bash ./scripts/test.sh
```

### Test Categories

| Category | Tests | Coverage |
|----------|-------|----------|
| Health Checks | 5 | Core functionality |
| ML Model Integration | 15 | Predictions |
| SHAP Explainer | 12 | Feature importance |
| API Endpoints | 25 | REST API |
| Database CRUD | 20 | Persistence |
| Security | 10 | Password hashing |
| Integration | 78 | End-to-end |

**Total:** 165 tests, 83% code coverage

### CI/CD

GitHub Actions workflows:
- `ci.yml` - Combined pipeline (lint → test → e2e)
- `backend-tests.yml` - Backend tests with coverage
- `playwright.yml` - E2E API tests

---

## API

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/utils/health-check/` | GET | Health status |
| `/api/v1/predict/` | POST | ML prediction |
| `/api/v1/explainer/explain` | POST | SHAP explanation |
| `/api/v1/feedback/` | GET/POST | Feedback management |
| `/api/v1/patients/` | GET | List patients (paginated) |
| `/api/v1/patients/{id}` | GET/PUT/DELETE | Patient CRUD |
| `/docs` | GET | Swagger UI |
| `/redoc` | GET | ReDoc documentation |

**Interactive documentation:** http://localhost:8000/docs

### Example Requests

```bash
# Health check
curl http://localhost:8000/api/v1/utils/health-check/

# Prediction
curl -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{"Alter [J]": 45, "Geschlecht": "w", ...}'

# SHAP explanation
curl -X POST http://localhost:8000/api/v1/explainer/explain \
  -H "Content-Type: application/json" \
  -d '{"age": 45, "gender": "w", ...}'
```

See [main README](../README.md) for full examples.

---

## Contributing

### Code Standards

- **Style:** PEP 8, enforced by Ruff
- **Type hints:** Required for all functions
- **Tests:** Write tests for new features (aim for 80%+ coverage)
- **Documentation:** Update API docs and docstrings

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and add tests
3. Run linter: `ruff check app/`
4. Run tests: `pytest app/tests/`
5. Commit: `git commit -m "feat: add feature"`
6. Push and open PR

### Linting & Formatting

```bash
# Check code
docker compose -f docker/docker-compose.yml exec backend ruff check app/

# Auto-fix issues
docker compose -f docker/docker-compose.yml exec backend ruff check app/ --fix

# Type checking
docker compose -f docker/docker-compose.yml exec backend mypy app/
```

---

## License

MIT License - see [LICENSE](../LICENSE)

---

## Further Documentation

- [Main README](../README.md) - Complete project documentation
- [Testing Guide](README-TESTING.md) - Detailed test documentation
- [Dependencies](README-DEPS.md) - Package management
- [Model Deployment](MODEL_DEPLOYMENT.md) - Model configuration & deployment guide
- [Project Documentation](../docs/Projektdokumentation.md) - Full technical docs (German)
- [Production Readiness](../docs/PRODUCTION_READINESS.md) - Deployment checklist

