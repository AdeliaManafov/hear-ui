# HEAR-UI

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-183%20passed-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/Coverage-83%25-green.svg)](#testing)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI-assisted decision support for estimating Cochlear Implant success and explaining predictions via SHAP.

---

**Quick links**: [Getting Started](#getting-started) • [Usage](#usage) • [Development](#development) • [Contributing](#contributing) • [License](#license)

**Short pitch**: HEAR‑UI predicts the probability that a patient will benefit from a cochlear implant and returns interpretable explanations to support clinical decisions.

## Getting Started

These instructions get you a development environment running locally using Docker Compose (recommended).

Prerequisites

- Docker & Docker Compose
- Git

Clone and start services

```bash
git clone <repo-url>
cd hear-ui
cp .env.example .env
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

## Contributing

We welcome contributions. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for the development workflow, coding standards, and PR checklist.

Quick process:

1. Fork the repo
2. Create a topic branch: `git checkout -b feature/your-feature`
3. Add tests and run the test suite
4. Open a pull request with a clear description

## Security

If you discover a security vulnerability, please report it privately to the maintainers (open an issue marked `security` or email the project owner) instead of creating a public issue.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

## Maintainers

- Adelia Manafov
- Artem Mozharov
- Niels Kuhl

---
