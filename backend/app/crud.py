import uuid

from sqlmodel import Session, select

from app.models import (
    Feedback,
    FeedbackCreate,
    Prediction,
    PredictionCreate,
)


# ------------------------------------------------------------
# Feedback CRUD
# ------------------------------------------------------------
def create_feedback(session: Session, feedback_in: FeedbackCreate) -> Feedback:
    db_obj = Feedback(**feedback_in.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_feedback(session: Session, feedback_id: uuid.UUID) -> Feedback | None:
    statement = select(Feedback).where(Feedback.id == feedback_id)
    result = session.exec(statement)
    return result.first()


def list_feedback(session: Session, limit: int = 100, offset: int = 0) -> list[Feedback]:
    statement = select(Feedback).offset(offset).limit(limit)
    return session.exec(statement).all()


# ------------------------------------------------------------
# Prediction CRUD
# ------------------------------------------------------------
def create_prediction(session: Session, prediction_in: PredictionCreate) -> Prediction:
    db_obj = Prediction(**prediction_in.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_prediction(session: Session, prediction_id: uuid.UUID) -> Prediction | None:
    statement = select(Prediction).where(Prediction.id == prediction_id)
    result = session.exec(statement)
    return result.first()


def list_predictions(session: Session, limit: int = 100, offset: int = 0) -> list[Prediction]:
    statement = select(Prediction).offset(offset).limit(limit)
    return session.exec(statement).all()
