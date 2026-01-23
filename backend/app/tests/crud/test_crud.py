"""Tests for CRUD operations."""

from uuid import uuid4

import pytest
from sqlmodel import Session

from app import crud
from app.models import FeedbackCreate, PatientCreate, PredictionCreate


def _db_available() -> bool:
    """Check if database is reachable."""
    try:
        from sqlalchemy import text

        from app.core.db import engine

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _db_available(), reason="Database not available")


class TestFeedbackCRUD:
    """Tests for Feedback CRUD operations."""

    def test_create_feedback(self, db: Session):
        """Test creating feedback."""
        feedback_in = FeedbackCreate(
            input_features={"age": 45},
            prediction=0.85,
            accepted=True,
            comment="Test feedback",
        )

        result = crud.create_feedback(session=db, feedback_in=feedback_in)

        assert result.id is not None
        assert result.prediction == 0.85
        assert result.accepted is True
        assert result.comment == "Test feedback"

    def test_get_feedback(self, db: Session):
        """Test getting feedback by ID."""
        feedback_in = FeedbackCreate(
            input_features={"age": 50},
            prediction=0.75,
            accepted=False,
        )
        created = crud.create_feedback(session=db, feedback_in=feedback_in)

        result = crud.get_feedback(session=db, feedback_id=created.id)

        assert result is not None
        assert result.id == created.id

    def test_get_feedback_not_found(self, db: Session):
        """Test getting non-existent feedback."""
        result = crud.get_feedback(session=db, feedback_id=uuid4())
        assert result is None

    def test_list_feedback(self, db: Session):
        """Test listing feedback."""
        # Create some feedback
        for i in range(3):
            crud.create_feedback(
                session=db, feedback_in=FeedbackCreate(prediction=0.5 + i * 0.1)
            )

        result = crud.list_feedback(session=db, limit=10)

        assert isinstance(result, list)
        assert len(result) >= 3

    def test_list_feedback_with_pagination(self, db: Session):
        """Test listing feedback with offset and limit."""
        result = crud.list_feedback(session=db, limit=2, offset=0)
        assert len(result) <= 2


class TestPredictionCRUD:
    """Tests for Prediction CRUD operations."""

    def test_create_prediction(self, db: Session):
        """Test creating prediction."""
        prediction_in = PredictionCreate(
            input_features={"age": 55, "gender": "m"},
            prediction=0.92,
        )

        result = crud.create_prediction(session=db, prediction_in=prediction_in)

        assert result.id is not None
        assert result.prediction == 0.92

    def test_get_prediction(self, db: Session):
        """Test getting prediction by ID."""
        prediction_in = PredictionCreate(
            input_features={"age": 60},
            prediction=0.88,
        )
        created = crud.create_prediction(session=db, prediction_in=prediction_in)

        result = crud.get_prediction(session=db, prediction_id=created.id)

        assert result is not None
        assert result.id == created.id

    def test_get_prediction_not_found(self, db: Session):
        """Test getting non-existent prediction."""
        result = crud.get_prediction(session=db, prediction_id=uuid4())
        assert result is None

    def test_list_predictions(self, db: Session):
        """Test listing predictions."""
        result = crud.list_predictions(session=db, limit=10)
        assert isinstance(result, list)


class TestPatientCRUD:
    """Tests for Patient CRUD operations."""

    def test_create_patient(self, db: Session):
        """Test creating patient."""
        patient_in = PatientCreate(input_features={"Alter [J]": 45, "Geschlecht": "w"})

        result = crud.create_patient(session=db, patient_in=patient_in)

        assert result.id is not None
        assert result.input_features["Alter [J]"] == 45

    def test_get_patient(self, db: Session):
        """Test getting patient by ID."""
        patient_in = PatientCreate(input_features={"Alter [J]": 50})
        created = crud.create_patient(session=db, patient_in=patient_in)

        result = crud.get_patient(session=db, patient_id=created.id)

        assert result is not None
        assert result.id == created.id

    def test_get_patient_not_found(self, db: Session):
        """Test getting non-existent patient."""
        result = crud.get_patient(session=db, patient_id=uuid4())
        assert result is None

    def test_list_patients(self, db: Session):
        """Test listing patients."""
        result = crud.list_patients(session=db, limit=10)
        assert isinstance(result, list)

    def test_list_patients_with_pagination(self, db: Session):
        """Test listing patients with pagination."""
        result = crud.list_patients(session=db, limit=5, offset=0)
        assert len(result) <= 5

    def test_count_patients(self, db: Session):
        """Test counting patients."""
        # Create a patient
        crud.create_patient(
            session=db, patient_in=PatientCreate(input_features={"test": True})
        )

        count = crud.count_patients(session=db)

        assert isinstance(count, int)
        assert count >= 1
