# Testing Guide

## Schnellstart

**Einfachste Lösung - nur Unit-Tests (keine externen Services):**
```bash
cd backend
./scripts/run_unit_tests.sh
```
→ Läuft ~178 Unit-Tests, kein Docker/DB/Server nötig

**Vollständige Tests (inkl. Integration mit Testcontainers):**
```bash
cd backend
./scripts/run_all_tests.sh
```
→ Installiert Testcontainers, startet Postgres-Container, läuft alle Tests

---

## Test-Kategorien

Das Backend hat 3 Arten von Tests:

### 1. **Unit-Tests** (Standard)
Tests mit In-Memory SQLite, gemockten Dependencies:
```bash
pytest -m "not integration and not e2e" -v --cov=app
```
Ergebnis: ~178 Tests (schnell, keine externen Services)

### 2. **Integration-Tests** (brauchen Postgres)
Tests mit echter Datenbank-Verbindung:
```bash
# Mit Testcontainers (empfohlen):
pip install "testcontainers[postgres]"
pytest --cov=app

# Oder nur Integration-Tests:
pytest -m integration
```

### 3. **E2E-Tests** (brauchen laufenden Server)
Tests gegen localhost:8000:
```bash
# Server in einem Terminal starten:
uvicorn app.main:app --port 8000

# In anderem Terminal:
pytest -m e2e
```

## Vollständige Test-Suite

```bash
# 1. Starte Services
docker-compose up -d

# 2. Warte auf Backend
sleep 5

# 3. Alle Tests
pytest

# 4. Mit Coverage
pytest --cov=app --cov-report=term-missing --cov-report=html
```

## CI/CD

`.github/workflows/test-backend.yml` und `backend-tests.yml` laufen mit:
- Postgres 15 Service ✅
- Unit-Tests ✅
- Integration-Tests ✅
- **Ohne** E2E (kein laufender Server in CI) ❌

```yaml
pytest -m "not e2e" -v --cov=app
```

Resultat: ~194 Tests (178 Unit + 16 Integration)

### Umgang mit Port-Konflikten beim Starten von Docker

Der lokale `docker-compose.override.yml` mappt den Postgres-Container auf einen Host-Port.
Wenn der Port bereits vom Host oder einem anderen Container belegt ist, schlägt `docker compose up` fehl
("Bind for 0.0.0.0:5433 failed: port is already allocated").

Lösungsmöglichkeiten:

- Schnell (stoppe den Conflicting Container):
    ```bash
    # Liste laufende Container und beende den, der Port 5433 nutzt
    docker ps
    docker stop <container-id>
    ```

- Sofort (ohne Stoppen): starte Compose mit einem anderen Host-Port:
    ```bash
    # Setze Host-Port z.B. 5434
    POSTGRES_HOST_PORT=5434 docker compose up -d
    ```

- Persistente Option: die `docker-compose.override.yml` erlaubt jetzt eine Umgebungsvariable
    `POSTGRES_HOST_PORT`. Standard ist `5434`. Du kannst `.env` oder die Shell-Umgebung setzen.

Beispiel mit `.env` (im `hear-ui`-Root):
```
POSTGRES_HOST_PORT=5434
```

Dann:
```bash
docker compose up -d
```

Diese Änderung verhindert Port-Konflikte für die meisten lokalen Entwicklungs-Setups.

## Hilfs-Skripte

### `run_unit_tests.sh` - Schnelle Unit-Tests
Läuft nur Unit-Tests (keine DB, kein Server):
```bash
cd backend
chmod +x scripts/run_unit_tests.sh
./scripts/run_unit_tests.sh
```

### `run_all_tests.sh` - Vollständige Test-Suite
Installiert Testcontainers, prüft Docker, läuft alle Tests:
```bash
cd backend
chmod +x scripts/run_all_tests.sh
./scripts/run_all_tests.sh
```

Beide Skripte erzeugen HTML-Coverage-Reports in `backend/htmlcov/index.html`.

## Test-Marker

Definiert in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "integration: requires real database",
    "e2e: requires running server",
]
```

## Empfohlene Workflows

**Lokale Entwicklung (schnell):**
```bash
pytest app/api/tests/ -v
```

**Vor Commit:**
```bash
pytest -m "not e2e" --cov=app
```

**Vollständiger Test:**
```bash
docker-compose up -d && pytest --cov=app
```
