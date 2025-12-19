"""Additional tests to improve coverage for core modules."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


class TestPatientsRouteCoverage:
    """Tests to improve coverage of patients routes."""
    
    def test_list_patients_paginated(self, client: TestClient, test_patient):
        """Test paginated patient list."""
        response = client.get("/api/v1/patients/?paginated=true&limit=10&offset=0")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert "has_more" in data
    
    def test_get_patient_by_id(self, client: TestClient, test_patient):
        """Test getting single patient."""
        response = client.get(f"/api/v1/patients/{test_patient.id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == str(test_patient.id)
    
    def test_update_patient(self, client: TestClient, test_patient, db: Session):
        """Test updating patient."""
        payload = {
            "input_features": {
                "Alter [J]": 50,
                "Geschlecht": "w"
            },
            "display_name": "Updated Patient"
        }
        
        response = client.put(f"/api/v1/patients/{test_patient.id}", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["display_name"] == "Updated Patient"
    
    def test_validate_patient_endpoint(self, client: TestClient, test_patient):
        """Test patient validation endpoint."""
        response = client.get(f"/api/v1/patients/{test_patient.id}/validate")
        assert response.status_code == 200
        
        data = response.json()
        assert "ok" in data
        assert "missing_features" in data
    
    def test_patient_not_found(self, client: TestClient):
        """Test 404 for non-existent patient."""
        import uuid
        fake_id = uuid.uuid4()
        response = client.get(f"/api/v1/patients/{fake_id}")
        assert response.status_code == 404


class TestPreprocessorCoverage:
    """Tests to improve preprocessor coverage."""
    
    def test_preprocessor_with_minimal_data(self):
        """Test preprocessor handles minimal data."""
        from app.core.preprocessor import preprocess_patient_data
        
        # Only age
        data = {"Alter [J]": 45}
        result = preprocess_patient_data(data)
        
        assert result is not None
        assert len(result.columns) == 68  # All expected features
    
    def test_preprocessor_with_alternative_keys(self):
        """Test preprocessor handles alternative column names."""
        from app.core.preprocessor import preprocess_patient_data
        
        # Use lowercase alternatives
        data = {
            "alter": 45,
            "geschlecht": "w"
        }
        result = preprocess_patient_data(data)
        
        assert result is not None
        assert result.shape[1] == 68


class TestCrudCoverage:
    """Tests to improve CRUD coverage."""
    
    def test_crud_get_patient_not_found(self, db: Session):
        """Test CRUD get_patient with non-existent ID."""
        from app import crud
        import uuid
        
        fake_id = uuid.uuid4()
        patient = crud.get_patient(session=db, patient_id=fake_id)
        
        assert patient is None
    
    def test_crud_get_patients_with_limit(self, db: Session, test_patient):
        """Test CRUD get_patients with pagination."""
        from app import crud
        
        patients = crud.get_patients(session=db, limit=5, offset=0)
        
        assert patients is not None
        assert len(patients) <= 5
    
    def test_crud_count_patients(self, db: Session, test_patient):
        """Test CRUD count_patients."""
        from app import crud
        
        count = crud.count_patients(session=db)
        
        assert count >= 1  # At least the test_patient
    
    def test_crud_update_patient(self, db: Session, test_patient):
        """Test CRUD update_patient."""
        from app import crud
        from app.models import PatientUpdate
        
        update_data = PatientUpdate(
            display_name="Updated via CRUD"
        )
        
        updated = crud.update_patient(
            session=db,
            patient_id=test_patient.id,
            patient_in=update_data
        )
        db.commit()
        
        assert updated is not None
        assert updated.display_name == "Updated via CRUD"


class TestFeedbackCoverage:
    """Tests to improve feedback coverage."""

    def test_feedback_list(self, client: TestClient):
        """Test listing all feedbacks."""
        response = client.get("/api/v1/feedback/")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

    def test_feedback_create_and_retrieve(self, client: TestClient):
        """Test creating and retrieving feedback."""
        payload = {
            "user_agrees": True,
            "comment": "Test coverage feedback",
            "prediction_id": None
        }

        # Create
        response = client.post("/api/v1/feedback/", json=payload)
        assert response.status_code == 201

        data = response.json()
        feedback_id = data["id"]

        # Retrieve
        response = client.get("/api/v1/feedback/")
        assert response.status_code == 200
        feedbacks = response.json()

        assert any(f["id"] == feedback_id for f in feedbacks)


class TestConfigCoverage:
    """Tests to improve config coverage."""
    
    def test_config_settings_exist(self):
        """Test that config settings are properly initialized."""
        from app.core.config import settings
        
        assert settings is not None
        assert settings.API_V1_STR is not None
        assert settings.PROJECT_NAME is not None

