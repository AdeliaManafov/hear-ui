# frontend/src

Hauptquelle für die Frontend-Anwendung (React + TypeScript).

Wichtige Unterordner:
- `client/` — automatisch generierter OpenAPI-Client.
- `components/` — wiederverwendbare UI-Komponenten.
- `hooks/` — benutzerdefinierte React-Hooks.
- `routes/` — Routendefinitionen / Seiten.

Entwicklung:
- Node Setup: siehe `frontend/README.md` (fnm/nvm, `npm install`).
- Dev-Server: `npm run dev`, öffne `http://localhost:5173`.

Generieren des Clients: `./scripts/generate-client.sh` (Projekt-Root) oder `npm run generate-client` im Frontend nach Herunterladen von `openapi.json`.
