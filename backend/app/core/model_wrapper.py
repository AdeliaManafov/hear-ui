import os
import logging
import pickle
from typing import Any, Optional

try:
    import joblib
except Exception:  # joblib not available at import time
    joblib = None

from .preprocessor import preprocess_patient_data

logger = logging.getLogger(__name__)

# Path to the model file. Prefer a pipeline (joblib) if available.
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    # Prefer the exported pipeline (includes preprocessing + estimator).
    os.path.join(os.path.dirname(__file__), "../models/logreg_best_pipeline.pkl"),
)


class ModelWrapper:
    def __init__(self):
        self.model: Optional[Any] = None
        # retain path for diagnostics
        self.model_path = MODEL_PATH
        # Attempt to load at construction but do NOT raise — keep app import-safe.
        try:
            self.load_model()
        except Exception as e:
            logger.exception("Model load failed during ModelWrapper init: %s", e)
            self.model = None

    # Compatibility wrapper: older code expects `load()` and `is_loaded()`
    def load(self) -> None:
        return self.load_model()

    def is_loaded(self) -> bool:
        return self.model is not None

    def load_model(self) -> None:
        """Try to load the model using joblib (preferred) then pickle as fallback.

        This method raises exceptions to the caller; the constructor catches them
        and leaves `self.model` as None so the application can continue to start.
        """
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

        # Prefer joblib if available and the file looks like a joblib dump
        if joblib is not None:
            try:
                self.model = joblib.load(MODEL_PATH)
                logger.info("Loaded model with joblib from %s", MODEL_PATH)
                return
            except Exception:
                logger.debug("joblib.load failed, will try pickle.load", exc_info=True)

        # Fallback to pickle
        with open(MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)
            logger.info("Loaded model with pickle from %s", MODEL_PATH)

    def predict(self, raw: dict):
        """Return predicted probability for class 1.

        The raw dict is transformed by the preprocessor before prediction. If no
        model is loaded a RuntimeError is raised so the API route can decide on
        a fallback behaviour.
        """
        if self.model is None:
            raise RuntimeError("No model loaded")

        # Accept either raw dict-like input or already-preprocessed X (DataFrame/array)
        if isinstance(raw, dict) or hasattr(raw, "get"):
            X = self.prepare_input(raw)
        else:
            X = raw
        # Most sklearn estimators provide `predict_proba`; fall back to `decision_function`.
        try:
            # If the pipeline/estimator supports probabilities, use them.
            if hasattr(self.model, "predict_proba"):
                return self.model.predict_proba(X)[:, 1]

            # Some estimators expose a decision function we can map to (0,1).
            if hasattr(self.model, "decision_function"):
                # Map decision_function output to probability-like score via sigmoid
                import numpy as _np

                scores = self.model.decision_function(X)
                probs = 1 / (1 + _np.exp(-scores))
                return probs

            # Determine final estimator (for Pipeline objects)
            final_estimator = getattr(self.model, "steps", None)
            if final_estimator:
                final_estimator = self.model.steps[-1][1]
            else:
                final_estimator = self.model

            # If the final estimator is a regressor, return its continuous prediction.
            try:
                from sklearn.base import is_regressor

                if is_regressor(final_estimator):
                    preds = self.model.predict(X)
                    # Ensure float array output
                    import numpy as _np

                    return _np.asarray(preds, dtype=float)
            except Exception:
                # sklearn may not be available in the static analysis environment;
                # fall back to attempting to call predict and return numeric values.
                try:
                    preds = self.model.predict(X)
                    import numpy as _np

                    return _np.asarray(preds, dtype=float)
                except Exception:
                    pass

            # Last resort for classifiers without predict_proba: map predict() to 0/1
            preds = self.model.predict(X)
            import numpy as _np

            return (_np.asarray(preds) == 1).astype(float)
        except ValueError as ve:
            # Common sklearn error when the feature vector length doesn't match.
            # Provide a more actionable error message for users integrating the model.
            expected = getattr(self.model, "n_features_in_", None)
            actual = None
            try:
                # X may be a DataFrame or numpy array
                actual = X.shape[1]
            except Exception:
                try:
                    actual = len(X[0]) if hasattr(X, "__iter__") and len(X) > 0 else None
                except Exception:
                    actual = None

            hint_parts = []
            if expected is not None and actual is not None:
                hint_parts.append(f"model expects {expected} features but got {actual}")
            elif expected is not None:
                hint_parts.append(f"model expects {expected} features")
            elif actual is not None:
                hint_parts.append(f"input has {actual} features")

            hint = ", ".join(hint_parts) if hint_parts else "feature shape mismatch"
            guidance = (
                "Provide a scikit-learn `Pipeline` that includes preprocessing and the estimator, "
                "saved with `joblib.dump(pipeline, 'logreg_best_pipeline.pkl')`, then set the `MODEL_PATH` "
                f"environment variable or place the file at {MODEL_PATH}. Alternatively, update `preprocess_patient_data` "
                "so it produces the full feature vector the model expects."
            )
            raise ValueError(f"Model input mismatch: {hint}. {guidance}") from ve

    def prepare_input(self, raw: dict):
        """Prepare a single-row input suitable for the loaded model.

        Attempts to construct a pandas.DataFrame matching `model.feature_names_in_`
        when available. Falls back to the legacy `preprocess_patient_data`.
        """
        # If model exposes feature names, build a DataFrame with those columns
        fnames = getattr(self.model, "feature_names_in_", None)
        if fnames is not None:
            try:
                import pandas as _pd

                row = {}
                for fname in fnames:
                    low = fname.lower()
                    if "alter" in low or "age" in low:
                        row[fname] = raw.get("age")
                    elif "höranamnese" in low or "beginn" in low or "dauer" in low or "hearing" in low:
                        row[fname] = raw.get("hearing_loss_duration")
                    elif "implant" in low or "ci implantation" in low or "behandlung" in low:
                        row[fname] = raw.get("implant_type")
                    elif "geschlecht" in low or "gender" in low:
                        row[fname] = raw.get("gender")
                    elif "sprache" in low:
                        row[fname] = raw.get("primary_language")
                    elif "tinnitus" in low:
                        row[fname] = raw.get("tinnitus")
                    elif "ursache" in low or "cause" in low:
                        row[fname] = raw.get("cause")
                    else:
                        row[fname] = raw.get(fname)

                return _pd.DataFrame([row])
            except Exception:
                return preprocess_patient_data(raw)

        # No feature names available: fall back to legacy preprocessor
        return preprocess_patient_data(raw)

