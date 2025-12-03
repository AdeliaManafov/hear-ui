"""Tests for feedback API endpoints."""

import uuid
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.main import app
from app.models import Feedback
from app.core.db import engine

client = TestClient(app)


def test_create_feedback_success():
    """Test creating feedback with valid data."""
    payload = {
        "input_features": {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch"
        },
        "prediction": 0.75,
        "explanation": {
            "age": 0.15,
            "hearing_loss_duration": 0.25,
            "implant_type": 0.35
        },
        "accepted": True,
        "comment": "Good prediction"
    }
    
    response = client.post("/api/v1/feedback/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["accepted"] is True
    assert data["comment"] == "Good prediction"
    assert data["prediction"] == 0.75
    assert "input_features" in data
    assert "created_at" in data


def test_create_feedback_minimal():
    """Test creating feedback with minimal required data."""
    payload = {
        "input_features": {"test": "data"},
        "prediction": 0.5,
        "explanation": {},
        "accepted": False
    }
    
    response = client.post("/api/v1/feedback/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["accepted"] is False
    assert data["comment"] is None


def test_create_feedback_rejected():
    """Test creating feedback with rejected prediction."""
    payload = {
        "input_features": {"age": 30},
        "prediction": 0.25,
        "explanation": {},
        "accepted": False,
        "comment": "Prediction seems wrong"
    }
    
    response = client.post("/api/v1/feedback/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["accepted"] is False
    assert "wrong" in data["comment"].lower()


def test_get_feedback_by_id():
    """Test retrieving feedback by ID."""
    # First create feedback
    payload = {
        "input_features": {"test": "retrieve"},
        "prediction": 0.8,
        "explanation": {},
        "accepted": True
    }
    
    create_response = client.post("/api/v1/feedback/", json=payload)
    assert create_response.status_code == 201
    feedback_id = create_response.json()["id"]
    
    # Now retrieve it
    get_response = client.get(f"/api/v1/feedback/{feedback_id}")
    
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == feedback_id
    assert data["prediction"] == 0.8
    assert data["accepted"] is True


def test_get_feedback_not_found():
    """Test retrieving non-existent feedback returns 404."""
    fake_id = str(uuid.uuid4())
    
    response = client.get(f"/api/v1/feedback/{fake_id}")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_feedback_persists_in_database():
    """Test that feedback is actually persisted in the database."""
    payload = {
        "input_features": {"persist": "test"},
        "prediction": 0.9,
        "explanation": {},
        "accepted": True,
        "comment": "Persistence test"
    }
    
    response = client.post("/api/v1/feedback/", json=payload)
    assert response.status_code == 201
    feedback_id = response.json()["id"]
    
    # Query database directly
    with Session(engine) as session:
        statement = select(Feedback).where(Feedback.id == uuid.UUID(feedback_id))
        result = session.exec(statement)
        feedback = result.first()
        
        assert feedback is not None
        assert feedback.comment == "Persistence test"
        assert feedback.accepted is True
        assert feedback.prediction == 0.9


def test_create_feedback_with_null_values():
    """Test creating feedback with null/None values."""
    payload = {
        "input_features": None,
        "prediction": None,
        "explanation": None,
        "accepted": None,
        "comment": None
    }
    
    response = client.post("/api/v1/feedback/", json=payload)
    
    # Should still succeed - all fields are optional in the model
    assert response.status_code == 201
    data = response.json()
    assert data["accepted"] is None
    assert data["comment"] is None


def test_create_feedback_with_complex_explanation():
    """Test creating feedback with detailed SHAP explanation."""
    payload = {
        "input_features": {
            "Alter [J]": 55,
            "Geschlecht": "m",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual"
        },
        "prediction": 0.65,
        "explanation": {
            "feature_importance": {
                "age": 0.12,
                "hearing_loss_duration": 0.23,
                "implant_type": 0.30
            },
            "shap_values": [0.12, 0.23, 0.30, -0.05],
            "base_value": 0.5
        },
        "accepted": True,
        "comment": "SHAP values look reasonable"
    }
    
    response = client.post("/api/v1/feedback/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "feature_importance" in data["explanation"]
    assert "shap_values" in data["explanation"]


def test_feedback_roundtrip():
    """Test creating and retrieving feedback maintains data integrity."""
    original_payload = {
        "input_features": {
            "Alter [J]": 42,
            "Geschlecht": "w"
        },
        "prediction": 0.777,
        "explanation": {
            "top_feature": "age",
            "importance": 0.5
        },
        "accepted": False,
        "comment": "Roundtrip test comment"
    }
    
    # Create
    create_resp = client.post("/api/v1/feedback/", json=original_payload)
    assert create_resp.status_code == 201
    feedback_id = create_resp.json()["id"]
    
    # Retrieve
    get_resp = client.get(f"/api/v1/feedback/{feedback_id}")
    assert get_resp.status_code == 200
    retrieved = get_resp.json()
    
    # Verify integrity
    assert retrieved["prediction"] == original_payload["prediction"]
    assert retrieved["accepted"] == original_payload["accepted"]
    assert retrieved["comment"] == original_payload["comment"]
    assert retrieved["input_features"]["Alter [J]"] == 42
    assert retrieved["explanation"]["top_feature"] == "age"
