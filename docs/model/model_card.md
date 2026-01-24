Model Card — HEAR CI Prediction Model

Version: v1 (draft)
Last updated: 2025-12-30

1. Model Overview

This document summarizes the ML model used in the HEAR project. The model is a Logistic Regression model (scikit-learn) trained to predict post‑operative outcome for cochlear implant patients. It expects 68 features (see Preprocessing) and outputs a probability for the positive class (success metric used by the project).

2. Intended Use

- Purpose: Support clinicians by estimating the probability of a positive outcome after cochlear implantation.
- Intended users: Clinicians and decision support integrators in hospital settings.
- Not intended for: Autonomous clinical decisions without human oversight, use outside validated populations, or legal/administrative decisions.

3. Model Details

- Model type: LogisticRegression (scikit-learn). Saved artifact: `backend/app/models/logreg_best_model.pkl` (or configured via `MODEL_PATH`).
- Input: 68‑feature vector following `backend/app/core/preprocessor.py::EXPECTED_FEATURES` ordering. The preprocessor accepts German aliases and several shorthand keys.
- Output: Probability in [0,1] for positive outcome.

4. Preprocessing

- See `backend/app/core/preprocessor.py` for exact preprocessing logic, feature ordering and alias mapping.
- The preprocessor returns a pandas DataFrame with columns in the same order as `EXPECTED_FEATURES`.
- Important: Do not change the order of `EXPECTED_FEATURES` without updating dependent code and tests.

5. Training Data

- Training data: not included in this repository. Example and sample patients for integration tests reside in `data/sample_patients.csv`.
- If training artifacts are available, link them here (dataset name, timeframe, preprocessing steps). If not available, document that reproduction requires access to original training dataset.

6. Evaluation Metrics

- Reported metrics: see evaluation scripts / logs if present in `scripts/training` or `model/` (add paths when available).
- If metrics files are not present, list steps to recreate: train with the provided pipeline, evaluate on held-out test set, compute AUC, accuracy, calibration plots.

7. Explainability

- SHAP: The backend provides SHAP‑based explanations via `backend/app/core/shap_explainer.py`. The server falls back to a coefficient‑based explanation when SHAP is not available or fails.
- Background dataset: SHAP explanations depend on a background dataset. The project currently uses a small synthetic/background sample (see `backend/app/core/background_data.py` / `data/sample_patients.csv`). For reproducible results, store a versioned background file and reference it here.

8. Limitations & Bias

- Performance and attributions depend on the background dataset used for SHAP and on preprocessing defaults.
- Some categorical encodings and default values are chosen in the preprocessing script; these can bias results when missing values are common.
- Behaviour outside the population represented in the training data is not validated here.

9. Recommendations

- Use only as support tool
- Human medical judgment has priority
- Regular evaluation is recommended

10. Reproducibility

To reproduce predictions and explanations locally:

- Clone repository and install dependencies (see `backend/pyproject.toml` / `requirements.txt`).
- Place the trained model at the path configured by `MODEL_PATH` or set `MODEL_PATH` environment variable.
- Start the backend: `cd backend; uvicorn app.main:app --reload --port 8000`.
- Example predict and explain requests: see `docs/api-examples/`.

Required artifacts for full reproducibility:
- Model artifact (pickle/joblib) and exact training script
- Training dataset or a description of it
- Preprocessing code (present in `backend/app/core/preprocessor.py`)
- Background dataset used for SHAP (versioned)
- Random seeds and environment (python package versions in `requirements.txt`)

11. Contact & License

- Repository: local repo (hear-ui)
- License: see `LICENSE` at repository root.
- Contact: maintainers listed in repository metadata (add email/contact here if available).

Notes

This model card is a living document. When more artifacts (training data, evaluation logs, background dataset) become available they should be linked here and the Model Card updated.
