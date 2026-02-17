import numpy as np
from fastapi.testclient import TestClient

from app.main import app


class DummyModel:
    def __init__(self, n_features: int = 68, value: float = 0.42):
        # simple linear model stub with coef_ and intercept_
        self.coef_ = np.zeros((1, n_features))
        # set one small non-zero coefficient for determinism
        self.coef_[0, 0] = 0.0
        self.intercept_ = np.array([0.0])
        self._pred = value

    def predict(self, X):
        # Return constant prediction for testing
        return np.array([self._pred])


class DummyWrapper:
    def __init__(self, n_features: int = 68, prediction_value: float = 0.42):
        self.model = DummyModel(n_features=n_features)
        self._n = n_features
        self._pred = float(prediction_value)
        # Add model_adapter to satisfy new architecture
        from unittest.mock import MagicMock

        self.model_adapter = MagicMock()
        self.model_adapter.predict_proba.return_value = np.array([self._pred])

    def is_loaded(self):
        return True

    def predict(self, patient_dict, clip: bool = True):
        # ignore input and return deterministic value
        # clip parameter accepted for API compatibility
        return [self._pred]

    def prepare_input(self, patient_dict):
        # return a 1 x n_features numpy array of zeros
        return np.zeros((1, self._n))

    def get_feature_names(self):
        # Return dummy feature names
        return [f"feature_{i}" for i in range(self._n)]


def test_predict_and_explainer_consistency():
    # Attach dummy wrapper to app state so endpoints use it
    app.state.model_wrapper = DummyWrapper()

    client = TestClient(app)

    payload_predict = {"Alter [J]": 45, "Geschlecht": "w", "Primäre Sprache": "Deutsch"}

    # Call predict endpoint
    r1 = client.post("/api/v1/predict/", json=payload_predict)
    assert r1.status_code == 200, r1.text
    pred1 = r1.json().get("prediction")

    # Call explainer endpoint (use same input but include_plot False to keep response small)
    payload_explainer = {
        "Alter [J]": 45,
        "Geschlecht": "w",
        "Primäre Sprache": "Deutsch",
        "include_plot": False,
    }

    r2 = client.post("/api/v1/explainer/explain", json=payload_explainer)
    assert r2.status_code == 200, r2.text
    pred2 = r2.json().get("prediction")

    # Both endpoints should return the same prediction value
    assert pred1 == pred2
