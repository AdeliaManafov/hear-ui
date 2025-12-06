"""
Umfassende Datenbank-Integrationstests für das HEAR-Projekt.

Diese Tests prüfen:
- Datenbank-Verbindung
- CRUD-Operationen
- Daten-Persistierung
- Transaktionen
"""

import uuid
from datetime import datetime

import pytest
from sqlmodel import Session, select

from app.crud import create_feedback, create_prediction, get_feedback, get_prediction
from app.models import Feedback, FeedbackCreate, Prediction, PredictionCreate


@pytest.mark.integration
class TestDatabaseConnection:
    """Tests für Datenbank-Verbindung."""

    def test_database_connection_is_active(self, db: Session) -> None:
        """Test: Datenbank-Verbindung ist aktiv."""
        assert db is not None
        assert db.is_active

    def test_can_execute_simple_query(self, db: Session) -> None:
        """Test: Einfache Query kann ausgeführt werden."""
        result = db.execute(select(1))
        assert result.scalar() == 1


@pytest.mark.integration
class TestFeedbackCRUD:
    """Tests für Feedback CRUD-Operationen."""

    def test_create_feedback_with_all_fields(self, db: Session) -> None:
        """Test: Feedback mit allen Feldern erstellen."""
        feedback_in = FeedbackCreate(
            input_features={"age": 45, "hearing_loss_duration": 3.0, "implant_type": "type_b"},
            prediction=0.85,
            explanation={"age": 0.3, "hearing_loss_duration": 0.4, "implant_type": 0.15},
            accepted=True,
            comment="Sehr gute Vorhersage",
        )

        feedback = create_feedback(session=db, feedback_in=feedback_in)

        assert feedback.id is not None
        assert isinstance(feedback.id, uuid.UUID)
        assert feedback.prediction == 0.85
        assert feedback.accepted is True
        assert feedback.comment == "Sehr gute Vorhersage"
        assert feedback.created_at is not None
        assert isinstance(feedback.created_at, datetime)

    def test_create_feedback_with_minimal_fields(self, db: Session) -> None:
        """Test: Feedback mit minimalen Feldern erstellen."""
        feedback_in = FeedbackCreate()
        feedback = create_feedback(session=db, feedback_in=feedback_in)

        assert feedback.id is not None
        assert feedback.input_features is None
        assert feedback.prediction is None
        assert feedback.accepted is None
        assert feedback.comment is None

    def test_get_feedback_by_id(self, db: Session) -> None:
        """Test: Feedback nach ID abrufen."""
        feedback_in = FeedbackCreate(
            prediction=0.75,
            accepted=True,
            comment="Test",
        )
        created = create_feedback(session=db, feedback_in=feedback_in)

        retrieved = get_feedback(session=db, feedback_id=created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.prediction == 0.75
        assert retrieved.accepted is True

    def test_get_nonexistent_feedback_returns_none(self, db: Session) -> None:
        """Test: Nicht existierendes Feedback gibt None zurück."""
        fake_id = uuid.uuid4()
        result = get_feedback(session=db, feedback_id=fake_id)
        assert result is None


@pytest.mark.integration
class TestPredictionCRUD:
    """Tests für Prediction CRUD-Operationen."""

    def test_create_prediction_with_all_fields(self, db: Session) -> None:
        """Test: Prediction mit allen Feldern erstellen."""
        prediction_in = PredictionCreate(
            input_features={"age": 55, "hearing_loss_duration": 7.0, "implant_type": "type_c"},
            prediction=0.62,
            explanation={"age": 0.25, "hearing_loss_duration": 0.2, "implant_type": 0.17},
        )

        prediction = create_prediction(session=db, prediction_in=prediction_in)

        assert prediction.id is not None
        assert isinstance(prediction.id, uuid.UUID)
        assert prediction.prediction == 0.62
        assert prediction.input_features["age"] == 55
        assert prediction.explanation["age"] == 0.25
        assert prediction.created_at is not None

    def test_get_prediction_by_id(self, db: Session) -> None:
        """Test: Prediction nach ID abrufen."""
        prediction_in = PredictionCreate(
            input_features={"age": 40},
            prediction=0.9,
            explanation={"age": 0.5},
        )
        created = create_prediction(session=db, prediction_in=prediction_in)

        retrieved = get_prediction(session=db, prediction_id=created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.prediction == 0.9

    def test_get_nonexistent_prediction_returns_none(self, db: Session) -> None:
        """Test: Nicht existierende Prediction gibt None zurück."""
        fake_id = uuid.uuid4()
        result = get_prediction(session=db, prediction_id=fake_id)
        assert result is None


@pytest.mark.integration
class TestDataPersistence:
    """Tests für Daten-Persistierung."""

    def test_feedback_persists_across_sessions(self, db: Session) -> None:
        """Test: Feedback bleibt über Sessions hinweg erhalten."""
        # Erstelle Feedback
        feedback_in = FeedbackCreate(
            prediction=0.88,
            accepted=True,
            comment="Persistenz-Test",
        )
        created = create_feedback(session=db, feedback_in=feedback_in)
        feedback_id = created.id

        # Commit und schließe Session
        db.commit()
        db.close()

        # Neue Session
        from app.core.db import engine

        with Session(engine) as new_session:
            retrieved = get_feedback(session=new_session, feedback_id=feedback_id)
            assert retrieved is not None
            assert retrieved.comment == "Persistenz-Test"

    def test_json_fields_are_correctly_stored(self, db: Session) -> None:
        """Test: JSON-Felder werden korrekt gespeichert."""
        complex_data = {
            "age": 65,
            "hearing_loss_duration": 5.5,
            "implant_type": "type_a",
            "additional_info": {"notes": "Test", "score": 42},
        }

        feedback_in = FeedbackCreate(
            input_features=complex_data,
            explanation={"feature1": 0.1, "feature2": 0.2, "feature3": 0.3},
        )

        feedback = create_feedback(session=db, feedback_in=feedback_in)

        # Abrufen und prüfen
        retrieved = get_feedback(session=db, feedback_id=feedback.id)
        assert retrieved.input_features == complex_data
        assert retrieved.explanation["feature2"] == 0.2


@pytest.mark.integration
class TestDataValidation:
    """Tests für Datenvalidierung."""

    def test_feedback_with_negative_prediction_is_accepted(self, db: Session) -> None:
        """Test: Feedback mit negativer Vorhersage wird akzeptiert (keine Validierung)."""
        feedback_in = FeedbackCreate(prediction=-0.5)
        feedback = create_feedback(session=db, feedback_in=feedback_in)
        assert feedback.prediction == -0.5

    def test_feedback_with_prediction_over_one_is_accepted(self, db: Session) -> None:
        """Test: Feedback mit Vorhersage > 1 wird akzeptiert (keine Validierung)."""
        feedback_in = FeedbackCreate(prediction=1.5)
        feedback = create_feedback(session=db, feedback_in=feedback_in)
        assert feedback.prediction == 1.5

    def test_empty_json_fields_are_handled(self, db: Session) -> None:
        """Test: Leere JSON-Felder werden korrekt behandelt."""
        feedback_in = FeedbackCreate(
            input_features={},
            explanation={},
        )
        feedback = create_feedback(session=db, feedback_in=feedback_in)

        assert feedback.input_features == {}
        assert feedback.explanation == {}
