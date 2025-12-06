"""Tests for utils API routes."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestHealthCheck:
    """Test health check endpoint."""

    def test_health_check_returns_ok(self):
        """Test health check returns status ok."""
        response = client.get("/api/v1/utils/health-check/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestModelInfo:
    """Test model info endpoint."""

    def test_model_info_returns_loaded_status(self):
        """Test model info returns loaded status."""
        response = client.get("/api/v1/utils/model-info/")
        assert response.status_code == 200
        data = response.json()
        assert "loaded" in data
        assert isinstance(data["loaded"], bool)

    def test_model_info_returns_model_type(self):
        """Test model info returns model type."""
        response = client.get("/api/v1/utils/model-info/")
        assert response.status_code == 200
        data = response.json()
        assert "model_type" in data


class TestFeatureNames:
    """Test feature names endpoint."""

    def test_get_feature_names_returns_dict(self):
        """Test get_feature_names returns dictionary."""
        response = client.get("/api/v1/utils/feature-names/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_feature_names_contains_age(self):
        """Test feature names contains age mapping."""
        response = client.get("/api/v1/utils/feature-names/")
        data = response.json()
        # Should contain age feature
        assert any("Alter" in key for key in data.keys())

    def test_feature_names_has_german_labels(self):
        """Test feature names have German labels as values."""
        response = client.get("/api/v1/utils/feature-names/")
        data = response.json()
        # Values should be in German
        values = list(data.values())
        assert any("Alter" in v or "Geschlecht" in v for v in values)


class TestFeatureCategories:
    """Test feature categories endpoint."""

    def test_get_feature_categories_returns_dict(self):
        """Test get_feature_categories returns dictionary."""
        response = client.get("/api/v1/utils/feature-categories/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_categories_contains_demographics(self):
        """Test categories contains demographics section."""
        response = client.get("/api/v1/utils/feature-categories/")
        data = response.json()
        assert "Demographische Daten" in data

    def test_categories_contains_diagnosis(self):
        """Test categories contains diagnosis sections."""
        response = client.get("/api/v1/utils/feature-categories/")
        data = response.json()
        categories = list(data.keys())
        assert any("Diagnose" in cat for cat in categories)

    def test_categories_values_are_lists(self):
        """Test category values are lists of feature names."""
        response = client.get("/api/v1/utils/feature-categories/")
        data = response.json()
        for category, features in data.items():
            assert isinstance(features, list)
            assert all(isinstance(f, str) for f in features)

    def test_categories_has_treatment_section(self):
        """Test categories has treatment section."""
        response = client.get("/api/v1/utils/feature-categories/")
        data = response.json()
        assert "Behandlung" in data
