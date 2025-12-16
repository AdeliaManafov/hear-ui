# Lokales CI-Testing (ohne git push)

Es gibt 3 Wege, CI lokal zu testen ohne zu pushen:

## Option 1: Mit `act` (GitHub Actions lokal ausführen)

`act` simuliert GitHub Actions runner auf deinem Mac.

### Installation
```bash
brew install act
```

### Nutzung
```bash
# Alle workflows ausführen
act

# Nur einen Job ausführen
act -j test-backend

# Spezifischen Workflow ausführen
act -W .github/workflows/backend-tests.yml

# Mit bestimmtem Event
act push

# Secrets übergeben (wenn nötig)
act -s GITHUB_TOKEN=xyz

# Verbose logs
act -v
```

**Vorteile:** Exakte CI-Simulation  
**Nachteile:** Benötigt Docker, kann langsam sein

---

## Option 2: Docker Compose (schnell & einfach)

Starte Services und führe Tests manuell aus.

### Backend Tests
```bash
# Services starten
docker compose up -d db

# In backend container ausführen oder lokal:
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# DB vorbereiten
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/hear_db"
alembic upgrade heads

# Tests ausführen
pytest -v --cov=app --cov-report=html --cov-fail-under=80

# Services stoppen
docker compose down
```

### E2E Tests
```bash
# Backend + DB starten
docker compose up -d db backend

# Warten bis bereit
for i in {1..30}; do
  curl -sf http://localhost:8000/api/v1/utils/health-check/ && break
  sleep 2
done

# Frontend tests
cd frontend
pnpm install
pnpm exec playwright install --with-deps chromium
pnpm exec playwright test --project=api

# Cleanup
docker compose down
```

---

## Option 3: Dev Container (dein Setup!)

Du hast `.devcontainer/` konfiguriert – VS Code nutzt das automatisch!

### So nutzt du es:
1. Öffne VS Code
2. Cmd+Shift+P → "Dev Containers: Reopen in Container"
3. VS Code startet Backend-Container mit allen Tools
4. Im Container-Terminal:
   ```bash
   # Tests direkt ausführen
   cd /app
   pytest -v --cov=app
   
   # oder mit Script
   ./scripts/test.sh
   ```

**Vorteile:** Exakt wie CI, schnell, persistiert  
**Nachteile:** Nur Backend (nicht E2E ohne extra Setup)

---

## Empfehlung für dich

**Für schnelle Backend-Tests:**
```bash
# Option 2 – einfach und schnell
docker compose up -d db
cd backend
source .venv/bin/activate  # oder erstelle neu
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/hear_db"
alembic upgrade heads
pytest -v --cov=app --cov-report=term-missing
```

**Für vollständige CI-Simulation vor Push:**
```bash
# Option 1 – act
act -j test-backend  # nur Backend
act -j e2e-tests     # nur E2E
```

**Für dev work:**
```bash
# Option 3 – Dev Container in VS Code
# Öffne einfach den Ordner in VS Code und klicke "Reopen in Container"
```

---

## Schnelltest-Kommandos

Füge diese zu deinem `~/.zshrc` hinzu:
```bash
# Backend tests lokal
alias test-backend="cd backend && pytest -v --maxfail=1"

# CI lokal simulieren
alias test-ci="act -j test-backend"

# Health check
alias check-backend="curl -s http://localhost:8000/api/v1/utils/health-check/ | jq"
```

Dann kannst du einfach `test-backend` oder `test-ci` im Terminal eingeben!
