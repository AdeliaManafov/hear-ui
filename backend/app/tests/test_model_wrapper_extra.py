"""Additional tests for ModelWrapper behaviors."""

from unittest.mock import MagicMock

import numpy as np
import pytest

from app.core.model_wrapper import ModelWrapper


def test_predict_raises_when_no_model():
    mw = ModelWrapper()
    mw.model = None
    with pytest.raises(RuntimeError):
        mw.predict({"Alter [J]": 45})


def test_predict_with_predict_proba(monkeypatch):
    mw = ModelWrapper()
    # mock prepare_input to return 2D array
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))

    class FakeProba:
        def predict_proba(self, X):
            return np.array([[0.3, 0.7]])

    mw.model = FakeProba()

    res = mw.predict({"Alter [J]": 45})
    assert hasattr(res, "__iter__")
    assert float(res[0]) == pytest.approx(0.7)


def test_predict_with_decision_function(monkeypatch):
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[0.0]]))

    class FakeDecision:
        def decision_function(self, X):
            return np.array([0.0])

    mw.model = FakeDecision()

    res = mw.predict({"Alter [J]": 45})
    assert float(res[0]) == pytest.approx(0.5)


def test_predict_regressor_path(monkeypatch):
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[1.0]]))

    class FakeReg:
        def predict(self, X):
            return [0.42]

    mw.model = FakeReg()
    import sys
    import types

    sklearn_base = types.SimpleNamespace(is_regressor=lambda x: True)
    sys.modules["sklearn.base"] = sklearn_base
    try:
        res = mw.predict({"Alter [J]": 45})
        assert float(res[0]) == pytest.approx(0.42)
    finally:
        del sys.modules["sklearn.base"]


def test_predict_value_error_hints(monkeypatch):
    mw = ModelWrapper()
    # make prepare_input return a 1x2 array, but model expects 3 features
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))
    fake_model = MagicMock()

    def raise_value_error(X):
        raise ValueError("feature mismatch")

    fake_model.predict_proba.side_effect = raise_value_error
    fake_model.n_features_in_ = 3
    mw.model = fake_model

    with pytest.raises(ValueError) as exc:
        mw.predict({"Alter [J]": 45})
    assert "expects 3 features" in str(exc.value) or "input has" in str(exc.value)
