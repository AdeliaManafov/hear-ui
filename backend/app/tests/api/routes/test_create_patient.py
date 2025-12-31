"""Tests for POST /api/v1/patients/ endpoint."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app

client = TestClient(app)


def test_create_patient_with_valid_data(db: Session):
    """Test creating a patient with valid input_features."""
    payload = {
        "input_features": {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch"
        },
        "display_name": "Muster, Anna"
    }

    response = client.post("/api/v1/patients/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert data["input_features"] == payload["input_features"]
    assert data["display_name"] == "Muster, Anna"


def test_create_patient_minimal_fields(db: Session):
    """Test creating a patient with minimal input_features."""
    payload = {
        "input_features": {
            "Alter [J]": 30,
            "Geschlecht": "m"
        }
    }

    response = client.post("/api/v1/patients/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["input_features"]["Alter [J]"] == 30
    assert data["input_features"]["Geschlecht"] == "m"


def test_create_patient_empty_input_features():
    """Test that creating a patient with empty input_features fails."""
    payload = {
        "input_features": {}
    }

    response = client.post("/api/v1/patients/", json=payload)

    assert response.status_code == 400
    assert "input_features is required" in response.json()["detail"]


def test_create_patient_missing_input_features():
    """Test that creating a patient without input_features fails."""
    payload = {
        "display_name": "Test Patient"
    }

    response = client.post("/api/v1/patients/", json=payload)

    # Our validation catches this and returns 400
    assert response.status_code == 400
    assert "input_features" in response.json()["detail"].lower()


def test_create_patient_with_complex_features(db: Session):
    """Test creating a patient with many features."""
    payload = {
        "input_features": {
            "Alter [J]": 55,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
            "Symptome präoperativ.Tinnitus...": "ja",
            "Behandlung/OP.CI Implantation": "Cochlear Nucleus"
        },
        "display_name": "Schmidt, Maria"
    }

    response = client.post("/api/v1/patients/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["input_features"]["Alter [J]"] == 55
    assert data["input_features"]["Symptome präoperativ.Tinnitus..."] == "ja"


def test_create_patient_can_be_retrieved(db: Session):
    """Test that created patient can be retrieved by ID."""
    payload = {
        "input_features": {
            "Alter [J]": 40,
            "Geschlecht": "m"
        },
        "display_name": "Test Retrieval"
    }

    # Create patient
    create_response = client.post("/api/v1/patients/", json=payload)
    assert create_response.status_code == 201
    patient_id = create_response.json()["id"]

    # Retrieve patient
    get_response = client.get(f"/api/v1/patients/{patient_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == patient_id
    assert data["display_name"] == "Test Retrieval"


def test_create_multiple_patients(db: Session):
    """Test creating multiple patients."""
    patients_data = [
        {
            "input_features": {"Alter [J]": 25, "Geschlecht": "w"},
            "display_name": "Patient 1"
        },
        {
            "input_features": {"Alter [J]": 35, "Geschlecht": "m"},
            "display_name": "Patient 2"
        },
        {
            "input_features": {"Alter [J]": 45, "Geschlecht": "w"},
            "display_name": "Patient 3"
        }
    ]

    created_ids = []
    for patient_data in patients_data:
        response = client.post("/api/v1/patients/", json=patient_data)
        assert response.status_code == 201
        created_ids.append(response.json()["id"])

    # Verify all patients were created with unique IDs
    assert len(set(created_ids)) == 3
