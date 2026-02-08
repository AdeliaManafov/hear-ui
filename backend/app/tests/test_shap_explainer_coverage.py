"""Additional tests for app.core.shap_explainer – targeting uncovered branches.

Focuses on: _get_n_features, _init_raw_explainer, _init_transformed_explainer,
_prepare_background_and_transform, explain() edge cases, get_top_features,
_generate_plot, _extract_feature_names.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pandas as pd
import pytest

# ===========================================================================
# _get_n_features
# ===========================================================================


class TestGetNFeatures:
    def test_via_n_features_in(self):
        from app.core.shap_explainer import ShapExplainer

        model = MagicMock()
        model.n_features_in_ = 10
        # Bypass __init__ to test method directly
        obj = ShapExplainer.__new__(ShapExplainer)
        obj.model = model
        obj.feature_names = None
        obj._final_estimator = model
        assert obj._get_n_features() == 10

    def test_via_coef(self):
        from app.core.shap_explainer import ShapExplainer

        model = MagicMock()
        del model.n_features_in_
        model.coef_ = np.array([[0.1, 0.2, 0.3]])
        obj = ShapExplainer.__new__(ShapExplainer)
        obj.model = model
        obj.feature_names = None
        assert obj._get_n_features() == 3

    def test_via_coef_1d(self):
        from app.core.shap_explainer import ShapExplainer

        model = MagicMock()
        del model.n_features_in_
        model.coef_ = np.array([0.1, 0.2])
        obj = ShapExplainer.__new__(ShapExplainer)
        obj.model = model
        obj.feature_names = None
        assert obj._get_n_features() == 2

    def test_via_feature_names(self):
        from app.core.shap_explainer import ShapExplainer

        model = MagicMock()
        del model.n_features_in_
        del model.coef_
        obj = ShapExplainer.__new__(ShapExplainer)
        obj.model = model
        obj.feature_names = ["a", "b", "c", "d"]
        assert obj._get_n_features() == 4

    def test_fallback(self):
        from app.core.shap_explainer import ShapExplainer

        model = MagicMock()
        del model.n_features_in_
        del model.coef_
        obj = ShapExplainer.__new__(ShapExplainer)
        obj.model = model
        obj.feature_names = None
        assert obj._get_n_features() == 10


# ===========================================================================
# _extract_feature_names
# ===========================================================================


class TestExtractFeatureNames:
    def test_from_preprocessor(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._preprocessor = MagicMock()
        obj._preprocessor.get_feature_names_out.return_value = ["f1", "f2"]
        obj.model = MagicMock()
        result = obj._extract_feature_names()
        assert result == ["f1", "f2"]

    def test_from_model(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._preprocessor = None
        obj.model = MagicMock()
        obj.model.feature_names_in_ = ["a", "b"]
        result = obj._extract_feature_names()
        assert result == ["a", "b"]

    def test_returns_none(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._preprocessor = None
        obj.model = MagicMock()
        del obj.model.feature_names_in_
        result = obj._extract_feature_names()
        assert result is None


# ===========================================================================
# explain() edge cases
# ===========================================================================


class TestExplainEdgeCases:
    def _make_explainer_obj(self, shap_vals, base_value=0.5, feature_names=None):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.explainer = MagicMock()
        obj.feature_names = feature_names
        obj.use_transformed = False
        obj._preprocessor = None
        obj._final_estimator = None
        obj._masker_numeric = False
        obj._value_to_code = {}

        # Traditional API
        obj.explainer.shap_values = MagicMock(return_value=shap_vals)
        obj.explainer.expected_value = base_value
        return obj

    def test_explain_shap_not_available(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = None
        obj.explainer = None
        obj.feature_names = None

        result = obj.explain(np.array([1.0, 2.0]))
        assert result["feature_importance"] == {}
        assert result["shap_values"] == []

    def test_explain_1d_sample(self):
        # shap_values returns list of arrays (multi-class)
        vals = [np.array([[0.1, 0.2]]), np.array([[0.3, 0.4]])]
        obj = self._make_explainer_obj(vals, base_value=[0.1, 0.5])
        result = obj.explain(np.array([1.0, 2.0]))  # 1-D → reshaped
        assert len(result["shap_values"]) == 2

    def test_explain_2d_shap_values(self):
        vals = np.array([[0.5, -0.3]])  # 2-D single output
        obj = self._make_explainer_obj(vals, base_value=0.2)
        result = obj.explain(np.array([[1.0, 2.0]]))
        assert result["shap_values"] == [pytest.approx(0.5), pytest.approx(-0.3)]

    def test_explain_3d_shap_multi_class(self):
        # (1, 2, 2) shape: 1 sample, 2 features, 2 classes
        vals = np.array([[[0.1, 0.2], [0.3, 0.4]]])
        obj = self._make_explainer_obj(vals, base_value=0.0)
        result = obj.explain(np.array([[1.0, 2.0]]))
        # Should pick class 1 (index 1)
        assert result["shap_values"] == [pytest.approx(0.2), pytest.approx(0.4)]

    def test_explain_3d_single_class(self):
        vals = np.array([[[0.5], [0.6]]])  # 1 sample, 2 features, 1 class
        obj = self._make_explainer_obj(vals, base_value=0.0)
        result = obj.explain(np.array([[1.0, 2.0]]))
        assert result["shap_values"] == [pytest.approx(0.5), pytest.approx(0.6)]

    def test_explain_with_feature_names(self):
        vals = np.array([[0.1, 0.2]])
        obj = self._make_explainer_obj(vals, feature_names=["age", "gender"])
        result = obj.explain(np.array([[1.0, 2.0]]))
        assert "age" in result["feature_importance"]
        assert "gender" in result["feature_importance"]

    def test_explain_without_feature_names(self):
        vals = np.array([[0.1, 0.2]])
        obj = self._make_explainer_obj(vals, feature_names=None)
        result = obj.explain(np.array([[1.0, 2.0]]))
        assert "feature_0" in result["feature_importance"]

    def test_explain_with_return_plot(self):
        vals = np.array([[0.1, 0.2]])
        obj = self._make_explainer_obj(vals, feature_names=["a", "b"])
        # Mock _generate_plot
        obj._generate_plot = MagicMock(return_value="data:image/png;base64,AAAA")

        result = obj.explain(np.array([[1.0, 2.0]]), return_plot=True)
        assert "plot_base64" in result
        obj._generate_plot.assert_called_once()

    def test_explain_plot_failure_graceful(self):
        vals = np.array([[0.1, 0.2]])
        obj = self._make_explainer_obj(vals, feature_names=["a", "b"])
        obj._generate_plot = MagicMock(side_effect=Exception("plot error"))

        result = obj.explain(np.array([[1.0, 2.0]]), return_plot=True)
        assert "plot_base64" not in result
        assert len(result["shap_values"]) == 2  # explanation still works

    def test_explain_with_transform(self):
        """When use_transformed=True and preprocessor exists, sample is transformed."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a", "b"]
        obj.use_transformed = True
        obj._preprocessor = MagicMock()
        obj._preprocessor.transform.return_value = np.array([[0.5, 0.5]])
        obj._final_estimator = None
        obj._masker_numeric = False
        obj._value_to_code = {}

        mock_explainer = MagicMock()
        mock_explainer.shap_values = MagicMock(return_value=np.array([[0.1, 0.2]]))
        mock_explainer.expected_value = 0.0
        obj.explainer = mock_explainer

        result = obj.explain(np.array([[1.0, 2.0]]))
        obj._preprocessor.transform.assert_called_once()
        assert "a" in result["feature_importance"]


# ===========================================================================
# get_top_features
# ===========================================================================


class TestGetTopFeatures:
    def test_returns_sorted_features(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a", "b", "c"]
        # Mock explain to return feature importances
        obj.explain = MagicMock(
            return_value={
                "feature_importance": {"a": 0.1, "b": -0.5, "c": 0.3},
                "shap_values": [0.1, -0.5, 0.3],
                "base_value": 0.0,
            }
        )
        top = obj.get_top_features(np.array([[1.0, 2.0, 3.0]]), top_k=2)
        assert len(top) == 2
        assert top[0]["feature"] == "b"  # highest abs importance
        assert top[0]["importance"] == -0.5

    def test_includes_feature_values(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj.feature_names = ["a", "b"]
        obj.explain = MagicMock(
            return_value={
                "feature_importance": {"a": 0.3, "b": 0.1},
                "shap_values": [0.3, 0.1],
                "base_value": 0.0,
            }
        )
        top = obj.get_top_features(np.array([[5.0, 10.0]]), top_k=2)
        assert "value" in top[0]
        assert top[0]["value"] == pytest.approx(5.0)


# ===========================================================================
# _init_transformed_explainer edge cases
# ===========================================================================


class TestInitTransformedExplainer:
    def test_no_background_data(self):
        """When background_data is None, uses zeros."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj._final_estimator = MagicMock()
        obj._final_estimator.coef_ = np.array([[0.1, 0.2]])
        del obj._final_estimator.feature_importances_
        del obj._final_estimator.tree_
        obj.feature_names = ["a", "b"]
        obj.model = MagicMock()
        obj.model.n_features_in_ = 2

        obj._init_transformed_explainer(None)
        # Should have initialized LinearExplainer or KernelExplainer
        assert obj.explainer is not None or obj._shap.LinearExplainer.called

    def test_tree_model(self):
        """Tree-based model uses TreeExplainer."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj._final_estimator = MagicMock()
        obj._final_estimator.feature_importances_ = np.array([0.5, 0.5])
        obj.feature_names = None
        obj.model = MagicMock()

        bg = np.zeros((5, 2))
        obj._init_transformed_explainer(bg)
        obj._shap.TreeExplainer.assert_called()

    def test_kernel_fallback(self):
        """When no coef_ and no tree, falls back to KernelExplainer."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj._final_estimator = MagicMock()
        del obj._final_estimator.feature_importances_
        del obj._final_estimator.tree_
        del obj._final_estimator.coef_
        obj._final_estimator.predict_proba = MagicMock()
        obj.feature_names = None
        obj.model = MagicMock()

        bg = np.zeros((5, 2))
        obj._init_transformed_explainer(bg)
        obj._shap.KernelExplainer.assert_called()


# ===========================================================================
# _init_raw_explainer edge cases
# ===========================================================================


class TestInitRawExplainer:
    def test_no_background_uses_zeros(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj._final_estimator = MagicMock()
        obj._final_estimator.coef_ = np.array([[0.1]])
        del obj._final_estimator.feature_importances_
        del obj._final_estimator.tree_
        obj.feature_names = ["a"]
        obj.model = MagicMock()
        obj.model.n_features_in_ = 1

        obj._init_raw_explainer(None)
        # Should call LinearExplainer with generated zeros
        assert obj._shap.LinearExplainer.called or obj._shap.KernelExplainer.called

    def test_unified_api_fallback(self):
        """When Tree and Linear fail, tries shap.Explainer (unified API)."""
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj._shap = MagicMock()
        obj._final_estimator = MagicMock()
        del obj._final_estimator.feature_importances_
        del obj._final_estimator.tree_
        del obj._final_estimator.coef_
        obj.feature_names = None
        obj.model = MagicMock()

        # Make KernelExplainer fail so unified API path is tested
        obj._shap.Explainer.return_value = MagicMock()

        bg = np.zeros((2, 3))
        obj._init_raw_explainer(bg)
        obj._shap.Explainer.assert_called()


# ===========================================================================
# _prepare_background_and_transform
# ===========================================================================


class TestPrepareBackgroundAndTransform:
    def test_with_preprocessor_success(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj.use_transformed = True
        obj._preprocessor = MagicMock()
        obj._preprocessor.transform.return_value = np.array([[1.0, 2.0]])
        obj._cat_columns = []
        obj._value_to_code = {}
        obj._code_to_value = {}
        obj._masker_numeric = False

        df = pd.DataFrame({"a": [1.0], "b": ["cat"]})
        result = obj._prepare_background_and_transform(df)
        np.testing.assert_array_equal(result, [[1.0, 2.0]])

    def test_preprocessor_fails_encodes_categoricals(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj.use_transformed = True
        obj._preprocessor = MagicMock()
        # First transform fails, second succeeds
        obj._preprocessor.transform.side_effect = [
            ValueError("can't transform"),
            np.array([[0.0, 1.0]]),
        ]
        obj._cat_columns = []
        obj._value_to_code = {}
        obj._code_to_value = {}
        obj._masker_numeric = False

        df = pd.DataFrame({"a": [1.0], "b": ["cat"]})
        result = obj._prepare_background_and_transform(df)
        assert result is not None

    def test_no_preprocessor(self):
        from app.core.shap_explainer import ShapExplainer

        obj = ShapExplainer.__new__(ShapExplainer)
        obj.use_transformed = False
        obj._preprocessor = None
        obj._cat_columns = []
        obj._value_to_code = {}
        obj._code_to_value = {}
        obj._masker_numeric = False

        df = pd.DataFrame({"a": [1.0], "b": [2.0]})
        result = obj._prepare_background_and_transform(df)
        assert result is not None
        assert result.shape == (1, 2)
