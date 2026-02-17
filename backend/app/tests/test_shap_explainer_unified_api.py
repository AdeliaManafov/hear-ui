"""Tests for ShapExplainer unified API path (lines 425-509) and _generate_plot (599-623)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest


class TestShapExplainerUnifiedAPI:
    """Test the newer unified API path: explainer(...) returns Explanation object."""

    def test_unified_api_with_dataframe_input(self):
        """Test explain() with DataFrame input using unified API."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a", "b"]
        obj.use_transformed = False
        obj._preprocessor = None
        obj._masker_numeric = False
        obj._value_to_code = {}

        # Mock explainer that doesn't have shap_values method (forces unified API path)
        mock_explainer = MagicMock()
        del mock_explainer.shap_values  # Remove traditional API
        del mock_explainer.expected_value

        # Mock Explanation object returned by unified API
        mock_explanation = MagicMock()
        mock_explanation.values = np.array([[0.1, 0.2]])  # 2D
        mock_explanation.base_values = 0.3
        mock_explainer.return_value = mock_explanation

        obj.explainer = mock_explainer

        # Input is DataFrame (not ndarray)
        df_input = pd.DataFrame({"a": [1.0], "b": [2.0]})
        result = obj.explain(df_input)

        assert "feature_importance" in result
        assert "a" in result["feature_importance"]
        assert result["base_value"] == pytest.approx(0.3)

    def test_unified_api_with_categorical_encoding(self):
        """Test unified API with categorical encoding fallback."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["cat_col", "num_col"]
        obj.use_transformed = False
        obj._preprocessor = None
        obj._masker_numeric = True  # Categorical encoding was used
        obj._value_to_code = {"cat_col": {"A": 0, "B": 1}}

        mock_explainer = MagicMock()
        del mock_explainer.shap_values
        del mock_explainer.expected_value

        mock_explanation = MagicMock()
        mock_explanation.values = np.array([[0.5, 0.3]])
        mock_explanation.base_values = np.array([0.2])
        mock_explainer.return_value = mock_explanation

        obj.explainer = mock_explainer

        # DataFrame with categorical value that needs encoding
        df = pd.DataFrame({"cat_col": ["A"], "num_col": [5.0]})
        result = obj.explain(df)

        assert "feature_importance" in result
        assert len(result["shap_values"]) == 2

    def test_unified_api_with_preprocessor_transform(self):
        """Test unified API path with preprocessor transformation."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["f1", "f2"]
        obj.use_transformed = True
        obj._preprocessor = MagicMock()
        obj._preprocessor.transform.return_value = np.array([[0.8, 0.9]])
        obj._masker_numeric = False
        obj._value_to_code = {}

        mock_explainer = MagicMock()
        del mock_explainer.shap_values
        mock_explanation = MagicMock()
        mock_explanation.values = np.array([[0.2, 0.1]])
        mock_explanation.base_values = 0.0
        mock_explainer.return_value = mock_explanation
        obj.explainer = mock_explainer

        df = pd.DataFrame({"f1": [1.0], "f2": [2.0]})
        result = obj.explain(df)

        # transform may be called multiple times (once for preprocessing, possibly again in explain logic)
        assert obj._preprocessor.transform.called
        assert "feature_importance" in result

    def test_unified_api_preprocessor_transform_fails(self):
        """Test fallback when preprocessor transform fails."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a", "b"]
        obj.use_transformed = True
        obj._preprocessor = MagicMock()
        obj._preprocessor.transform.side_effect = ValueError("transform error")
        obj._masker_numeric = False
        obj._value_to_code = {}

        mock_explainer = MagicMock()
        del mock_explainer.shap_values
        mock_explanation = MagicMock()
        mock_explanation.values = np.array([[0.1, 0.2]])
        mock_explanation.base_values = 0.0
        mock_explainer.return_value = mock_explanation
        obj.explainer = mock_explainer

        df = pd.DataFrame({"a": [1.0], "b": [2.0]})
        result = obj.explain(df)

        # Should fallback to df.values
        assert "feature_importance" in result

    def test_unified_api_explanation_values_none(self):
        """Test when Explanation object has no values or shap_values."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a"]
        obj.use_transformed = False
        obj._preprocessor = None
        obj._masker_numeric = False
        obj._value_to_code = {}

        mock_explainer = MagicMock()
        del mock_explainer.shap_values
        mock_explanation = MagicMock()
        del mock_explanation.values
        del mock_explanation.shap_values
        mock_explainer.return_value = mock_explanation
        obj.explainer = mock_explainer

        result = obj.explain(np.array([[1.0]]))
        # Should catch exception and return error
        assert "error" in result

    def test_unified_api_multiclass_list_values(self):
        """Test unified API with list of arrays (multiclass)."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["f1", "f2"]
        obj.use_transformed = False
        obj._preprocessor = None
        obj._masker_numeric = False
        obj._value_to_code = {}

        mock_explainer = MagicMock()
        del mock_explainer.shap_values
        mock_explanation = MagicMock()
        # List of arrays (multi-class)
        mock_explanation.values = [np.array([[0.1, 0.2]]), np.array([[0.3, 0.4]])]
        mock_explanation.base_values = [0.0, 0.5]
        mock_explainer.return_value = mock_explanation
        obj.explainer = mock_explainer

        result = obj.explain(np.array([[1.0, 2.0]]))
        assert result["shap_values"] == [pytest.approx(0.3), pytest.approx(0.4)]

    def test_unified_api_base_values_extraction(self):
        """Test extraction of base_values from unified API."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a"]
        obj.use_transformed = False
        obj._preprocessor = None
        obj._masker_numeric = False
        obj._value_to_code = {}

        mock_explainer = MagicMock()
        del mock_explainer.shap_values
        mock_explanation = MagicMock()
        mock_explanation.values = np.array([[0.5]])
        # base_values as array
        mock_explanation.base_values = np.array([0.25])
        del mock_explanation.expected_value
        mock_explainer.return_value = mock_explanation
        obj.explainer = mock_explainer

        result = obj.explain(np.array([[1.0]]))
        assert result["base_value"] == pytest.approx(0.25)


class TestGeneratePlot:
    """Test _generate_plot method (lines 599-623)."""

    @pytest.mark.skipif(
        not pytest.importorskip("matplotlib", reason="matplotlib not installed"),
        reason="matplotlib not available",
    )
    def test_generate_plot_creates_base64_image(self):
        """Test that _generate_plot returns base64 encoded PNG."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["feature_1", "feature_2"]

        # Mock SHAP Explanation class
        mock_explanation_cls = MagicMock()
        obj._shap.Explanation = mock_explanation_cls

        # Mock waterfall plot
        obj._shap.plots = MagicMock()
        obj._shap.plots.waterfall = MagicMock()

        shap_vals = np.array([0.5, -0.3])
        base = 0.2
        sample = np.array([1.0, 2.0])

        with patch("matplotlib.pyplot") as mock_plt:
            mock_fig = MagicMock()
            mock_ax = MagicMock()
            mock_plt.subplots.return_value = (mock_fig, mock_ax)

            result = obj._generate_plot(shap_vals, base, sample)

            assert result.startswith("data:image/png;base64,")
            mock_plt.subplots.assert_called_once_with(figsize=(10, 6))
            obj._shap.plots.waterfall.assert_called_once()
            mock_plt.close.assert_called_once()

    @pytest.mark.skipif(
        not pytest.importorskip("matplotlib", reason="matplotlib not installed"),
        reason="matplotlib not available",
    )
    def test_generate_plot_with_missing_feature_names(self):
        """Test _generate_plot when feature_names is None."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = None

        mock_explanation_cls = MagicMock()
        obj._shap.Explanation = mock_explanation_cls
        obj._shap.plots = MagicMock()

        with patch("matplotlib.pyplot") as mock_plt:
            mock_plt.subplots.return_value = (MagicMock(), MagicMock())

            result = obj._generate_plot(np.array([0.1, 0.2]), 0.0, np.array([1.0, 2.0]))

            assert "data:image/png;base64," in result
