# CI/CD Setup — HEAR Projekt

Diese Seite fasst eine minimal sinnvolle CI/CD‑Konfiguration zusammen (GitHub Actions). Ziel: schnelle, reproduzierbare Checks (Lint + Tests) und optionaler Docker‑Build.

## Empfohlene Workflows

1) `lint-and-test.yml` — bei `push` und `pull_request`
   - Abhängigkeiten installieren
   - Linter (Ruff / Black / ESLint) ausführen
   - `pytest` ausführen

2) `build-and-push.yml` — bei Merge in `main` (optional)
   - Docker‑Image bauen
   - Image in Registry pushen (Docker Hub / GHCR)

## Wichtige CI‑Secrets

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (für Integrationstests)
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` oder `GHCR_TOKEN`
- `PYPI_TOKEN` (falls Veröffentlichung geplant)
- `SECRET_KEY` (nur falls nötig)

## Minimaler Beispiel‑Workflow (`.github/workflows/lint-and-test.yml`)

```yaml
name: Lint and Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: hear_test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres" --health-interval 10s
          --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt || true
      - name: Run linters
        run: |
          pip install ruff black
          ruff backend --fix || true
          black --check backend || true
      - name: Run tests
        run: |
          pip install pytest
          pytest backend -q
```