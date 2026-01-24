from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Any

try:
    from lime import lime_tabular
except ImportError:
    lime_tabular = None


class LimeExplainer:
    def __init__(
        self,
        model: Any,
        feature_names: list[str] | None = None,
        training_data: np.ndarray | pd.DataFrame | None = None,
        class_names: list[str] | None = None,
        use_transformed: bool = True,
    ):
        self.model = model
        self.feature_names = feature_names
        self.class_names = class_names or ["class_0", "class_1"]
        self.use_transformed = use_transformed

        self.explainer = None
        self._final_estimator = None
        self._preprocessor = None

        if lime_tabular is None:
            raise ImportError("lime not installed. Run: pip install lime")

        # Pipeline support (ähnlich wie bei deinem SHAP-Code)
        if hasattr(model, "named_steps"):
            self._preprocessor = (
                model.named_steps.get("preprocessor")
                or model.named_steps.get("scaler")
                or model.named_steps.get("transformer")
                or model.named_steps.get("preprocessing")
            )
            self._final_estimator = model.steps[-1][1]
        else:
            self._final_estimator = model

        # Training data vorbereiten
        if training_data is not None:
            self.prepare_training_data(training_data)

    def prepare_training_data(self, training_data: np.ndarray | pd.DataFrame):
        if isinstance(training_data, pd.DataFrame):
            if self.feature_names is None:
                self.feature_names = list(training_data.columns)
            X = training_data.values
        else:
            X = np.asarray(training_data)

        # Optional durch Preprocessor jagen (wie bei SHAP)
        if self.use_transformed and self._preprocessor is not None:
            try:
                X = self._preprocessor.transform(X)
            except Exception:
                pass

        self.explainer = lime_tabular.LimeTabularExplainer(
            training_data=X,
            feature_names=self.feature_names,
            class_names=self.class_names,
            mode="classification"
        )

    def explain(self, sample: np.ndarray) -> dict[str, Any]:
        if self.explainer is None:
            raise RuntimeError("Call prepare_training_data() first")

        # Ensure 1D
        sample = np.asarray(sample)
        if sample.ndim == 2:
            sample = sample[0]

        # Optional transformieren wie bei SHAP
        sample_for_model = sample.reshape(1, -1)
        if self.use_transformed and self._preprocessor is not None:
            try:
                sample_for_model = self._preprocessor.transform(sample_for_model)
                sample = sample_for_model[0]
            except Exception:
                pass

        explanation = self.explainer.explain_instance(
            sample,
            self.model.predict_proba,
            num_features=len(self.feature_names)
        )

        result = {}
        for feature, weight in explanation.as_list():
            result[feature] = {
                "importance": float(abs(weight)),
                "direction": "positive" if weight > 0 else "negative",
                "raw_weight": float(weight)
            }

        return result
