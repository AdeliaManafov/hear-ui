"""Tests for app.api.routes.predict – predict endpoint and helper functions."""

from __future__ import annotations

from unittest.mock import MagicMock

import numpy as np
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.predict import (
    PatientData,
    _interpret_prediction,
    compute_prediction_and_explanation,
    router,
)

# ===========================================================================
# PatientData model
# ===========================================================================


class TestPatientDataModel:
    def test_extra_fields_allowed(self):
        data = PatientData.model_validate({"Alter [J]": 45, "extra_field": "hello"})
        assert data.alter == 45

    def test_all_none_by_default(self):
        data = PatientData()
        assert data.alter is None
        assert data.geschlecht is None

    def test_model_dump_by_alias(self):
        data = PatientData.model_validate({"Alter [J]": 50, "Geschlecht": "m"})
        d = data.model_dump(by_alias=True)
        assert d["Alter [J]"] == 50
        assert d["Geschlecht"] == "m"

    def test_populate_by_name(self):
        data = PatientData(alter=30, geschlecht="w")
        assert data.alter == 30
        assert data.geschlecht == "w"


# ===========================================================================
# _interpret_prediction
# ===========================================================================


class TestInterpretPrediction:
    def test_very_high(self):
        r = _interpret_prediction(0.85, 0.05)
        assert r["level"] == "very_high"
        assert r["model_confidence"] == "high"  # uncertainty 0.05 <= 0.10

    def test_high(self):
        r = _interpret_prediction(0.65, 0.15)
        assert r["level"] == "high"
        assert r["model_confidence"] == "moderate"

    def test_moderate(self):
        r = _interpret_prediction(0.45, 0.25)
        assert r["level"] == "moderate"
        assert r["model_confidence"] == "low"

    def test_low(self):
        r = _interpret_prediction(0.25, 0.08)
        assert r["level"] == "low"

    def test_very_low(self):
        r = _interpret_prediction(0.1, 0.05)
        assert r["level"] == "very_low"

    def test_german_fields_present(self):
        r = _interpret_prediction(0.5, 0.1)
        assert "level_de" in r
        assert "description_de" in r
        assert "model_confidence_de" in r
        assert "note_de" in r


# ===========================================================================
# compute_prediction_and_explanation
# ===========================================================================


class TestComputePredictionAndExplanation:
    def test_basic_prediction(self):
        mock_wrapper = MagicMock()
        mock_wrapper.predict.return_value = np.array([0.75])
        mock_wrapper.model = None  # skip SHAP

        result = compute_prediction_and_explanation({"Alter [J]": 50}, mock_wrapper)
        assert result["prediction"] == pytest.approx(0.75)

    def test_prediction_scalar(self):
        mock_wrapper = MagicMock()
        mock_wrapper.predict.return_value = 0.6
        mock_wrapper.model = None
        result = compute_prediction_and_explanation({}, mock_wrapper)
        assert result["prediction"] == pytest.approx(0.6)

    def test_prediction_error_raises(self):
        mock_wrapper = MagicMock()
        mock_wrapper.predict.side_effect = RuntimeError("kaboom")
        with pytest.raises(RuntimeError, match="kaboom"):
            compute_prediction_and_explanation({}, mock_wrapper)

    def test_shap_failure_returns_empty_explanation(self):
        """When SHAP fails, prediction still works, explanation is empty."""
        mock_wrapper = MagicMock()
        mock_wrapper.predict.return_value = np.array([0.55])
        mock_wrapper.model = MagicMock()  # triggers SHAP attempt
        mock_wrapper.prepare_input.side_effect = Exception("shap boom")

        result = compute_prediction_and_explanation({}, mock_wrapper)
        assert result["prediction"] == pytest.approx(0.55)
        assert result["explanation"] == {}


# ===========================================================================
# Predict endpoint (integration via TestClient)
# ===========================================================================


def _make_app(model_loaded=True, predict_result=np.array([0.8])):
    """Create a FastAPI app with mocked model_wrapper."""
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")

    mock_wrapper = MagicMock()
    mock_wrapper.is_loaded.return_value = model_loaded
    mock_wrapper.predict.return_value = predict_result
    mock_wrapper.predict_with_confidence.return_value = {
        "prediction": 0.8,
        "confidence_interval": (0.7, 0.9),
        "uncertainty": 0.2,
        "confidence_level": 0.95,
    }
    app.state.model_wrapper = mock_wrapper

    # We need a mock db session dependency

    return app, mock_wrapper


class TestPredictEndpoint:
    @pytest.fixture()
    def client(self):
        app, wrapper = _make_app()
        # Override the DB dependency to return a mock session
        from app.api import deps

        mock_session = MagicMock()

        def override_session():
            return mock_session

        app.dependency_overrides[deps.get_db] = override_session
        return TestClient(app), wrapper

    def test_predict_success(self, client):
        tc, wrapper = client
        resp = tc.post("/api/v1/predict/", json={"Alter [J]": 45, "Geschlecht": "w"})
        assert resp.status_code == 200
        data = resp.json()
        assert "prediction" in data
        assert data["prediction"] == pytest.approx(0.8)

    def test_predict_model_not_loaded(self):
        app, _ = _make_app(model_loaded=False)
        from app.api import deps

        app.dependency_overrides[deps.get_db] = lambda: MagicMock()
        tc = TestClient(app)
        resp = tc.post("/api/v1/predict/", json={"Alter [J]": 30})
        assert resp.status_code == 503

    def test_predict_with_confidence(self, client):
        tc, wrapper = client
        resp = tc.post(
            "/api/v1/predict/",
            json={"Alter [J]": 45},
            params={"include_confidence": True},
        )
        data = resp.json()
        assert "confidence_interval" in data
        assert "uncertainty" in data
        assert "interpretation" in data

    def test_predict_with_persist(self, client):
        tc, wrapper = client
        resp = tc.post(
            "/api/v1/predict/",
            json={"Alter [J]": 45},
            params={"persist": True},
        )
        data = resp.json()
        assert "persisted" in data

    def test_predict_exception(self):
        app, wrapper = _make_app()
        wrapper.predict.side_effect = Exception("model error")
        from app.api import deps

        app.dependency_overrides[deps.get_db] = lambda: MagicMock()
        tc = TestClient(app)
        resp = tc.post("/api/v1/predict/", json={"Alter [J]": 45})
        assert resp.status_code == 500
