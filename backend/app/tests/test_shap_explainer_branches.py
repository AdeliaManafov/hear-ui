"""Focused tests for SHAP explainer initialization branches (Linear, Tree, Kernel)."""

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

import numpy as np

from app.core.shap_explainer import ShapExplainer


def make_fake_shap(linear_ok=True, tree_ok=True, kernel_ok=True):
    calls = {}

    class FakeLinear:
        def __init__(self, estimator, background_data, feature_names=None):
            calls["linear"] = {
                "estimator": estimator,
                "bg": background_data,
                "fnames": feature_names,
            }
            # return an object with shap_values when used
            obj = MagicMock()
            obj.shap_values.return_value = np.array([[0.1, 0.2]])
            obj.expected_value = 0.5
            return obj

    class FakeTree:
        def __init__(self, estimator, data=None, feature_names=None):
            calls["tree"] = {"estimator": estimator}
            return MagicMock()

    class FakeKernel:
        def __init__(self, predict_fn, background_data):
            calls["kernel"] = {"predict_fn": predict_fn}
            return MagicMock()

    fake = SimpleNamespace(
        LinearExplainer=FakeLinear if linear_ok else None,
        TreeExplainer=FakeTree if tree_ok else None,
        KernelExplainer=FakeKernel if kernel_ok else None,
        Explanation=lambda *a, **k: None,
        plots=SimpleNamespace(waterfall=lambda *a, **k: None),
    )
    return fake, calls


def test_init_transformed_linear_branch(monkeypatch):
    fake_shap, calls = make_fake_shap()
    # inject fake shap module
    sys.modules["shap"] = fake_shap

    try:
        se = ShapExplainer.__new__(ShapExplainer)
        se._shap = fake_shap

        # fake final estimator with coef_ to trigger linear branch
        class Est:
            coef_ = np.array([1.0])
            feature_names_in_ = np.array(["f1"])

            def predict(self, X):
                return np.zeros((X.shape[0],))

        est = Est()
        est.coef_ = np.array([0.1, 0.2])
        se._final_estimator = est
        se._preprocessor = MagicMock()
        se.feature_names = ["a", "b"]
        se._get_n_features = lambda: 2

        se._init_transformed_explainer(background_data=None)
        assert "linear" in calls
    finally:
        del sys.modules["shap"]


def test_init_transformed_tree_branch(monkeypatch):
    fake_shap, calls = make_fake_shap()
    sys.modules["shap"] = fake_shap
    try:
        se = ShapExplainer.__new__(ShapExplainer)
        se._shap = fake_shap

        # final estimator with feature_importances_ to trigger tree branch
        class Est:
            feature_importances_ = np.array([0.5])
            feature_names_in_ = np.array(["f1"])

            def predict(self, X):
                return np.zeros((X.shape[0],))

        est = Est()
        est.feature_importances_ = np.array([0.1, 0.2])
        se._final_estimator = est
        se._preprocessor = MagicMock()
        se.feature_names = ["a", "b"]
        se._get_n_features = lambda: 2

        se._init_transformed_explainer(background_data=None)
        assert "tree" in calls
    finally:
        del sys.modules["shap"]


def test_init_transformed_kernel_fallback(monkeypatch):
    # create fake shap without Tree or Linear to force Kernel branch
    fake_shap, calls = make_fake_shap(linear_ok=False, tree_ok=False)
    sys.modules["shap"] = fake_shap
    try:
        se = ShapExplainer.__new__(ShapExplainer)
        se._shap = fake_shap

        # estimator without coef_ or tree
        class Est:
            feature_names_in_ = np.array(["f1"])

            def predict(self, X):
                return np.zeros((X.shape[0],))

        est = Est()
        se._final_estimator = est
        se._preprocessor = MagicMock()
        se.feature_names = None
        se._get_n_features = lambda: 2

        se._init_transformed_explainer(background_data=np.zeros((1, 2)))
        assert "kernel" in calls
    finally:
        del sys.modules["shap"]
