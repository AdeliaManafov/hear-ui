"""Additional tests for ShapExplainer behavior."""

from unittest.mock import MagicMock

import numpy as np
import pytest

from app.core.shap_explainer import ShapExplainer


def test_explain_returns_empty_when_no_shap_or_explainer():
    se = ShapExplainer.__new__(ShapExplainer)
    # simulate missing shap/explainer
    se._shap = None
    se.explainer = None
    se.feature_names = None
    se._preprocessor = None
    se.use_transformed = False

    out = se.explain(np.array([1.0, 2.0]))
    assert out.get("feature_importance") == {}
    assert out.get("shap_values") == []


def test_explain_with_shap_values():
    se = ShapExplainer.__new__(ShapExplainer)
    se._shap = MagicMock()
    # fake explainer with shap_values and expected_value
    fake_explainer = MagicMock()
    fake_explainer.shap_values.return_value = np.array([[0.1, 0.2]])
    fake_explainer.expected_value = 0.5
    se.explainer = fake_explainer
    se.feature_names = ["a", "b"]
    se._preprocessor = None
    se.use_transformed = False

    sample = np.array([1.0, 2.0])
    out = se.explain(sample)

    assert "feature_importance" in out
    assert out["base_value"] == pytest.approx(0.5)
    assert out["feature_importance"]["a"] == pytest.approx(0.1)
    assert out["shap_values"][0] == pytest.approx(0.1)


def test_get_top_features_uses_explain():
    se = ShapExplainer.__new__(ShapExplainer)
    se.explain = MagicMock(return_value={
        "feature_importance": {"a": 0.1, "b": -0.2},
        "shap_values": [0.1, -0.2],
        "base_value": 0.0,
    })
    se.feature_names = ["a", "b"]

    sample = np.array([1.0, 2.0])
    top = se.get_top_features(sample, top_k=2)
    assert isinstance(top, list)
    assert top[0]["feature"] in ("a", "b")
    assert len(top) == 2
