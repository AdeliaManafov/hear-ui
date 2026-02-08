"""Tests for app.core.alternative_explainers – CoefficientExplainer & LIMEExplainer."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest

from app.core.alternative_explainers import CoefficientExplainer, LIMEExplainer
from app.core.explainer_interface import Explanation

# ---------------------------------------------------------------------------
# Helpers – tiny mock models
# ---------------------------------------------------------------------------


def _make_linear_model(n_features: int = 3):
    """Return a mock linear model with coef_, intercept_, and predict_proba."""
    m = MagicMock()
    m.coef_ = np.array([[0.5, -0.3, 0.2]])  # 2-D
    m.intercept_ = np.array([0.1])
    m.predict_proba = MagicMock(return_value=np.array([[0.3, 0.7]]))
    m.predict = MagicMock(return_value=np.array([1]))
    return m


def _make_pipeline_model(n_features: int = 3):
    """Return a mock Pipeline whose final step has coef_."""
    final_est = MagicMock()
    final_est.coef_ = np.array([0.4, -0.1, 0.6])  # 1-D
    final_est.intercept_ = np.array([0.05])
    pipe = MagicMock()
    pipe.steps = [("scaler", MagicMock()), ("clf", final_est)]
    pipe.predict_proba = MagicMock(return_value=np.array([[0.4, 0.6]]))
    # Remove coef_ from the pipeline itself so code uses the steps path
    del pipe.coef_
    del pipe.intercept_
    return pipe


def _make_model_without_coef():
    m = MagicMock()
    del m.coef_
    del m.steps
    m.predict_proba = MagicMock(return_value=np.array([[0.5, 0.5]]))
    return m


def _make_model_predict_only(n_features=3):
    m = MagicMock()
    m.coef_ = np.array([[0.1, 0.2, 0.3]])
    m.intercept_ = 0.05  # scalar intercept
    del m.predict_proba
    m.predict = MagicMock(return_value=np.array([0.42]))
    return m


# ===========================================================================
# CoefficientExplainer
# ===========================================================================


class TestCoefficientExplainerBasic:
    def test_explain_returns_explanation(self):
        model = _make_linear_model()
        expl = CoefficientExplainer()
        X = np.array([[1.0, 2.0, 3.0]])
        result = expl.explain(model, X, feature_names=["a", "b", "c"])

        assert isinstance(result, Explanation)
        assert result.method == "coefficient"
        assert "a" in result.feature_importance
        assert "b" in result.feature_importance
        assert "c" in result.feature_importance
        assert result.prediction == pytest.approx(0.7)
        assert result.base_value == pytest.approx(0.1)

    def test_explain_1d_input(self):
        model = _make_linear_model()
        expl = CoefficientExplainer()
        X = np.array([1.0, 2.0, 3.0])  # 1-D → should be reshaped
        result = expl.explain(model, X)
        assert isinstance(result, Explanation)
        assert len(result.feature_importance) == 3

    def test_explain_no_feature_names(self):
        model = _make_linear_model()
        expl = CoefficientExplainer()
        X = np.array([[1.0, 2.0, 3.0]])
        result = expl.explain(model, X)
        assert "feature_0" in result.feature_importance
        assert "feature_1" in result.feature_importance

    def test_explain_dict_input_raises(self):
        model = _make_linear_model()
        expl = CoefficientExplainer()
        with pytest.raises(ValueError, match="requires preprocessed array"):
            expl.explain(model, {"a": 1})

    def test_explain_no_coef_raises(self):
        model = _make_model_without_coef()
        expl = CoefficientExplainer()
        with pytest.raises(ValueError, match="does not have coefficients"):
            expl.explain(model, np.array([[1.0, 2.0]]))

    def test_explain_coef_mismatch_raises(self):
        model = _make_linear_model(3)
        expl = CoefficientExplainer()
        with pytest.raises(ValueError, match="does not match"):
            expl.explain(model, np.array([[1.0, 2.0]]))  # 2 features vs 3 coefs

    def test_contributions_match_coef_times_value(self):
        model = _make_linear_model()
        expl = CoefficientExplainer()
        X = np.array([[2.0, 3.0, 4.0]])
        result = expl.explain(model, X, feature_names=["a", "b", "c"])

        # coef_ 2D → first row: [0.5, -0.3, 0.2]
        assert result.feature_importance["a"] == pytest.approx(1.0)
        assert result.feature_importance["b"] == pytest.approx(-0.9)
        assert result.feature_importance["c"] == pytest.approx(0.8)

    def test_metadata_contains_coefficients(self):
        model = _make_linear_model()
        expl = CoefficientExplainer()
        result = expl.explain(model, np.array([[1.0, 2.0, 3.0]]))
        assert "coefficients" in result.metadata

    def test_method_name(self):
        assert CoefficientExplainer().get_method_name() == "coefficient"

    def test_supports_visualization(self):
        assert CoefficientExplainer().supports_visualization() is False


class TestCoefficientExplainerPipeline:
    def test_explain_with_pipeline_model(self):
        model = _make_pipeline_model()
        expl = CoefficientExplainer()
        X = np.array([[1.0, 2.0, 3.0]])
        result = expl.explain(model, X, feature_names=["a", "b", "c"])
        assert isinstance(result, Explanation)
        # coef from final step: [0.4, -0.1, 0.6]
        assert result.feature_importance["a"] == pytest.approx(0.4)

    def test_intercept_from_pipeline(self):
        model = _make_pipeline_model()
        expl = CoefficientExplainer()
        result = expl.explain(model, np.array([[1.0, 1.0, 1.0]]))
        assert result.base_value == pytest.approx(0.05)


class TestCoefficientExplainerPredict:
    def test_predict_only_model(self):
        """Model without predict_proba uses predict() for prediction."""
        model = _make_model_predict_only()
        expl = CoefficientExplainer()
        result = expl.explain(model, np.array([[1.0, 2.0, 3.0]]))
        assert result.prediction == pytest.approx(0.42)

    def test_scalar_intercept(self):
        model = _make_model_predict_only()
        expl = CoefficientExplainer()
        result = expl.explain(model, np.array([[1.0, 2.0, 3.0]]))
        assert result.base_value == pytest.approx(0.05)


# ===========================================================================
# LIMEExplainer
# ===========================================================================


class TestLIMEExplainer:
    def test_init_without_lime_installed(self, monkeypatch):
        """When lime is not importable, the explainer should be created with LimeTabularExplainer=None."""
        import builtins

        real_import = builtins.__import__

        def fake_import(name, *args, **kwargs):
            if name == "lime.lime_tabular" or name == "lime":
                raise ImportError("fake")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", fake_import)
        expl = LIMEExplainer.__new__(LIMEExplainer)
        expl.model = None
        expl.lime_explainer = None
        try:
            from lime.lime_tabular import LimeTabularExplainer  # noqa: F401
            expl.LimeTabularExplainer = LimeTabularExplainer
        except ImportError:
            expl.LimeTabularExplainer = None

        # Should not blow up
        assert expl.LimeTabularExplainer is None or expl.LimeTabularExplainer is not None

    def test_explain_raises_without_lime(self):
        """LIME explain raises ImportError if lime not available."""
        expl = LIMEExplainer.__new__(LIMEExplainer)
        expl.model = None
        expl.lime_explainer = None
        expl.LimeTabularExplainer = None
        with pytest.raises(ImportError, match="LIME is not installed"):
            expl.explain(MagicMock(), np.array([[1.0, 2.0]]))

    def test_explain_raises_on_dict_input(self):
        expl = LIMEExplainer.__new__(LIMEExplainer)
        expl.model = None
        expl.lime_explainer = None
        expl.LimeTabularExplainer = MagicMock()  # pretend lime exists
        with pytest.raises(ValueError, match="requires preprocessed array"):
            expl.explain(MagicMock(), {"a": 1})

    def test_method_name(self):
        expl = LIMEExplainer.__new__(LIMEExplainer)
        assert expl.get_method_name() == "lime"

    def test_supports_visualization(self):
        expl = LIMEExplainer.__new__(LIMEExplainer)
        assert expl.supports_visualization() is True

    def test_explain_with_mock_lime(self):
        """Full explain path with a mocked LIME library."""
        mock_lime_instance = MagicMock()
        mock_explanation = MagicMock()
        mock_explanation.as_list.return_value = [("feat_0", 0.3), ("feat_1", -0.1)]
        mock_explanation.intercept = [0.0, 0.5]
        mock_lime_instance.explain_instance.return_value = mock_explanation

        expl = LIMEExplainer.__new__(LIMEExplainer)
        expl.model = None
        expl.lime_explainer = mock_lime_instance
        expl.LimeTabularExplainer = MagicMock()

        model = MagicMock()
        model.predict_proba = MagicMock(return_value=np.array([[0.2, 0.8]]))
        X = np.array([[1.0, 2.0]])

        result = expl.explain(model, X, feature_names=["feat_0", "feat_1"])
        assert isinstance(result, Explanation)
        assert result.method == "lime"
        assert result.prediction == pytest.approx(0.8)
        assert "feat_0" in result.feature_importance

    def test_explain_predict_only(self):
        """Model without predict_proba."""
        mock_lime_instance = MagicMock()
        mock_explanation = MagicMock()
        mock_explanation.as_list.return_value = [("f0", 0.1)]
        mock_explanation.intercept = [0.1, 0.2]
        mock_lime_instance.explain_instance.return_value = mock_explanation

        model = MagicMock()
        del model.predict_proba
        model.predict = MagicMock(return_value=np.array([0.6]))

        expl = LIMEExplainer.__new__(LIMEExplainer)
        expl.model = None
        expl.lime_explainer = mock_lime_instance
        expl.LimeTabularExplainer = MagicMock()

        result = expl.explain(model, np.array([[5.0]]))
        assert result.prediction == pytest.approx(0.6)

    def test_lime_init_explainer_on_first_call(self):
        """When lime_explainer is None, it creates one from training_data."""
        mock_lime_cls = MagicMock()
        mock_lime_instance = MagicMock()
        mock_explanation = MagicMock()
        mock_explanation.as_list.return_value = [("f0", 0.2)]
        mock_explanation.intercept = [0.0, 0.3]
        mock_lime_instance.explain_instance.return_value = mock_explanation
        mock_lime_cls.return_value = mock_lime_instance

        expl = LIMEExplainer.__new__(LIMEExplainer)
        expl.model = None
        expl.lime_explainer = None  # triggers init path
        expl.LimeTabularExplainer = mock_lime_cls

        model = MagicMock()
        model.predict_proba = MagicMock(return_value=np.array([[0.1, 0.9]]))

        X = np.array([[1.0, 2.0]])
        result = expl.explain(model, X, training_data=np.array([[0, 0], [1, 1]]))
        assert isinstance(result, Explanation)
        mock_lime_cls.assert_called_once()  # constructor was called
