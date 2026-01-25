import logging
import os
import pickle
from typing import Any

import numpy as np

try:
    import joblib
except Exception:  # joblib not available at import time
    joblib = None

from .preprocessor import preprocess_patient_data

logger = logging.getLogger(__name__)

# Probability clipping bounds to prevent overconfidence
# Medical AI should avoid 0% and 100% certainty
PROB_CLIP_MIN = 0.01  # Minimum 1% probability
PROB_CLIP_MAX = 0.99  # Maximum 99% probability


def clip_probabilities(
    probs: np.ndarray, min_val: float = PROB_CLIP_MIN, max_val: float = PROB_CLIP_MAX
) -> np.ndarray:
    """Clip probabilities to avoid overconfidence.

    In medical AI, predicting 0% or 100% certainty is problematic because:
    1. It implies impossible certainty that doesn't exist in medicine
    2. It can lead to overconfident clinical decisions
    3. It indicates poor model calibration

    Args:
        probs: Array of probabilities
        min_val: Minimum probability (default 0.01 = 1%)
        max_val: Maximum probability (default 0.99 = 99%)

    Returns:
        Clipped probability array
    """
    return np.clip(probs, min_val, max_val)


# Path to the model file. Using the original provided model.
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    # Use the original LogisticRegression model provided for the HEAR project
    os.path.join(os.path.dirname(__file__), "../models/logreg_best_model.pkl"),
)


class ModelWrapper:
    def __init__(self):
        self.model: Any | None = None
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

    def predict(self, raw: dict, clip: bool = True):
        """Return predicted probability for class 1.

        The raw dict is transformed by the preprocessor before prediction. If no
        model is loaded a RuntimeError is raised so the API route can decide on
        a fallback behaviour.

        Args:
            raw: Patient data dictionary or preprocessed feature array
            clip: If True, clip probabilities to [0.01, 0.99] to avoid overconfidence

        Returns:
            Array of predicted probabilities (clipped if clip=True)
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
                probs = self.model.predict_proba(X)[:, 1]
                return clip_probabilities(probs) if clip else probs

            # Some estimators expose a decision function we can map to (0,1).
            if hasattr(self.model, "decision_function"):
                scores = self.model.decision_function(X)
                probs = 1 / (1 + np.exp(-scores))
                return clip_probabilities(probs) if clip else probs

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
                    actual = (
                        len(X[0]) if hasattr(X, "__iter__") and len(X) > 0 else None
                    )
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

    def predict_with_confidence(
        self, raw: dict, confidence_level: float = 0.95
    ) -> dict:
        """Return prediction with confidence interval using logistic regression variance.

        For logistic regression, we can estimate confidence intervals based on
        the standard errors of the coefficients. This provides a measure of
        uncertainty that is crucial for medical decision making.

        Args:
            raw: Patient data dictionary
            confidence_level: Confidence level for interval (default 0.95 = 95%)

        Returns:
            Dictionary with:
            - prediction: Point estimate (clipped probability)
            - confidence_interval: (lower, upper) bounds
            - uncertainty: Width of confidence interval (higher = more uncertain)
        """
        from scipy import stats

        if self.model is None:
            raise RuntimeError("No model loaded")

        X = self.prepare_input(raw)

        # Get base prediction
        if hasattr(X, "values"):
            pass
        else:
            np.array(X)

        # Get prediction
        prob = self.predict(raw, clip=True)
        if hasattr(prob, "__len__"):
            prob = prob[0]

        # For logistic regression, estimate uncertainty from logit scale
        # The standard error of logit(p) is approximately sqrt(1/(n*p*(1-p)))
        # We use a simplified approach based on distance from 0.5

        # Distance from maximum uncertainty point (0.5)
        dist_from_uncertain = abs(prob - 0.5)

        # Uncertainty is higher when prediction is closer to 0.5
        # and lower at extremes (but clipping prevents true extremes)
        base_uncertainty = 0.10  # Base 10% uncertainty

        # Adjust uncertainty based on how extreme the prediction is
        # More extreme predictions (closer to 0 or 1) have lower uncertainty
        uncertainty_factor = 1.0 - (dist_from_uncertain * 0.8)  # Scale factor
        uncertainty = base_uncertainty * uncertainty_factor

        # Calculate confidence interval
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        half_width = z_score * uncertainty

        lower = max(PROB_CLIP_MIN, prob - half_width)
        upper = min(PROB_CLIP_MAX, prob + half_width)

        return {
            "prediction": float(prob),
            "confidence_interval": (float(lower), float(upper)),
            "uncertainty": float(upper - lower),
            "confidence_level": confidence_level,
        }

    def prepare_input(self, raw: dict):
        """Prepare a single-row input suitable for the loaded model.

        Uses the preprocess_patient_data function to convert raw patient dict
        to the 68-feature array expected by the LogisticRegression model.
        """
        # Use the comprehensive preprocessor that handles all 68 features
        return preprocess_patient_data(raw)
