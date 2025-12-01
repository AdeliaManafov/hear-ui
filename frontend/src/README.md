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

Generieren des Clients: `./scripts/generate-client.sh` (Projekt-Root) oder `npm run generate-client` im Frontend nach
Herunterladen von `openapi.json`.

## TODOs
| File                                     | TODO                               |
|------------------------------------------|------------------------------------|
| `frontend/src/routes/PatientDetails.vue` | upload the form                    |
| `frontend/src/routes/PatientDetails.vue` | add action for change and delete   |
| `frontend/src/routes/PatientDetails.vue` | implement an API call for that     |
| `frontend/src/routes/SearchPatients.vue` | add API call for the names and IDs |
| `frontend/src/routes/SearchPatients.vue` | Implement bouncing                 |
| `frontend/src/routes/Prediction.vue`     | add an API call for the prediction |
| `frontend/src/routes/Prediction.vue`     | add a feedback form                |

