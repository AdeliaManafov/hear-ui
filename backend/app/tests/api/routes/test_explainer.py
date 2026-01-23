"""Tests for Explainer API routes."""

from fastapi.testclient import TestClient

from app.core.config import settings


class TestExplainerEndpoint:
    """Tests for GET /patients/{patient_id}/explainer endpoint."""

    def test_explain_returns_valid_response(self, client: TestClient, test_patient):
        """Test that explain endpoint returns valid SHAP response."""
        # Use test_patient fixture which creates a patient in DB
        patient_id = test_patient.id

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient_id}/explainer")

        # Either 200 (success) or 503 (model not loaded)
        assert resp.status_code in [200, 503]

        if resp.status_code == 200:
            data = resp.json()
            assert "prediction" in data
            assert "feature_importance" in data
            assert "shap_values" in data
            assert "base_value" in data
            assert "top_features" in data

    def test_explain_with_minimal_data(self, client: TestClient, db):
        """Test explain with minimal required fields."""
        from app import crud
        from app.models import PatientCreate

        # Create patient with minimal data
        patient_in = PatientCreate(
            input_features={"Alter [J]": 50, "Geschlecht": "m"},
            display_name="Test Minimal",
        )
        patient = crud.create_patient(session=db, patient_in=patient_in)
        db.commit()
        db.refresh(patient)

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient.id}/explainer")
        # Should accept minimal data (uses defaults)
        assert resp.status_code in [200, 422, 503]

    def test_explain_with_include_plot_false(self, client: TestClient, test_patient):
        """Test explain endpoint (plot is always None in new implementation)."""
        patient_id = test_patient.id

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient_id}/explainer")

        if resp.status_code == 200:
            data = resp.json()
            # New implementation doesn't generate plots
            assert data.get("plot_base64") is None

    def test_explain_top_features_structure(self, client: TestClient, test_patient):
        """Test that top_features has correct structure."""
        patient_id = test_patient.id

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient_id}/explainer")

        if resp.status_code == 200:
            data = resp.json()
            top_features = data.get("top_features", [])

            if top_features:
                for feat in top_features:
                    assert "feature" in feat
                    assert "importance" in feat


class TestExplainerEdgeCases:
    """Edge case tests for explainer."""

    def test_explain_with_extreme_age(self, client: TestClient, db):
        """Test with extreme age values."""
        from app import crud
        from app.models import PatientCreate

        patient_in = PatientCreate(
            input_features={"Alter [J]": 95, "Geschlecht": "w"},
            display_name="Test Extreme Age",
        )
        patient = crud.create_patient(session=db, patient_in=patient_in)
        db.commit()
        db.refresh(patient)

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient.id}/explainer")
        assert resp.status_code in [200, 503]

    def test_explain_with_young_patient(self, client: TestClient, db):
        """Test with young patient."""
        from app import crud
        from app.models import PatientCreate

        patient_in = PatientCreate(
            input_features={"Alter [J]": 5, "Geschlecht": "m"},
            display_name="Test Young",
        )
        patient = crud.create_patient(session=db, patient_in=patient_in)
        db.commit()
        db.refresh(patient)

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient.id}/explainer")
        assert resp.status_code in [200, 503]

    def test_explain_with_all_unknown_values(self, client: TestClient, db):
        """Test with all unknown categorical values."""
        from app import crud
        from app.models import PatientCreate

        patient_in = PatientCreate(
            input_features={
                "Alter [J]": 50,
                "Geschlecht": "d",
                "Primäre Sprache": "Andere",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
            },
            display_name="Test Unknown Values",
        )
        patient = crud.create_patient(session=db, patient_in=patient_in)
        db.commit()
        db.refresh(patient)

        resp = client.get(f"{settings.API_V1_STR}/patients/{patient.id}/explainer")
        assert resp.status_code in [200, 503]
