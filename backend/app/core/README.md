# backend/app/core

Core modules and configurations for the backend application.

Contents:
- `config.py` — Application settings (Pydantic Settings)
- `db.py` — Database connection and session management
- `model_wrapper.py` — ML model interface for predictions
- `preprocessor.py` — Feature preprocessing for the ML pipeline
- `shap_explainer.py` — SHAP integration for explainable AI
- `background_data.py` — Synthetic background data generation for SHAP

Changes here can affect the entire app — test changes with unit and integration tests.

See `backend/README.md` for startup and migration steps.
