"""Tests for /predict/simple endpoint."""

from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.predict import router


@pytest.fixture
def app_with_simple_predict():
    """Create test app with predict router and mocked model wrapper."""
    app = FastAPI()
    app.include_router(router)

    # Mock model wrapper
    mock_wrapper = MagicMock()
    mock_wrapper.is_loaded.return_value = True
    mock_wrapper.predict.return_value = [0.75]  # Return as array

    app.state.model_wrapper = mock_wrapper

    return app, mock_wrapper


class TestPredictSimple:
    """Tests for the /predict/simple endpoint."""

    def test_predict_simple_returns_only_prediction(self, app_with_simple_predict):
        """Test that /predict/simple returns only prediction without explanation."""
        app, mock_wrapper = app_with_simple_predict
        client = TestClient(app)

        response = client.post(
            "/predict/simple",
            json={
                "Alter [J]": 45,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Should only have prediction, no explanation
        assert "prediction" in data
        assert data["prediction"] == pytest.approx(0.75)
        assert "explanation" not in data
        assert "feature_importance" not in data

    def test_predict_simple_uses_canonical_wrapper(self, app_with_simple_predict):
        """Test that /predict/simple uses the canonical model_wrapper."""
        app, mock_wrapper = app_with_simple_predict
        client = TestClient(app)

        client.post(
            "/predict/simple",
            json={"Alter [J]": 50, "Geschlecht": "m"},
        )

        # Verify wrapper.predict was called with clip=True
        mock_wrapper.predict.assert_called_once()
        call_args = mock_wrapper.predict.call_args
        assert call_args[1]["clip"] is True

    def test_predict_simple_with_minimal_data(self, app_with_simple_predict):
        """Test /predict/simple with minimal patient data."""
        app, mock_wrapper = app_with_simple_predict
        client = TestClient(app)

        mock_wrapper.predict.return_value = [0.60]

        response = client.post(
            "/predict/simple",
            json={"Alter [J]": 30},
        )

        assert response.status_code == 200
        assert response.json()["prediction"] == pytest.approx(0.60)

    def test_predict_simple_model_not_loaded(self):
        """Test /predict/simple returns 503 when model not loaded."""
        app = FastAPI()
        app.include_router(router)

        mock_wrapper = MagicMock()
        mock_wrapper.is_loaded.return_value = False
        app.state.model_wrapper = mock_wrapper

        client = TestClient(app)

        response = client.post(
            "/predict/simple",
            json={"Alter [J]": 45},
        )

        assert response.status_code == 503
        assert "Model not loaded" in response.json()["detail"]

    def test_predict_simple_handles_scalar_response(self, app_with_simple_predict):
        """Test that /predict/simple handles scalar predictions."""
        app, mock_wrapper = app_with_simple_predict
        client = TestClient(app)

        # Mock returns scalar instead of array
        mock_wrapper.predict.return_value = 0.88

        response = client.post(
            "/predict/simple",
            json={"Alter [J]": 40, "Geschlecht": "w"},
        )

        assert response.status_code == 200
        assert response.json()["prediction"] == pytest.approx(0.88)

    def test_predict_simple_error_handling(self, app_with_simple_predict):
        """Test /predict/simple handles prediction errors."""
        app, mock_wrapper = app_with_simple_predict
        client = TestClient(app)

        mock_wrapper.predict.side_effect = ValueError("Prediction error")

        response = client.post(
            "/predict/simple",
            json={"Alter [J]": 45},
        )

        assert response.status_code == 500
        assert "Prediction failed" in response.json()["detail"]
