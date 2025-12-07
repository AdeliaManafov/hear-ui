# frontend/src

Hauptquelle für die Frontend-Anwendung (React + TypeScript).

Development
- See the project-level `frontend/README.md` for Node version manager recommendations (fnm/nvm) and detailed setup instructions.
- From the `frontend` directory:
	- Install dependencies: `npm install` (or `pnpm install` depending on the repository setup).
	- Start dev server: `npm run dev` and open `http://localhost:5173`.

Generate / update API client
- When the backend OpenAPI schema changes, regenerate the client to keep types and API calls in sync.
	- From project root: `./scripts/generate-client.sh`
	- Or from `frontend`: `npm run generate-client` (if configured).
	- Ensure the latest `openapi.json` is available to the generator before running the script.

Other useful commands
- Build production bundle: `npm run build`.
- Run unit tests: `npm run test`.
- Lint and format: `npm run lint` / `npm run format` (if available).

Notes
- The `client/` folder is generated code — avoid manual edits. Put app-specific wrappers or helpers outside of the generated files.
- Keep routes and components small and well-documented; add Storybook stories for shared UI where it helps collaboration and QA.


## TODOs
| File                                     | TODO                                                                                   |
|------------------------------------------|----------------------------------------------------------------------------------------|
| `frontend/src/routes/PatientDetails.vue` | Render patient detail form (prefill with fetched patient data; allow read-only vs edit modes). |
| `frontend/src/routes/PatientDetails.vue` | Implement “Edit patient” flow (reuse create form prefilled; save via backend update API when available). |
| `frontend/src/routes/PatientDetails.vue` | Implement “Delete patient” action (confirm dialog, call backend delete once exposed).  |
| `frontend/src/routes/Prediction.vue`     | Wire prediction API call (use patient_id params; show loading/error states).           |
| `frontend/src/routes/Prediction.vue`     | Add feedback form after prediction (capture acceptance/comment; POST to backend).      |
