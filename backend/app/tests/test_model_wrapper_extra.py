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

    # Mock the adapter
    mock_adapter = MagicMock()
    mock_adapter.predict_proba.return_value = np.array([[0.3, 0.7]])
    mw.model_adapter = mock_adapter
    mw.model = MagicMock()  # Need some model set to pass the is None check

    res = mw.predict({"Alter [J]": 45})
    assert hasattr(res, "__iter__")
    assert float(res[0]) == pytest.approx(0.7)


def test_predict_with_decision_function(monkeypatch):
    from scipy.special import expit
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[0.0]]))

    # Mock the adapter to return sigmoid of decision function
    mock_adapter = MagicMock()
    mock_adapter.predict_proba.return_value = expit(np.array([0.0]))
    mw.model_adapter = mock_adapter
    mw.model = MagicMock()

    res = mw.predict({"Alter [J]": 45})
    assert float(res[0]) == pytest.approx(0.5)


def test_predict_regressor_path(monkeypatch):
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[1.0]]))

    # Mock adapter to return regression value directly
    mock_adapter = MagicMock()
    mock_adapter.predict_proba.return_value = np.array([0.42])
    mw.model_adapter = mock_adapter
    mw.model = MagicMock()


def test_predict_value_error_hints(monkeypatch):
    mw = ModelWrapper()
    # make prepare_input return a 1x2 array, but adapter raises error
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))

    mock_adapter = MagicMock()
    def raise_value_error(X):
        raise ValueError("feature mismatch: expects 3 features but input has 2")
    mock_adapter.predict_proba.side_effect = raise_value_error

    mw.model_adapter = mock_adapter
    mw.model = MagicMock()

    with pytest.raises(ValueError) as exc:
        mw.predict({"Alter [J]": 45})
    assert "feature" in str(exc.value).lower()
