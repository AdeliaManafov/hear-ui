"""Tests for explainer API endpoints with SHAP mocking."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def mock_model_wrapper():
    """Mock the model wrapper to avoid real model loading."""
    with patch("app.main.app") as mock_app:
        mock_wrapper = MagicMock()
        mock_wrapper.is_loaded.return_value = True
        mock_wrapper.model = MagicMock()
        mock_wrapper.model.coef_ = [[0.1, 0.2, 0.3]]  # Mock linear model coefficients
        mock_wrapper.model.intercept_ = [0.5]
        mock_wrapper.prepare_input.return_value = MagicMock()
        mock_wrapper.prepare_input.return_value.values = [[1.0, 2.0, 3.0]]
        mock_wrapper.predict.return_value = [0.75]

        mock_app.state.model_wrapper = mock_wrapper
        yield mock_wrapper


def test_explainer_model_not_loaded():
    """Test explainer returns 503 when model is not loaded."""
    with patch("app.main.app") as mock_app:
        mock_wrapper = MagicMock()
        mock_wrapper.is_loaded.return_value = False
        mock_app.state.model_wrapper = mock_wrapper

        payload = {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch"
        }

        response = client.post("/api/v1/explainer/explain", json=payload)

        assert response.status_code == 503
        assert "not loaded" in response.json()["detail"].lower()


def test_explainer_with_valid_input(mock_model_wrapper):
    """Test explainer with valid patient data."""
    with patch("app.core.preprocessor.EXPECTED_FEATURES", ["age", "gender", "language"]):
        payload = {
            "Alter [J]": 50,
            "Geschlecht": "m",
            "Primäre Sprache": "Deutsch",
            "include_plot": False
        }

        response = client.post("/api/v1/explainer/explain", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "feature_importance" in data
        assert "shap_values" in data
        assert "base_value" in data
        assert isinstance(data["prediction"], float)
        assert isinstance(data["feature_importance"], dict)


def test_explainer_returns_top_features(mock_model_wrapper):
    """Test that explainer returns top features list."""
    with patch("app.core.preprocessor.EXPECTED_FEATURES", ["age", "gender", "language"]):
        payload = {
            "Alter [J]": 60,
            "Geschlecht": "w",
            "include_plot": False
        }

        response = client.post("/api/v1/explainer/explain", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "top_features" in data
        assert isinstance(data["top_features"], list)
        if len(data["top_features"]) > 0:
            assert "feature" in data["top_features"][0]
            assert "importance" in data["top_features"][0]


def test_explainer_with_minimal_data(mock_model_wrapper):
    """Test explainer with minimal required fields."""
    payload = {
        "Alter [J]": 45,
        "Geschlecht": "w"
    }

    response = client.post("/api/v1/explainer/explain", json=payload)

    # Should use defaults for missing fields
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 0.75  # From mock


def test_explainer_with_all_fields(mock_model_wrapper):
    """Test explainer with all available patient fields."""
    payload = {
        "Alter [J]": 55,
        "Geschlecht": "m",
        "Primäre Sprache": "Deutsch",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
        "Diagnose.Höranamnese.Ursache....Ursache...": "Genetisch",
        "Symptome präoperativ.Tinnitus...": "ja",
        "Behandlung/OP.CI Implantation": "Cochlear Nucleus",
        "include_plot": False
    }

    response = client.post("/api/v1/explainer/explain", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 0.75


def test_explainer_plot_generation_disabled(mock_model_wrapper):
    """Test that plot generation is skipped when include_plot=False."""
    payload = {
        "Alter [J]": 50,
        "Geschlecht": "w",
        "include_plot": False
    }

    response = client.post("/api/v1/explainer/explain", json=payload)

    assert response.status_code == 200
    data = response.json()
    # Plot should be None when disabled
    assert data.get("plot_base64") is None


def test_explainer_handles_preprocessing_error():
    """Test explainer handles errors in preprocessing gracefully."""
    with patch("app.main.app") as mock_app:
        mock_wrapper = MagicMock()
        mock_wrapper.is_loaded.return_value = True
        mock_wrapper.prepare_input.side_effect = ValueError("Preprocessing failed")
        mock_app.state.model_wrapper = mock_wrapper

        payload = {
            "Alter [J]": -999,  # Invalid age
            "Geschlecht": "invalid"
        }

        response = client.post("/api/v1/explainer/explain", json=payload)

        # Should return 500 with error detail
        assert response.status_code == 500
        assert "failed" in response.json()["detail"].lower()


def test_explainer_handles_prediction_error():
    """Test explainer handles prediction errors gracefully."""
    with patch("app.main.app") as mock_app:
        mock_wrapper = MagicMock()
        mock_wrapper.is_loaded.return_value = True
        mock_wrapper.prepare_input.return_value = MagicMock()
        mock_wrapper.predict.side_effect = RuntimeError("Model prediction failed")
        mock_app.state.model_wrapper = mock_wrapper

        payload = {
            "Alter [J]": 45,
            "Geschlecht": "w"
        }

        response = client.post("/api/v1/explainer/explain", json=payload)

        assert response.status_code == 500


def test_explainer_feature_importance_structure(mock_model_wrapper):
    """Test that feature importance has correct structure."""
    with patch("app.core.preprocessor.EXPECTED_FEATURES", ["feature_1", "feature_2", "feature_3"]):
        payload = {
            "Alter [J]": 45,
            "Geschlecht": "w"
        }

        response = client.post("/api/v1/explainer/explain", json=payload)

        assert response.status_code == 200
        data = response.json()
        feature_importance = data["feature_importance"]

        # Should be a dict with string keys and numeric values
        assert isinstance(feature_importance, dict)
        for key, value in feature_importance.items():
            assert isinstance(key, str)
            assert isinstance(value, (int, float))


def test_explainer_base_value_is_float(mock_model_wrapper):
    """Test that base_value is always a float."""
    payload = {
        "Alter [J]": 50,
        "Geschlecht": "m"
    }

    response = client.post("/api/v1/explainer/explain", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["base_value"], float)


def test_explainer_shap_values_is_list(mock_model_wrapper):
    """Test that shap_values is a list of floats."""
    payload = {
        "Alter [J]": 45,
        "Geschlecht": "w"
    }

    response = client.post("/api/v1/explainer/explain", json=payload)

    assert response.status_code == 200
    data = response.json()
    shap_values = data["shap_values"]

    assert isinstance(shap_values, list)
    for val in shap_values:
        assert isinstance(val, (int, float))


@pytest.mark.parametrize("age,gender", [
    (25, "m"),
    (45, "w"),
    (65, "m"),
    (75, "w"),
])
def test_explainer_various_demographics(mock_model_wrapper, age, gender):
    """Test explainer with various demographic combinations."""
    payload = {
        "Alter [J]": age,
        "Geschlecht": gender
    }

    response = client.post("/api/v1/explainer/explain", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "feature_importance" in data
