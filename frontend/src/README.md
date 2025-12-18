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
| File                                     | TODO                                                              |
|------------------------------------------|-------------------------------------------------------------------|
| `frontend/src/routes/PatientDetails.vue` | Delete patient                                                    |
| `frontend/src/routes/PatientDetails.vue` | Update patient                                                    |
| `frontend/src/routes/CreatePatient.vue`  | Change alerts to popups so the user understands what has happened |
| `frontend/src/routes/Prediction.vue`     | Add Feedback                                                      |
