from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional


MODEL_PATH_DEFAULT = os.getenv("MODEL_PATH", "app/models/logreg_best_model.pkl")


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
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        # Try pickle then joblib
        try:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception:
            try:
                import joblib

                self.model = joblib.load(self.model_path)
            except Exception as exc:  # pragma: no cover - hard to reproduce here
                raise RuntimeError(f"Failed to load model: {exc!r}")

    def is_loaded(self) -> bool:
        return self.model is not None

    def predict(self, features: List[float]) -> Dict[str, Any]:
        """Return a dict with `prediction` (probability for positive class) and `class`.

        The caller must pass a flat list representing a single sample (1D list).
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")

        import numpy as np

        X = np.array([features])
        # Prefer predict_proba if available
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X)[0]
            # assume binary classification and positive class at index 1
            prob_pos = float(probs[1]) if len(probs) > 1 else float(probs[0])
            pred_class = int(self.model.predict(X)[0]) if hasattr(self.model, "predict") else (1 if prob_pos >= 0.5 else 0)
            return {"prediction": prob_pos, "class": pred_class, "probs": probs.tolist()}

        # fallback: use predict only
        pred_class = int(self.model.predict(X)[0])
        return {"prediction": float(pred_class), "class": pred_class, "probs": [float(pred_class)]}

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
