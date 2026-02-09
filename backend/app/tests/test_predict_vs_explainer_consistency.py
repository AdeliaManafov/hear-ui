"""Test to verify /predict/simple and /explainer/explain return consistent predictions."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestPredictionConsistency:
    """Verify prediction consistency between endpoints."""

    def test_predict_vs_explainer_minimal(self):
        """Test with minimal data - both should return same prediction."""
        data = {"Alter [J]": 45}

        # Test /predict/simple
        resp1 = client.post("/api/v1/predict/simple", json=data)
        assert resp1.status_code == 200
        pred1 = resp1.json()["prediction"]
        print(f"\n/predict/simple: {pred1:.6f} ({pred1*100:.2f}%)")

        # Test /explainer/explain
        resp2 = client.post(
            "/api/v1/explainer/explain?method=shap&include_plot=false", json=data
        )
        assert resp2.status_code == 200
        pred2 = resp2.json()["prediction"]
        print(f"/explainer/explain: {pred2:.6f} ({pred2*100:.2f}%)")

        # They should match (within floating point precision)
        assert abs(pred1 - pred2) < 0.001, f"Predictions differ: {pred1} vs {pred2}"
        print(f"✓ Predictions match!")

    def test_predict_vs_explainer_full(self):
        """Test with full data - both should return same prediction."""
        data = {
            "Alter [J]": 65,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Symptome präoperativ.Tinnitus...": "nein",
            "Behandlung/OP.CI Implantation": "Cochlear",
        }

        # Test /predict/simple
        resp1 = client.post("/api/v1/predict/simple", json=data)
        assert resp1.status_code == 200
        pred1 = resp1.json()["prediction"]
        print(f"\n/predict/simple:    {pred1:.6f} ({pred1*100:.2f}%)")

        # Test /explainer/explain
        resp2 = client.post(
            "/api/v1/explainer/explain?method=shap&include_plot=false", json=data
        )
        assert resp2.status_code == 200
        result = resp2.json()
        pred2 = result["prediction"]
        print(f"/explainer/explain: {pred2:.6f} ({pred2*100:.2f}%)")

        # Show feature importance
        if "feature_importance" in result:
            features = sorted(
                result["feature_importance"].items(), key=lambda x: abs(x[1]), reverse=True
            )[:5]
            print("\nTop 5 features by importance:")
            for feat, importance in features:
                print(f"  {feat[:60]:60s} {importance:+8.3f}")

        # They should match
        assert abs(pred1 - pred2) < 0.001, f"Predictions differ: {pred1} vs {pred2}"
        print(f"\n✓ Predictions match!")

    def test_predict_vs_explainer_male(self):
        """Test with male patient - edge case check."""
        data = {
            "Alter [J]": 45,
            "Geschlecht": "m",
            "Symptome präoperativ.Tinnitus...": "ja",
        }

        # Test /predict/simple
        resp1 = client.post("/api/v1/predict/simple", json=data)
        assert resp1.status_code == 200
        pred1 = resp1.json()["prediction"]
        print(f"\n/predict/simple: {pred1:.6f} ({pred1*100:.2f}%)")

        # Test /explainer/explain
        resp2 = client.post(
            "/api/v1/explainer/explain?method=shap&include_plot=false", json=data
        )
        assert resp2.status_code == 200
        pred2 = resp2.json()["prediction"]
        print(f"/explainer/explain: {pred2:.6f} ({pred2*100:.2f}%)")

        # They should match
        assert abs(pred1 - pred2) < 0.001, f"Predictions differ: {pred1} vs {pred2}"
        print(f"✓ Predictions match!")
