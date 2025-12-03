# HEAR Backend - FastAPI

> Backend API for Cochlear Implant success prediction with ML model and SHAP explanations.

For general project information see the root README: `../README.md`

---

## 🚀 Quick Start Commands

```bash
# Navigate to project root
cd hear-ui

# Start all services (backend, database, adminer)
docker compose up -d --build

# Stop all services
docker compose down

# View backend logs
docker compose logs --follow --tail 200 backend

# Health check
curl -v http://localhost:8000/api/v1/utils/health-check/

# Run database migrations
docker compose exec backend alembic upgrade head

# Access PostgreSQL directly
PGPASSWORD=change_me psql -h localhost -p 5433 -U postgres -d app

# Import CSV data into database
docker cp mydata.csv hear-ui-db-1:/tmp/mydata.csv
docker exec -it hear-ui-db-1 psql -U postgres -d app -c "\copy patients FROM '/tmp/mydata.csv' WITH (FORMAT csv, HEADER true)"
```

---

## 📍 Available Services

| Service | URL | Description |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **API Docs (Swagger)** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/api/v1/utils/health-check/ | Service status |
| **Adminer (DB GUI)** | http://localhost:8080 | Database administration |
| **PostgreSQL** | localhost:5433 | Direct database access |

---

## 🔧 Requirements

* [Docker](https://www.docker.com/) and Docker Compose
* [uv](https://docs.astral.sh/uv/) for Python package and environment management (optional, for local dev)

---

## 🐳 Docker Compose Setup

### Start Services

```bash
cd hear-ui
docker compose up -d --build

# Verify containers are running
docker compose ps
# Expected: backend, db (postgres), adminer are "Up"
```

### View Logs

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs --follow --tail 200 backend

# Frontend only
docker compose logs --tail 200 frontend
```

### Stop Services

```bash
docker compose down

# Stop and remove volumes (reset database)
docker compose down -v
```

---

## 🧪 Running Tests

```bash
# Run all tests
docker compose exec backend python -m pytest -v

# Run with coverage
docker compose exec backend python -m pytest --cov=app --cov-report=html

# Run specific test file
docker compose exec backend python -m pytest app/tests/test_shap_explainer.py -v

# Quick test script
bash ./scripts/test.sh
```

**Current Test Status:**
- ✅ 164 tests passing
- ⏭️ 2 tests skipped
- 📊 82% code coverage

---

## 🗄️ Database Access

### Using Adminer (Web GUI)

1. Open http://localhost:8080
2. Fill in the form:
   - **System:** PostgreSQL
   - **Server:** db
   - **Username:** postgres
   - **Password:** change_me (or from `.env`)
   - **Database:** app

### Using psql (Command Line)

```bash
# From host machine
PGPASSWORD=change_me psql -h localhost -p 5433 -U postgres -d app

# From inside container
docker compose exec db psql -U postgres -d app

# List all tables
docker compose exec db psql -U postgres -d app -c "SELECT tablename FROM pg_tables WHERE schemaname='public';"

# Check migration status
docker compose exec db psql -U postgres -d app -c "SELECT * FROM alembic_version;"
```

---

## 🔄 Database Migrations (Alembic)

```bash
# Run migrations (inside container)
docker compose exec backend alembic upgrade head

# Create new migration after model changes
docker compose exec backend alembic revision --autogenerate -m "Add new field"

# Check current migration version
docker compose exec backend alembic current

# Rollback one migration
docker compose exec backend alembic downgrade -1
```

---

## 📡 API Endpoints

### Quick API Tests

```bash
# Health check
curl -sS http://localhost:8000/api/v1/utils/health-check/ | jq

# Model info
curl -sS http://localhost:8000/api/v1/utils/model-info/ | jq

# List patients
curl -sS http://localhost:8000/api/v1/patients/ | jq

# Single prediction
curl -sS -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{"Alter [J]": 45, "Geschlecht": "w", "Primäre Sprache": "Deutsch"}' | jq

# Get patient prediction
curl -sS http://localhost:8000/api/v1/patients/{patient_id}/predict | jq

# Get SHAP explanation for patient
curl -sS http://localhost:8000/api/v1/patients/{patient_id}/explainer | jq

# Create feedback
curl -sS -X POST http://localhost:8000/api/v1/feedback/ \
  -H "Content-Type: application/json" \
  -d '{"input_features": {"age": 55}, "prediction": 0.85, "accepted": true}' | jq
```

---

## 🛠️ Local Development (without Docker)

### Setup Virtual Environment

```bash
cd backend

# Install dependencies with uv
uv sync

# Activate virtual environment
source .venv/bin/activate

# Or use pip
pip install -r requirements.txt
```

### Run Development Server

```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using FastAPI CLI
fastapi dev app/main.py
```

### VS Code Integration

The project includes VS Code configurations for:
- Running the backend with debugger (breakpoints supported)
- Running tests through the Python test panel

Make sure your editor uses the correct Python interpreter: `backend/.venv/bin/python`

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/           # API endpoints
│   │   │   ├── predict.py    # Prediction endpoint
│   │   │   ├── patients.py   # Patient CRUD + predict/explainer
│   │   │   ├── explainer.py  # SHAP explanations
│   │   │   ├── feedback.py   # Feedback endpoint
│   │   │   └── utils.py      # Health check, model info
│   │   └── deps.py           # Dependency injection
│   ├── core/
│   │   ├── config.py         # Application settings
│   │   ├── db.py             # Database connection
│   │   ├── model_wrapper.py  # ML model interface
│   │   ├── preprocessor.py   # Feature preprocessing
│   │   ├── shap_explainer.py # SHAP integration
│   │   └── background_data.py # Synthetic data for SHAP
│   ├── models/
│   │   ├── logreg_best_model.pkl  # Trained ML model
│   │   ├── patient_record.py      # Patient SQLModel
│   │   ├── prediction.py          # Prediction SQLModel
│   │   └── feedback.py            # Feedback SQLModel
│   ├── tests/                # Test suite (164 tests)
│   └── alembic/              # Database migrations
├── scripts/                  # Utility scripts
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container build
└── alembic.ini              # Alembic configuration
```

---

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| `Model not loaded` | Check if `logreg_best_model.pkl` exists in `app/models/` |
| `Database connection failed` | Ensure PostgreSQL container is running: `docker compose ps` |
| `Migration failed` | Run `docker compose exec backend alembic upgrade head` |
| `Port already in use` | Stop other services or change ports in `docker-compose.yml` |
| `SHAP ImportError` | Install dependencies: `pip install shap numpy` |

### View Detailed Logs

```bash
# Backend logs with timestamps
docker compose logs -f --timestamps backend

# Check container status
docker compose ps

# Restart backend only
docker compose restart backend
```

---

## 📧 Email Templates (MVP Note)

Email functionality is archived for MVP. Templates are in `archiviert/backend_email_templates/`.

To re-enable:
1. Restore templates to `backend/app/email-templates/`
2. Configure SMTP in `.env`

---

## 🔐 Model Configuration & Deployment

For production deployments, model configuration, and best practices:

**👉 See [MODEL_DEPLOYMENT.md](MODEL_DEPLOYMENT.md) for:**
- `MODEL_PATH` environment variable configuration
- Model versioning and updates
- SHAP background data configuration
- Pipeline best practices
- Performance optimization
- Security considerations
- Monitoring and troubleshooting

---

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [API Docs](http://localhost:8000/docs) - Swagger UI
- [Projektdokumentation](../docs/Projektdokumentation.md) - Full technical docs
- [MODEL_DEPLOYMENT.md](MODEL_DEPLOYMENT.md) - Model configuration & deployment guide
- [README-DEPS.md](README-DEPS.md) - Dependency management
