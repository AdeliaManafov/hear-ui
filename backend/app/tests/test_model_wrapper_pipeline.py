"""Tests for ModelWrapper pipeline scenarios."""
import sys
from unittest.mock import MagicMock

import numpy as np

from app.core.model_wrapper import ModelWrapper


def test_pipeline_predict_proba():
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))

    fake_pipeline = MagicMock()
    fake_pipeline.predict_proba.return_value = np.array([[0.2, 0.8]])

    # simulate sklearn Pipeline forwarding predict_proba
    mw.model = fake_pipeline

    res = mw.predict({"Alter [J]": 45})
    assert float(res[0]) == 0.8


def test_pipeline_regressor_final_estimator():
    mw = ModelWrapper()
    mw.prepare_input = MagicMock(return_value=np.array([[1.0, 2.0]]))

    # Create a pipeline-like object without predict_proba, but with steps
    class FakeFinal:
        def predict(self, X):
            return [0.33]

    class FakePipeline:
        def __init__(self, steps):
            self.steps = steps

        def predict(self, X):
            # delegate to final estimator predict
            return self.steps[-1][1].predict(X)

    fake_pipeline = FakePipeline([("prep", MagicMock()), ("est", FakeFinal())])

    mw.model = fake_pipeline

    # Inject sklearn.base.is_regressor to return True so branch triggers
    import types
    sklearn_base = types.SimpleNamespace(is_regressor=lambda x: True)
    sys.modules['sklearn.base'] = sklearn_base

    try:
        res = mw.predict({"Alter [J]": 45})
        assert float(res[0]) == 0.33
    finally:
        del sys.modules['sklearn.base']
