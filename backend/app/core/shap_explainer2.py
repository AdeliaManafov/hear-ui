from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class ShapExplainer:
    """
    Lightweight SHAP wrapper for explainable predictions.

    Supports:
    - sklearn pipelines
    - linear models (LogisticRegression etc.)
    - tree models
    - JSON-serializable output
    """

    def __init__(
            self,
            model: Any,
            feature_names: Optional[List[str]] = None,
            background_data: Optional[np.ndarray] = None,
    ):
        self.model = model
        self.feature_names = feature_names
        self.background_data = background_data
        self.explainer = None

        try:
            import shap
            self.shap = shap
        except ImportError:
            logger.warning("SHAP is not installed.")
            self.shap = None
            return

        self._init_explainer()

    def _init_explainer(self):
        """Initialize appropriate SHAP explainer."""
        if self.shap is None:
            return

        # fallback background
        if self.background_data is None:
            n_features = self._get_n_features()
            self.background_data = np.zeros((1, n_features))

        model = self.model

        try:
            # Tree models
            if hasattr(model, "feature_importances_"):
                self.explainer = self.shap.TreeExplainer(model, self.background_data)
                logger.info("Using TreeExplainer")
                return

            # Linear models
            if hasattr(model, "coef_"):
                self.explainer = self.shap.LinearExplainer(model, self.background_data)
                logger.info("Using LinearExplainer")
                return

            # Generic fallback
            self.explainer = self.shap.Explainer(model, self.background_data)
            logger.info("Using generic shap.Explainer")

        except Exception as e:
            logger.exception("Failed to initialize SHAP explainer: %s", e)
            self.explainer = None

    def _get_n_features(self) -> int:
        if hasattr(self.model, "n_features_in_"):
            return self.model.n_features_in_
        if hasattr(self.model, "coef_"):
            coef = self.model.coef_
            return coef.shape[1] if coef.ndim > 1 else len(coef)
        if self.feature_names:
            return len(self.feature_names)
        return 10

    def explain(self, sample: np.ndarray) -> Dict[str, Any]:
        """
        Explain one prediction.

        Returns JSON-friendly dict:
        {
            "feature_importance": {...},
            "shap_values": [...],
            "base_value": float
        }
        """
        if self.shap is None or self.explainer is None:
            return {
                "feature_importance": {},
                "shap_values": [],
                "base_value": 0.0,
                "error": "SHAP not available",
            }

        # ensure 2D
        if sample.ndim == 1:
            sample = sample.reshape(1, -1)

        try:
            # unified API
            explanation = self.explainer(sample)

            values = explanation.values[0]
            base_value = float(
                explanation.base_values[0]
                if hasattr(explanation.base_values, "__len__")
                else explanation.base_values
            )

            # map to feature names
            feature_importance = {}
            if self.feature_names:
                for name, val in zip(self.feature_names, values):
                    feature_importance[name] = float(val)
            else:
                for i, val in enumerate(values):
                    feature_importance[f"feature_{i}"] = float(val)

            return {
                "feature_importance": feature_importance,
                "shap_values": [float(v) for v in values],
                "base_value": base_value,
            }

        except Exception as e:
            logger.exception("SHAP explanation failed: %s", e)
            return {
                "feature_importance": {},
                "shap_values": [],
                "base_value": 0.0,
                "error": str(e),
            }

    def get_top_features(self, sample: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        explanation = self.explain(sample)
        importance = explanation.get("feature_importance", {})

        sorted_feats = sorted(
            importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        return [
            {"feature": f, "importance": v}
            for f, v in sorted_feats[:top_k]
        ]
