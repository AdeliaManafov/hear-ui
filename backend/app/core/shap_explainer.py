"""SHAP explanation wrapper for model interpretability.

Provides SHAP-based feature importance explanations for predictions,
with support for both linear models and general estimators.
"""

from __future__ import annotations

import base64
import io
import logging
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)


class ShapExplainer:
    """Wrapper for SHAP explanations with support for linear and tree-based models.
    
    This class provides:
    - Feature importance values (SHAP values) for individual predictions
    - Optional visualization as base64-encoded plots
    - Automatic explainer selection based on model type
    """

    def __init__(
        self,
        model: Any,
        background_data: Optional[np.ndarray] = None,
        feature_names: Optional[List[str]] = None,
    ) -> None:
        """Initialize SHAP explainer.
        
        Args:
            model: Trained sklearn model or pipeline
            background_data: Background dataset for KernelExplainer (optional)
            feature_names: List of feature names for visualization
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer: Any = None
        
        # Lazy import to avoid loading shap if not needed
        try:
            import shap
            self._shap = shap
        except ImportError:
            logger.warning("SHAP not installed. Explanations will not be available.")
            self._shap = None
            return
        
        # Select appropriate explainer based on model type
        try:
            # Try LinearExplainer for linear models (faster)
            if hasattr(model, "coef_"):
                logger.info("Using SHAP LinearExplainer for linear model")
                self.explainer = shap.LinearExplainer(model, background_data)
            # Try TreeExplainer for tree-based models
            elif hasattr(model, "tree_"):
                logger.info("Using SHAP TreeExplainer")
                self.explainer = shap.TreeExplainer(model)
            # Fallback to KernelExplainer (slower but works for any model)
            else:
                logger.info("Using SHAP KernelExplainer (fallback)")
                
                # Determine prediction function
                predict_fn = model.predict
                if hasattr(model, "predict_proba"):
                    predict_fn = model.predict_proba
                
                # Handle Pipeline input requirements
                # KernelExplainer passes numpy arrays, but Pipeline might expect DataFrame
                if feature_names:
                    import pandas as pd
                    original_predict = predict_fn
                    
                    def predict_wrapper(data):
                        # data is numpy array from SHAP
                        if isinstance(data, np.ndarray):
                            # Convert back to DataFrame using feature names
                            try:
                                df = pd.DataFrame(data, columns=feature_names)
                                return original_predict(df)
                            except Exception:
                                # Fallback if conversion fails
                                return original_predict(data)
                        return original_predict(data)
                    
                    predict_fn = predict_wrapper

                if background_data is None:
                    logger.warning("No background data provided for KernelExplainer")
                    # Create dummy background
                    n_features = len(feature_names) if feature_names else self._get_n_features()
                    # Create array of zeros (or empty strings if object type needed?)
                    # This is risky for mixed types. Ideally user provides background_data.
                    background_data = np.zeros((1, n_features))
                    
                    # If we have feature names and a pipeline, we might need a DataFrame background
                    if feature_names:
                         # Try to create a dummy DataFrame with correct types if possible
                         # For now, just use the wrapper which handles conversion
                         pass

                self.explainer = shap.KernelExplainer(
                    predict_fn,
                    background_data,
                )
        except Exception as exc:
            logger.exception("Failed to initialize SHAP explainer: %s", exc)
            self.explainer = None

    def _get_n_features(self) -> int:
        """Get number of features expected by model."""
        if hasattr(self.model, "n_features_in_"):
            return self.model.n_features_in_
        if hasattr(self.model, "coef_"):
            return len(self.model.coef_[0]) if self.model.coef_.ndim > 1 else len(self.model.coef_)
        return 68  # fallback to known feature count

    def explain(
        self,
        sample: np.ndarray,
        return_plot: bool = False,
    ) -> Dict[str, Any]:
        """Generate SHAP explanation for a single prediction.
        
        Args:
            sample: Input sample (1D or 2D array)
            return_plot: If True, include base64-encoded waterfall plot
            
        Returns:
            Dictionary with:
            - feature_importance: Dict mapping feature names to SHAP values
            - shap_values: Raw SHAP values as list
            - base_value: Expected value (baseline)
            - plot_base64: Optional base64-encoded plot
        """
        if self._shap is None or self.explainer is None:
            logger.warning("SHAP explainer not available, returning empty explanation")
            return {"feature_importance": {}, "shap_values": [], "base_value": 0.0}
        
        # Ensure 2D array
        if sample.ndim == 1:
            sample = sample.reshape(1, -1)
        
        try:
            # Compute SHAP values
            shap_values = self.explainer.shap_values(sample)
            
            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                # Multi-class: take positive class (index 1)
                shap_vals = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
            else:
                shap_vals = shap_values[0]
            
            # Get base value (expected value)
            if hasattr(self.explainer, "expected_value"):
                base_value = self.explainer.expected_value
                if isinstance(base_value, (list, np.ndarray)):
                    base_value = base_value[1] if len(base_value) > 1 else base_value[0]
            else:
                base_value = 0.0
            
            # Create feature importance dict
            feature_importance = {}
            if self.feature_names:
                for i, name in enumerate(self.feature_names):
                    if i < len(shap_vals):
                        feature_importance[name] = float(shap_vals[i])
            else:
                for i, val in enumerate(shap_vals):
                    feature_importance[f"feature_{i}"] = float(val)
            
            result = {
                "feature_importance": feature_importance,
                "shap_values": [float(v) for v in shap_vals],
                "base_value": float(base_value),
            }
            
            # Optionally generate plot
            if return_plot:
                try:
                    plot_base64 = self._generate_plot(shap_vals, base_value, sample[0])
                    result["plot_base64"] = plot_base64
                except Exception as exc:
                    logger.warning("Failed to generate SHAP plot: %s", exc)
            
            return result
            
        except Exception as exc:
            logger.exception("SHAP explanation failed: %s", exc)
            return {"feature_importance": {}, "shap_values": [], "base_value": 0.0, "error": str(exc)}

    def _generate_plot(
        self,
        shap_values: np.ndarray,
        base_value: float,
        sample: np.ndarray,
    ) -> str:
        """Generate base64-encoded waterfall plot.
        
        Args:
            shap_values: SHAP values for the sample
            base_value: Expected value
            sample: Input sample
            
        Returns:
            Base64-encoded PNG image
        """
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend
        import matplotlib.pyplot as plt
        
        # Create explanation object for plotting
        explanation = self._shap.Explanation(
            values=shap_values,
            base_values=base_value,
            data=sample,
            feature_names=self.feature_names,
        )
        
        # Generate waterfall plot
        fig, ax = plt.subplots(figsize=(10, 6))
        self._shap.plots.waterfall(explanation, show=False)
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
        plt.close(fig)
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f"data:image/png;base64,{image_base64}"

    def get_top_features(
        self,
        sample: np.ndarray,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Get top K most important features for a prediction.
        
        Args:
            sample: Input sample
            top_k: Number of top features to return
            
        Returns:
            List of dicts with 'feature', 'importance', and 'value'
        """
        explanation = self.explain(sample, return_plot=False)
        feature_importance = explanation.get("feature_importance", {})
        
        # Sort by absolute importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True,
        )
        
        # Get sample values if available
        sample_1d = sample.flatten() if sample.ndim > 1 else sample
        
        top_features = []
        for i, (feature, importance) in enumerate(sorted_features[:top_k]):
            feature_dict = {
                "feature": feature,
                "importance": importance,
            }
            # Add feature value if we have it
            if self.feature_names and feature in self.feature_names:
                idx = self.feature_names.index(feature)
                if idx < len(sample_1d):
                    feature_dict["value"] = float(sample_1d[idx])
            top_features.append(feature_dict)
        
        return top_features
