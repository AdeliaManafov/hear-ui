import logging
import os
import pickle
from typing import Any

import numpy as np

try:
    import joblib
except Exception:  # joblib not available at import time
    joblib = None

from .ci_dataset_adapter import CochlearImplantDatasetAdapter
from .model_adapter import DatasetAdapter, ModelAdapter, SklearnModelAdapter
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
    def __init__(
        self,
        model_adapter: ModelAdapter | None = None,
        dataset_adapter: DatasetAdapter | None = None,
    ):
        """Initialize ModelWrapper with optional adapters.

        Args:
            model_adapter: Adapter for model framework (sklearn, PyTorch, etc.)
                          If None, auto-detected when model is loaded
            dataset_adapter: Adapter for dataset preprocessing
                            If None, defaults to CochlearImplantDatasetAdapter
        """
        self.model: Any | None = None
        self.model_adapter: ModelAdapter | None = model_adapter
        self.dataset_adapter: DatasetAdapter = (
            dataset_adapter or CochlearImplantDatasetAdapter()
        )
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

    def _auto_detect_model_adapter(self) -> ModelAdapter:
        """Auto-detect the appropriate model adapter based on model type.

        Returns:
            ModelAdapter instance for the detected framework
        """
        if self.model is None:
            raise RuntimeError("No model loaded")

        # Check for sklearn
        try:
            import sklearn.base

            if isinstance(self.model, sklearn.base.BaseEstimator) or hasattr(
                self.model, "predict"
            ):
                logger.info("Auto-detected sklearn model, using SklearnModelAdapter")
                return SklearnModelAdapter(self.model)
        except ImportError:
            pass

        # Check for PyTorch (placeholder for future)
        # try:
        #     import torch
        #     if isinstance(self.model, torch.nn.Module):
        #         return PyTorchModelAdapter(self.model)
        # except ImportError:
        #     pass

        # Default to sklearn adapter (most permissive)
        logger.warning(
            f"Could not auto-detect model type for {type(self.model).__name__}, "
            "defaulting to SklearnModelAdapter"
        )
        return SklearnModelAdapter(self.model)

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
            except Exception:
                logger.debug("joblib.load failed, will try pickle.load", exc_info=True)
                # Fallback to pickle
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                    logger.info("Loaded model with pickle from %s", MODEL_PATH)
        else:
            # Fallback to pickle
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
                logger.info("Loaded model with pickle from %s", MODEL_PATH)

        # Auto-detect model adapter if not provided
        if self.model_adapter is None:
            self.model_adapter = self._auto_detect_model_adapter()

    def predict(self, raw: dict, clip: bool = True):
        """Return predicted probability for class 1.

        The raw dict is transformed by the dataset adapter before prediction.
        If no model is loaded a RuntimeError is raised so the API route can
        decide on a fallback behaviour.

        Args:
            raw: Patient data dictionary or preprocessed feature array
            clip: If True, clip probabilities to [0.01, 0.99] to avoid overconfidence

        Returns:
            Array of predicted probabilities (clipped if clip=True)
        """
        if self.model is None:
            raise RuntimeError("No model loaded")
        if self.model_adapter is None:
            raise RuntimeError("No model adapter configured")

        # Accept either raw dict-like input or already-preprocessed X (DataFrame/array)
        if isinstance(raw, dict) or hasattr(raw, "get"):
            X = self.prepare_input(raw)
        else:
            X = raw

        # Use model adapter for prediction
        probs = self.model_adapter.predict_proba(X)

        return clip_probabilities(probs) if clip else probs

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

        Uses the dataset adapter to convert raw patient dict to the
        feature array expected by the model.

        Args:
            raw: Raw input dictionary

        Returns:
            Preprocessed feature array
        """
        return self.dataset_adapter.preprocess(raw)

    def get_feature_names(self) -> list[str]:
        """Get the list of feature names expected by the model.

        Returns:
            List of feature names in the correct order
        """
        return self.dataset_adapter.get_feature_names()
