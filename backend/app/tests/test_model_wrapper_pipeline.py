"""Tests for ModelWrapper pipeline scenarios."""

import sys
from unittest.mock import MagicMock

import numpy as np

from app.core.model_wrapper import ModelWrapper


def test_pipeline_predict_proba():
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))

    # Mock the adapter to return predictions
    mock_adapter = MagicMock()
    mock_adapter.predict_proba.return_value = np.array([[0.2, 0.8]])
    mw.model_adapter = mock_adapter
    mw.model = MagicMock()  # Need some model set

    res = mw.predict({"Alter [J]": 45})
    assert float(res[0]) == 0.8


def test_pipeline_regressor_final_estimator():
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))

    # Mock adapter to return regression value
    mock_adapter = MagicMock()
    mock_adapter.predict_proba.return_value = np.array([0.33])
    mw.model_adapter = mock_adapter
    mw.model = MagicMock()

    res = mw.predict({"Alter [J]": 45})
    assert float(res[0]) == 0.33
