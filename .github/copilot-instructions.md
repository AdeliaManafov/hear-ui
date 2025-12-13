# Copilot / AI Agent Instructions — hear-ui

Short, actionable guidance to make AI coding agents productive in this repository.

## Big picture
- Backend: FastAPI service in `backend/app` exposing `/api/v1/*` routes. Core responsibilities: model loading (`app/core/model_wrapper.py`), preprocessing (`app/core/preprocessor.py`) and SHAP / explanation logic (`app/core/shap_explainer.py`). Entrypoint: `backend/app/main.py`.
- Frontend: Vite-based SPA in `frontend/` (package.json shows a Vue app). Development server: `npm run dev` in `frontend/`.
- Orchestration: `docker-compose.yml` runs `backend`, `db` (Postgres), `frontend`, and `pgadmin` (dev). Use `docker compose up -d --build` to bring up a dev environment.
- Dev environment: Colima recommended on macOS (optimized config in `docs/COLIMA_SETUP.md`).

## Key integration points you must know
- Model instance: `backend/app/main.py` exposes the canonical wrapper on `app.state.model_wrapper`. Prefer that instance for predictions/explanations to avoid mismatches.
  - Example: `from app.main import app as fastapi_app; wrapper = fastapi_app.state.model_wrapper`.
- Beware of local wrapper instances: some route modules instantiate `ModelWrapper()` locally (e.g. `backend/app/api/routes/predict.py` has `model_wrapper = ModelWrapper()` at top). That can cause different model/preprocessor state and different numeric outputs.
- Prediction vs explainer differences:
  - `predict` endpoints call `ModelWrapper.predict()` which wraps preprocessing + model inference.
  - `explainer` (`explainer.py`) builds a preprocessed sample via `wrapper.prepare_input(...)` and computes contributions using model coefficients (coef * value). This is an approximate, coefficient-based explanation — not necessarily identical to a full SHAP run.
  - If you see different numbers for the same patient (e.g. 0.88 vs 0.94), check whether the same `ModelWrapper` instance and same preprocessing path were used (app.state vs local instance). Also check whether the explainer uses transformed features and whether contributions are summed differently.

## Concrete file pointers (patterns & examples)
- Use these files as canonical examples and references:
  - `backend/app/main.py` — app lifecycle, CORS, `app.state.model_wrapper` (preferred wrapper)
  - `backend/app/core/model_wrapper.py` — how the model is loaded and how `predict()` / `prepare_input()` behave
  - `backend/app/core/preprocessor.py` — `EXPECTED_FEATURES` and transformation pipeline (order matters)
  - `backend/app/api/routes/predict.py` — batch & single prediction handling (note local `ModelWrapper()` usage)
  - `backend/app/api/routes/explainer.py` — SHAP-like explanation (coef * value fallback)
  - `backend/app/api/routes/patients.py` — patient CRUD and patient-based `predict`/`explainer` endpoints (uses `app.state.model_wrapper`)

## Developer workflows and commands (copyable)
- Start full stack (recommended local dev):
  ```bash
  cd hear-ui
  docker compose up -d --build
  ```
- Backend logs and debug:
  ```bash
  docker compose logs --follow --tail 200 backend
  docker compose exec backend python -m pytest -v
  docker compose exec backend alembic upgrade head
  ```
- Local backend (no Docker):
  ```bash
  cd backend
  # install deps (project uses `uv` optionally) or pip
  uv sync   # if using uv
  source .venv/bin/activate
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```
- Frontend dev server:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

## Project-specific conventions and gotchas
- Column naming: data and endpoints frequently expect German column names (e.g. `Alter [J]`, `Geschlecht`). Pydantic models use `alias` and many routes call `model_dump(by_alias=True)` or `model_dump(by_alias=True, exclude={...})` — preserve alias usage when calling wrapper functions.
- Flexible input: Routes accept multiple keys for the same concept (e.g., `age`, `alter`, `Alter [J]`). Use `wrapper.prepare_input()` to normalize before inference.
- Persistence is optional: Single-prediction endpoints accept `persist` flags and will attempt DB writes. When updating endpoints, keep persistence failure non-fatal (current code logs and returns prediction).
- Tests and coverage: Backend has a large test suite (`backend/app/tests/`); prefer running tests inside the backend container to match environment.
- Frontend README mismatch: the `frontend/README.md` references React in places but `frontend/package.json` declares `vue` — follow `package.json` and `src/` contents.
- Patient CRUD: Use `PUT /patients/{id}` for updates (partial updates supported) and `DELETE /patients/{id}` for deletion (hard delete). See `docs/API_PATIENT_UPDATE_DELETE.md`.

## When you see different predictions for the same patient
1. **Check for different default values in Pydantic models:** The most common cause of prediction differences is that different endpoints use different Pydantic models with different defaults (e.g., `PatientData` vs `ShapVisualizationRequest`). These defaults are silently added to the input dict and dramatically change predictions. Example: `behandlung_ci="Cochlear"` vs `implant_type="unknown"` produces different feature encodings.
2. Confirm both endpoints used the same wrapper instance: prefer `app.state.model_wrapper`.
3. Confirm both pass identically preprocessed input: compare `wrapper.prepare_input(input)` outputs and the full input dicts (including defaults).
4. Check whether the explainer uses coefficient-based contributions vs. model probability. Coefficient sums (explainer) can differ from raw model predict-proba outputs depending on link functions and postprocessing.
5. If a route instantiates `ModelWrapper()` locally, replace it with the canonical `app.state.model_wrapper` to ensure identical model and preprocessor state.

**Best practice:** Avoid adding defaults to Pydantic request models for ML predictions. Let the frontend provide all values explicitly or document shared defaults in a central config file that both frontend and backend use.

## Useful quick checks (examples you can run)
- Inspect model load status from a running container:
  ```bash
  docker compose exec backend python - <<'PY'
  from app.main import app
  w = app.state.model_wrapper
  print('loaded=', w.is_loaded())
  print('model=', getattr(w, 'model', None))
  PY
  ```
- Compare preprocessed vectors for a sample input:
  ```bash
  docker compose exec backend python - <<'PY'
  from app.main import app
  w = app.state.model_wrapper
  s = {'Alter [J]':45,'Geschlecht':'w','Primäre Sprache':'Deutsch'}
  print(w.prepare_input(s))
  PY
  ```

## What not to change lightly
- Do not change feature ordering in `EXPECTED_FEATURES` (preprocessor) without updating all places that iterate/features rely on that ordering (explainer and tests).
- Avoid introducing new top-level `ModelWrapper()` singletons in route modules — always use `app.state.model_wrapper` or pass wrapper via dependency injection.

If anything here is unclear or you'd like me to emphasize a particular area (for example: packaging, CI, or the SHAP pipeline), tell me which part and I'll iterate.
