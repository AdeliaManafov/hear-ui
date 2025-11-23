from __future__ import annotations

import os
import pickle
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


MODEL_PATH_DEFAULT = os.getenv("MODEL_PATH")
if not MODEL_PATH_DEFAULT:
    # prefer a full pipeline if present, otherwise fall back to the estimator
    # Prioritize the specific model requested by user
    if os.path.exists("backend/app/models/logreg_best_model.pkl") or os.path.exists("app/models/logreg_best_model.pkl"):
        MODEL_PATH_DEFAULT = "app/models/logreg_best_model.pkl"
    else:
        MODEL_PATH_DEFAULT = "app/models/logreg_best_pipeline.pkl"

logger = logging.getLogger(__name__)


class ModelWrapper:
    """Simple wrapper to load a pickled sklearn model (or pipeline) once and
    provide a tiny predict API for the application.

    Notes:
    - The model is expected to implement `predict` and preferably `predict_proba`.
    - If a preprocessing `Pipeline` was saved together with the estimator, it will be used automatically.
    - This wrapper intentionally keeps feature-preparation outside of it: the caller
      must provide the numeric feature vector in the same order used during training.
    """

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model_path = Path(model_path or MODEL_PATH_DEFAULT)
        self.model: Any | None = None

    def load(self) -> None:
        if not self.model_path.exists():
            # log and raise so startup logs show why model was not loaded
            logger.warning("Model file not found at %s", self.model_path)
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        # Try pickle then joblib
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
            logger.info("Loaded model via pickle from %s", self.model_path)
        except Exception:
            try:
                import joblib

                self.model = joblib.load(self.model_path)
                logger.info("Loaded model via joblib from %s", self.model_path)
            except Exception as exc:  # pragma: no cover - hard to reproduce here
                logger.exception("Failed to load model from %s: %s", self.model_path, exc)
                raise RuntimeError(f"Failed to load model: {exc!r}")
        else:
            logger.info("Model loaded successfully from %s", self.model_path)

    def is_loaded(self) -> bool:
        return self.model is not None

    def predict(self, sample: Any) -> Dict[str, Any]:
        """Predict on a single sample.

        `sample` may be:
          - a list/sequence of numeric features (1D) matching model input
          - a dict mapping feature name -> value (will be converted to a single-row DataFrame)
          - a pandas.DataFrame with a single row

        The method tries to call `predict_proba` if available, otherwise falls back to `predict`.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")

        # Lazy import to avoid heavy dependencies until needed
        import numpy as _np

        # If user passed a mapping (raw features), convert to DataFrame if pipeline expects names
        try:
            import pandas as _pd
        except Exception:  # pandas may not be installed in minimal envs
            _pd = None

        X = None
        # list-like input
        if isinstance(sample, (list, tuple, _np.ndarray)):
            X = _np.array([sample])
        elif isinstance(sample, dict):
            if _pd is None:
                # cannot convert to DataFrame without pandas; attempt numpy array from values
                vals = list(sample.values())
                X = _np.array([vals])
            else:
                X = _pd.DataFrame([sample])
        elif _pd is not None and isinstance(sample, _pd.DataFrame):
            X = sample
        else:
            # unsupported sample type
            raise ValueError("Unsupported sample type for prediction")

        # Try direct predict_proba / predict on the loaded model. For pipelines that accept DataFrame this will work.
        try:
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(X)
                # select first sample
                probs0 = probs[0]
                prob_pos = float(probs0[1]) if len(probs0) > 1 else float(probs0[0])
                pred_class = int(self.model.predict(X)[0]) if hasattr(self.model, "predict") else (1 if prob_pos >= 0.5 else 0)
                return {"prediction": prob_pos, "class": pred_class, "probs": list(map(float, probs0))}
            else:
                pred_class = int(self.model.predict(X)[0])
                return {"prediction": float(pred_class), "class": pred_class, "probs": [float(pred_class)]}
        except Exception as exc:  # pragma: no cover - runtime dependent
            # surface a helpful error for the caller to decide; do not swallow silently
            raise RuntimeError(f"Model prediction failed: {exc!r}")

    def get_coef(self) -> Optional[List[float]]:
        """Return coefficient list if model exposes `coef_` (e.g. linear models).

        Used as a cheap explanation fallback when SHAP isn't available.
        """
        if self.model is None:
            return None
        coef = getattr(self.model, "coef_", None)
        if coef is None:
            return None
        # coef may be 2D (n_classes, n_features) or 1D
        import numpy as np

        arr = np.array(coef)
        if arr.ndim == 2:
            # return the coefficient vector for the positive class if present
            if arr.shape[0] == 2:
                arr = arr[1]
            else:
                arr = arr[0]
        return [float(x) for x in arr]
