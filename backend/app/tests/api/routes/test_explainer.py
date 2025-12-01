"""Tests for Explainer API routes."""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.core.config import settings


class TestExplainerEndpoint:
    """Tests for POST /explainer/explain endpoint."""

    def test_explain_returns_valid_response(self, client: TestClient):
        """Test that explain endpoint returns valid SHAP response."""
        payload = {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
            "Symptome präoperativ.Tinnitus...": "ja",
            "Behandlung/OP.CI Implantation": "Cochlear",
        }
        
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        
        # Either 200 (success) or 503 (model not loaded)
        assert resp.status_code in [200, 503]
        
        if resp.status_code == 200:
            data = resp.json()
            assert "prediction" in data
            assert "feature_importance" in data
            assert "shap_values" in data
            assert "base_value" in data
            assert "top_features" in data

    def test_explain_with_minimal_data(self, client: TestClient):
        """Test explain with minimal required fields."""
        payload = {
            "age": 50,
            "gender": "m",
        }
        
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        # Should accept minimal data (uses defaults)
        assert resp.status_code in [200, 422, 503]

    def test_explain_with_include_plot_false(self, client: TestClient):
        """Test explain with plot disabled."""
        payload = {
            "Alter [J]": 55,
            "Geschlecht": "m",
            "include_plot": False,
        }
        
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        
        if resp.status_code == 200:
            data = resp.json()
            assert data.get("plot_base64") is None

    def test_explain_top_features_structure(self, client: TestClient):
        """Test that top_features has correct structure."""
        payload = {
            "Alter [J]": 45,
            "Geschlecht": "w",
        }
        
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        
        if resp.status_code == 200:
            data = resp.json()
            top_features = data.get("top_features", [])
            
            if top_features:
                for feat in top_features:
                    assert "feature" in feat
                    assert "importance" in feat


class TestExplainerEdgeCases:
    """Edge case tests for explainer."""

    def test_explain_with_extreme_age(self, client: TestClient):
        """Test with extreme age values."""
        payload = {"Alter [J]": 95, "Geschlecht": "w"}
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        assert resp.status_code in [200, 503]

    def test_explain_with_young_patient(self, client: TestClient):
        """Test with young patient."""
        payload = {"Alter [J]": 5, "Geschlecht": "m"}
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        assert resp.status_code in [200, 503]

    def test_explain_with_all_unknown_values(self, client: TestClient):
        """Test with all unknown categorical values."""
        payload = {
            "Alter [J]": 50,
            "Geschlecht": "d",
            "Primäre Sprache": "Andere",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
        }
        resp = client.post(f"{settings.API_V1_STR}/explainer/explain", json=payload)
        assert resp.status_code in [200, 503]
