# HEAR-UI

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-394%20passed-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/Coverage-90%25-green.svg)](#testing)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-assisted decision support for estimating Cochlear Implant success and explaining predictions via SHAP.

---

**Quick links**: [Getting Started](#getting-started) • [Usage](#usage) • [Development](#development) • [License](#license)

**Short pitch**: HEAR‑UI predicts the probability that a patient will benefit from a cochlear implant and returns interpretable explanations to support clinical decisions.

## Getting Started

These instructions get you a development environment running locally using Docker Compose (recommended).

3. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Prerequisites

- Docker & Docker Compose
- Git

### Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

**Required variables** (see `.env.example` for all options):

| Variable | Description |
|----------|-------------|
| `POSTGRES_PASSWORD` | Database password (change from default!) |
| `SECRET_KEY` | JWT signing key (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`) |
| `DOCKER_IMAGE_BACKEND` | Backend image name (default: `hear-backend`) |
| `DOCKER_IMAGE_FRONTEND` | Frontend image name (default: `hear-frontend`) |

> ⚠️ **Security**: Never commit `.env` with real secrets. The `.env.example` contains placeholder values only.

### Clone and start services

```bash
git clone <repo-url>
cd hear-ui
cp .env.example .env
# Edit .env with secure values!
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.override.yml \
  --env-file "$PWD/.env" up -d --build

# health check
curl http://localhost:8000/api/v1/utils/health-check/
```

Open the API docs at http://localhost:8000/docs

If you prefer a quick demo (uses local scripts):

```bash
./demo.sh
```

## Usage

Minimal example — prediction

```bash
curl -sS -X POST http://localhost:8000/api/v1/predict/ \
  -H "Content-Type: application/json" \
  -d '{"Alter [J]": 45, "Geschlecht": "w", "Primäre Sprache": "Deutsch"}'
```

Example — SHAP explanation

```bash
curl -sS -X POST http://localhost:8000/api/v1/explainer/explain \
  -H "Content-Type: application/json" \
  -d '{"age":45, "gender":"w", "implant_type":"Cochlear"}'
```

See `/docs` for full request/response schema and additional endpoints (feedback, patients, etc.).

## Development

Run backend tests (inside Docker container):

```bash
docker compose -f docker/docker-compose.yml exec backend python -m pytest -v
```

Run linter:

```bash
docker compose -f docker/docker-compose.yml exec backend python -m ruff check app/
```

Useful scripts are under `backend/scripts/` (e.g. `test_all_patients.py`).

## Architecture & Files

- `backend/app/` — FastAPI app, routes, core logic
- `backend/app/core/` — model wrapper, preprocessing, explainer
- `backend/app/models/` — trained model and background sample
- `frontend/` — Vue.js app (in progress)
- `docker/` — docker-compose and container config

## Project Structure

```
hear-ui/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core logic (ML model, SHAP)
│   │   ├── models/      # Database models
│   │   └── tests/       # Backend tests
│   └── requirements.txt
├── frontend/            # Vue.js frontend
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── routes/      # Route definitions
│   │   └── client/      # API client
│   └── tests/          # Frontend tests
├── docker/             # Docker configuration
└── docs/               # Additional documentation

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

## Maintainers

- Adelia Manafov
- Artem Mozharov
- Niels Kuhl

---
