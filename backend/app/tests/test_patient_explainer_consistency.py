"""Test that /patients/{id}/explainer and /predict/simple return same predictions."""

from uuid import uuid4


class TestPatientExplainerConsistency:
    """Verify /patients/{id}/explainer returns same prediction as /predict/simple."""

    def test_explainer_endpoint_clips_predictions(self, client, db):
        """Patient explainer endpoint should clip predictions to [1%, 99%] like /predict/simple."""
        # Create a test patient
        from app.models import Patient

        patient_data = {
            "Alter [J]": 65,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Symptome präoperativ.Tinnitus...": "nein",
            "Behandlung/OP.CI Implantation": "Cochlear",
        }

        patient = Patient(id=uuid4(), input_features=patient_data)
        db.add(patient)
        db.commit()
        db.refresh(patient)

        # Get prediction from /predict/simple
        resp1 = client.post("/api/v1/predict/simple", json=patient_data)
        assert resp1.status_code == 200
        pred1 = resp1.json()["prediction"]

        # Get prediction from /patients/{id}/explainer
        resp2 = client.get(f"/api/v1/patients/{patient.id}/explainer")
        assert resp2.status_code == 200
        data = resp2.json()
        pred2 = data["prediction"]

        # Predictions should match
        assert abs(pred1 - pred2) < 0.001, (
            f"Predictions differ: /predict/simple={pred1:.6f} vs "
            f"/patients/{{id}}/explainer={pred2:.6f}"
        )

        # Both should be clipped to [0.01, 0.99]
        assert 0.01 <= pred1 <= 0.99, f"Prediction {pred1} not clipped correctly"
        assert 0.01 <= pred2 <= 0.99, (
            f"Explainer prediction {pred2} not clipped correctly"
        )

        print(f"\n✓ Both endpoints return {pred1:.4f} ({pred1 * 100:.1f}%)")
        print("✓ Predictions are properly clipped to [1%, 99%]")

    def test_explainer_endpoint_has_feature_importance(self, client, db):
        """Patient explainer endpoint should return feature importance."""
        from app.models import Patient

        patient_data = {
            "Alter [J]": 45,
            "Geschlecht": "m",
        }

        patient = Patient(id=uuid4(), input_features=patient_data)
        db.add(patient)
        db.commit()
        db.refresh(patient)

        # Get explainer response
        resp = client.get(f"/api/v1/patients/{patient.id}/explainer")
        assert resp.status_code == 200
        data = resp.json()

        # Should have all expected fields
        assert "prediction" in data
        assert "feature_importance" in data
        assert "shap_values" in data
        assert "base_value" in data

        # Feature importance should be a dict
        assert isinstance(data["feature_importance"], dict)
        assert len(data["feature_importance"]) > 0

        # Show top features
        features = sorted(
            data["feature_importance"].items(), key=lambda x: abs(x[1]), reverse=True
        )[:3]
        print("\n✓ Top 3 features:")
        for feat, importance in features:
            print(f"  {feat[:50]:50s} {importance:+8.3f}")
