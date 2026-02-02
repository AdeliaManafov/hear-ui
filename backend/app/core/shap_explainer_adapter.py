"""SHAP explainer implementation conforming to ExplainerInterface.

Wraps the existing ShapExplainer class to make it compatible with the
generic explainer framework.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from .explainer_interface import ExplainerInterface, Explanation
from .shap_explainer import ShapExplainer as LegacyShapExplainer

logger = logging.getLogger(__name__)


class ShapExplainerAdapter(ExplainerInterface):
    """SHAP-based explainer conforming to ExplainerInterface.

    This adapter wraps the existing SHAP implementation and makes it
    compatible with the generic explainer framework.
    """

    def __init__(
        self,
        model: Any = None,
        feature_names: list[str] | None = None,
        background_data: Any | None = None,
        **kwargs,
    ):
        """Initialize SHAP explainer.

        Args:
            model: Trained model instance
            feature_names: List of feature names
            background_data: Background samples for SHAP
            **kwargs: Additional SHAP-specific parameters
        """
        self.model = model
        self.feature_names = feature_names
        self.background_data = background_data
        self.shap_explainer: LegacyShapExplainer | None = None

        # Initialize legacy SHAP explainer if model provided
        if model is not None:
            try:
                self.shap_explainer = LegacyShapExplainer(
                    model=model,
                    feature_names=feature_names,
                    background_data=background_data,
                    use_transformed=kwargs.get("use_transformed", True),
                )
            except Exception as e:
                logger.warning(f"Failed to initialize SHAP explainer: {e}")
                self.shap_explainer = None

    def explain(
        self,
        model: Any,
        input_data: np.ndarray | dict,
        feature_names: list[str] | None = None,
        **kwargs,
    ) -> Explanation:
        """Generate SHAP explanation for a prediction.

        Args:
            model: The trained model
            input_data: Preprocessed input array or raw dict
            feature_names: Feature names for display
            **kwargs: Additional parameters (e.g., include_plot)

        Returns:
            Explanation object with SHAP values and metadata
        """
        # Use provided feature names or fallback to instance feature names
        feat_names = feature_names or self.feature_names

        # Convert dict to array if needed
        if isinstance(input_data, dict):
            # For dict input, we need preprocessing - but this should be done
            # by the caller. For now, raise error.
            raise ValueError(
                "ShapExplainerAdapter requires preprocessed array input. "
                "Use a DatasetAdapter to preprocess dict inputs first."
            )

        X = input_data if isinstance(input_data, np.ndarray) else np.array(input_data)

        # Ensure 2D array
        if X.ndim == 1:
            X = X.reshape(1, -1)

        # Get prediction
        if hasattr(model, "predict_proba"):
            prediction = float(model.predict_proba(X)[:, 1][0])
        else:
            prediction = float(model.predict(X)[0])

        # Try to use SHAP explainer if available
        if self.shap_explainer is not None:
            try:
                result = self.shap_explainer.explain_instance(
                    X, include_plot=kwargs.get("include_plot", False)
                )

                # Extract SHAP values and feature importance
                shap_values = result.get("shap_values", [])
                base_value = result.get("base_value", 0.0)

                # Build feature importance dict
                if feat_names and len(feat_names) == len(shap_values):
                    feature_importance = dict(
                        zip(feat_names, shap_values, strict=False)
                    )
                else:
                    feature_importance = {
                        f"feature_{i}": val for i, val in enumerate(shap_values)
                    }

                # Build feature values dict
                feature_values = {}
                if feat_names and X.shape[1] == len(feat_names):
                    feature_values = dict(zip(feat_names, X[0], strict=False))
                else:
                    feature_values = {f"feature_{i}": val for i, val in enumerate(X[0])}

                metadata = {
                    "shap_values": shap_values,
                    "plot_base64": result.get("plot"),
                }

                return Explanation(
                    feature_importance=feature_importance,
                    feature_values=feature_values,
                    base_value=base_value,
                    prediction=prediction,
                    method="shap",
                    metadata=metadata,
                )

            except Exception as e:
                logger.warning(f"SHAP explanation failed: {e}. Using fallback.")

        # Fallback: coefficient-based explanation for linear models
        return self._coefficient_based_explanation(model, X, feat_names, prediction)

    def _coefficient_based_explanation(
        self,
        model: Any,
        X: np.ndarray,
        feature_names: list[str] | None,
        prediction: float,
    ) -> Explanation:
        """Fallback explanation using model coefficients.

        Args:
            model: Linear model with coef_ attribute
            X: Input features
            feature_names: Feature names
            prediction: Model prediction

        Returns:
            Explanation with coefficient-based importance
        """
        # Try to extract coefficients
        coefficients = None
        if hasattr(model, "coef_"):
            coefficients = model.coef_[0] if model.coef_.ndim > 1 else model.coef_
        elif hasattr(model, "steps"):
            # Pipeline: check final estimator
            final_estimator = model.steps[-1][1]
            if hasattr(final_estimator, "coef_"):
                coefficients = (
                    final_estimator.coef_[0]
                    if final_estimator.coef_.ndim > 1
                    else final_estimator.coef_
                )

        if coefficients is None:
            # No coefficients available - return zero importance
            feature_importance = {
                (feature_names[i] if feature_names else f"feature_{i}"): 0.0
                for i in range(X.shape[1])
            }
            feature_values = {
                (feature_names[i] if feature_names else f"feature_{i}"): float(X[0, i])
                for i in range(X.shape[1])
            }

            return Explanation(
                feature_importance=feature_importance,
                feature_values=feature_values,
                base_value=0.0,
                prediction=prediction,
                method="shap_fallback",
                metadata={
                    "note": "No coefficients available, returning zero importance"
                },
            )

        # Calculate contributions: coef * value
        contributions = coefficients * X[0]

        # Build dictionaries
        feature_importance = {}
        feature_values = {}
        for i in range(len(contributions)):
            name = (
                feature_names[i]
                if feature_names and i < len(feature_names)
                else f"feature_{i}"
            )
            feature_importance[name] = float(contributions[i])
            feature_values[name] = float(X[0, i])

        # Base value approximation: intercept or 0
        base_value = 0.0
        if hasattr(model, "intercept_"):
            base_value = float(
                model.intercept_[0]
                if hasattr(model.intercept_, "__len__")
                else model.intercept_
            )
        elif hasattr(model, "steps"):
            final_estimator = model.steps[-1][1]
            if hasattr(final_estimator, "intercept_"):
                base_value = float(
                    final_estimator.intercept_[0]
                    if hasattr(final_estimator.intercept_, "__len__")
                    else final_estimator.intercept_
                )

        return Explanation(
            feature_importance=feature_importance,
            feature_values=feature_values,
            base_value=base_value,
            prediction=prediction,
            method="coefficient_based",
            metadata={"note": "Using coefficient * value as SHAP approximation"},
        )

    def get_method_name(self) -> str:
        """Return the explainer method name."""
        return "shap"

    def supports_visualization(self) -> bool:
        """SHAP supports visualization."""
        return True

    def generate_visualization(self, explanation: Explanation, **kwargs) -> str | None:
        """Generate SHAP waterfall plot.

        Args:
            explanation: The explanation to visualize
            **kwargs: Visualization parameters

        Returns:
            Base64-encoded plot or None
        """
        # If we already have a plot in metadata, return it
        if explanation.metadata and "plot_base64" in explanation.metadata:
            return explanation.metadata["plot_base64"]

        # Otherwise, would need to regenerate - not implemented yet
        return None
