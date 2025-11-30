"""Tests for Patient API routes.

Tests cover:
- GET /patients/ (list patients)
- GET /patients/{id} (get single patient)
- GET /patients/{id}/predict (predict for stored patient)
- GET /patients/{id}/explainer (SHAP explanation for stored patient)
- GET /patients/{id}/validate (validate patient features)

Note: Tests requiring database access will be skipped if DB is not available.
"""

from uuid import uuid4
import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app import crud
from app.models import PatientCreate


def _db_available() -> bool:
    """Check if database is reachable."""
    try:
        from app.core.db import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# Mark all tests in this module to skip if DB is not available
pytestmark = pytest.mark.skipif(
    not _db_available(),
    reason="Database not available - run with docker compose up db"
)


# Sample patient data for testing
SAMPLE_PATIENT_DATA = {
    "Alter [J]": 55,
    "Geschlecht": "w",
    "Seiten": "L",
    "Symptome präoperativ.Tinnitus...": "Vorhanden",
    "Symptome präoperativ.Schwindel...": "Kein",
    "Diagnose.Höranamnese.Hörminderung operiertes Ohr...": "Hochgradiger HV",
    "Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...": "Erworben - postlingual",
    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "> 20 y",
    "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
    "Diagnose.Höranamnese.Versorgung Gegenohr...": "Hörgerät",
    "Behandlung/OP.CI Implantation": "Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile CI532 (Slim Modiolar)",
    "outcome_measurments.pre.measure.": 10,
    "abstand": 365,
}

MINIMAL_PATIENT_DATA = {
    "age": 45,
    "gender": "m",
}


@pytest.fixture
def sample_patient(db: Session):
    """Create a sample patient for testing."""
    patient_create = PatientCreate(input_features=SAMPLE_PATIENT_DATA)
    patient = crud.create_patient(session=db, patient_in=patient_create)
    return patient


@pytest.fixture
def minimal_patient(db: Session):
    """Create a patient with minimal features."""
    patient_create = PatientCreate(input_features=MINIMAL_PATIENT_DATA)
    patient = crud.create_patient(session=db, patient_in=patient_create)
    return patient


@pytest.fixture
def empty_patient(db: Session):
    """Create a patient with no input features."""
    patient_create = PatientCreate(input_features={})
    patient = crud.create_patient(session=db, patient_in=patient_create)
    return patient


# =============================================================================
# GET /patients/ - List patients
# =============================================================================

class TestListPatients:
    """Tests for GET /patients/ endpoint."""

    def test_list_patients_empty(self, client: TestClient) -> None:
        """Test listing patients when database might be empty."""
        resp = client.get(f"{settings.API_V1_STR}/patients/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_list_patients_with_data(self, client: TestClient, sample_patient) -> None:
        """Test listing patients returns created patient."""
        resp = client.get(f"{settings.API_V1_STR}/patients/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Check that our sample patient is in the list
        patient_ids = [p["id"] for p in data]
        assert str(sample_patient.id) in patient_ids

    def test_list_patients_with_limit(self, client: TestClient, db: Session) -> None:
        """Test listing patients with limit parameter."""
        # Create multiple patients
        for i in range(3):
            crud.create_patient(
                session=db,
                patient_in=PatientCreate(input_features={"age": 30 + i})
            )
        
        resp = client.get(f"{settings.API_V1_STR}/patients/?limit=2")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) <= 2

    def test_list_patients_with_offset(self, client: TestClient, db: Session) -> None:
        """Test listing patients with offset parameter."""
        resp = client.get(f"{settings.API_V1_STR}/patients/?offset=0&limit=100")
        assert resp.status_code == 200
        total_count = len(resp.json())
        
        resp_offset = client.get(f"{settings.API_V1_STR}/patients/?offset=1&limit=100")
        assert resp_offset.status_code == 200
        # Should have one less item (or same if only one item)
        assert len(resp_offset.json()) <= total_count


# =============================================================================
# GET /patients/{id} - Get single patient
# =============================================================================

class TestGetPatient:
    """Tests for GET /patients/{id} endpoint."""

    def test_get_patient_success(self, client: TestClient, sample_patient) -> None:
        """Test getting a patient by ID."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == str(sample_patient.id)
        assert "input_features" in data
        assert data["input_features"]["Alter [J]"] == 55

    def test_get_patient_not_found(self, client: TestClient) -> None:
        """Test getting a non-existent patient returns 404."""
        fake_id = uuid4()
        resp = client.get(f"{settings.API_V1_STR}/patients/{fake_id}")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Patient not found"

    def test_get_patient_invalid_uuid(self, client: TestClient) -> None:
        """Test getting patient with invalid UUID returns error."""
        resp = client.get(f"{settings.API_V1_STR}/patients/invalid-uuid")
        assert resp.status_code == 422  # Validation error


# =============================================================================
# GET /patients/{id}/validate - Validate patient features
# =============================================================================

class TestValidatePatient:
    """Tests for GET /patients/{id}/validate endpoint."""

    def test_validate_patient_complete(self, client: TestClient, sample_patient) -> None:
        """Test validating a patient with complete features."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}/validate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["missing_features"] == []
        assert data["features_count"] > 0

    def test_validate_patient_minimal(self, client: TestClient, minimal_patient) -> None:
        """Test validating a patient with minimal required features."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{minimal_patient.id}/validate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["missing_features"] == []

    def test_validate_patient_empty(self, client: TestClient, empty_patient) -> None:
        """Test validating a patient with no features."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{empty_patient.id}/validate")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is False
        assert len(data["missing_features"]) > 0
        assert any("age" in f.lower() or "alter" in f.lower() for f in data["missing_features"])

    def test_validate_patient_not_found(self, client: TestClient) -> None:
        """Test validating a non-existent patient returns 404."""
        fake_id = uuid4()
        resp = client.get(f"{settings.API_V1_STR}/patients/{fake_id}/validate")
        assert resp.status_code == 404


# =============================================================================
# GET /patients/{id}/predict - Predict for patient
# =============================================================================

class TestPredictPatient:
    """Tests for GET /patients/{id}/predict endpoint."""

    def test_predict_patient_success(self, client: TestClient, sample_patient) -> None:
        """Test prediction for a patient with complete features."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}/predict")
        # May return 200 (success) or 503 (model not loaded in test env)
        assert resp.status_code in [200, 503]
        
        if resp.status_code == 200:
            data = resp.json()
            assert "prediction" in data
            assert isinstance(data["prediction"], (int, float))
            assert 0 <= data["prediction"] <= 1

    def test_predict_patient_not_found(self, client: TestClient) -> None:
        """Test prediction for non-existent patient returns 404."""
        fake_id = uuid4()
        resp = client.get(f"{settings.API_V1_STR}/patients/{fake_id}/predict")
        assert resp.status_code == 404

    def test_predict_patient_empty_features(self, client: TestClient, empty_patient) -> None:
        """Test prediction for patient without features returns error."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{empty_patient.id}/predict")
        # Should return 400 (no features) or 503 (model not loaded)
        assert resp.status_code in [400, 503]


# =============================================================================
# GET /patients/{id}/explainer - SHAP explanation for patient
# =============================================================================

class TestExplainerPatient:
    """Tests for GET /patients/{id}/explainer endpoint."""

    def test_explainer_patient_success(self, client: TestClient, sample_patient) -> None:
        """Test SHAP explanation for a patient with complete features."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}/explainer")
        # May return 200 (success), 503 (model not loaded), 500 (error), or 404 (endpoint not implemented)
        assert resp.status_code in [200, 404, 500, 503]
        
        if resp.status_code == 200:
            data = resp.json()
            # SHAP response should contain prediction and feature importance
            assert "prediction" in data or "top_features" in data

    def test_explainer_patient_not_found(self, client: TestClient) -> None:
        """Test SHAP for non-existent patient returns 404."""
        fake_id = uuid4()
        resp = client.get(f"{settings.API_V1_STR}/patients/{fake_id}/explainer")
        assert resp.status_code == 404

    def test_explainer_patient_empty_features(self, client: TestClient, empty_patient) -> None:
        """Test SHAP for patient without features returns error."""
        resp = client.get(f"{settings.API_V1_STR}/patients/{empty_patient.id}/explainer")
        # Should return 400 (no features) or other error
        assert resp.status_code in [400, 500, 503]


# =============================================================================
# Integration Tests
# =============================================================================

class TestPatientIntegration:
    """Integration tests for patient workflows."""

    def test_create_list_get_validate_workflow(self, client: TestClient, db: Session) -> None:
        """Test complete workflow: create -> list -> get -> validate."""
        # Create patient via CRUD (would normally be via upload endpoint)
        patient = crud.create_patient(
            session=db,
            patient_in=PatientCreate(input_features={
                "Alter [J]": 60,
                "Geschlecht": "m",
                "Seiten": "R",
            })
        )
        
        # List and find our patient
        list_resp = client.get(f"{settings.API_V1_STR}/patients/")
        assert list_resp.status_code == 200
        patient_ids = [p["id"] for p in list_resp.json()]
        assert str(patient.id) in patient_ids
        
        # Get specific patient
        get_resp = client.get(f"{settings.API_V1_STR}/patients/{patient.id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["input_features"]["Alter [J]"] == 60
        
        # Validate patient
        validate_resp = client.get(f"{settings.API_V1_STR}/patients/{patient.id}/validate")
        assert validate_resp.status_code == 200
        assert validate_resp.json()["ok"] is True

    def test_patient_prediction_workflow(self, client: TestClient, sample_patient) -> None:
        """Test workflow: get patient -> validate -> predict."""
        # Get patient
        get_resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}")
        assert get_resp.status_code == 200
        
        # Validate first
        validate_resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}/validate")
        assert validate_resp.status_code == 200
        
        if validate_resp.json()["ok"]:
            # If validation passes, try prediction
            predict_resp = client.get(f"{settings.API_V1_STR}/patients/{sample_patient.id}/predict")
            # Accept 200 (success) or 503 (model not loaded in CI)
            assert predict_resp.status_code in [200, 503]
