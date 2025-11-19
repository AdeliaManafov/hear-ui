import uuid
from typing import Any, Optional, List
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Item,
    ItemCreate,
    User,
    UserCreate,
    UserUpdate,
    Feedback,
    FeedbackCreate,
    Prediction,
    PredictionCreate,
)


# ------------------------------------------------------------
# Benutzer anhand der E-Mail abrufen
# ------------------------------------------------------------
def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    result = session.exec(statement)
    return result.first()


# ------------------------------------------------------------
# Benutzer erstellen
# ------------------------------------------------------------
def create_user(session: Session, user_create: UserCreate) -> User:
    db_user = User(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# ------------------------------------------------------------
# Benutzer aktualisieren
# ------------------------------------------------------------
def update_user(session: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        user_data["hashed_password"] = get_password_hash(user_data["password"])
        del user_data["password"]

    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# ------------------------------------------------------------
# Benutzer authentifizieren (Login)
# ------------------------------------------------------------
def authenticate(session: Session, email: str, password: str) -> Optional[User]:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# ------------------------------------------------------------
# Item (z. B. Patientendaten) anlegen
# ------------------------------------------------------------
def create_item(session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item(**item_in.model_dump(), owner_id=owner_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# ------------------------------------------------------------
# Feedback CRUD
# ------------------------------------------------------------
def create_feedback(session: Session, feedback_in: FeedbackCreate) -> Feedback:
    db_obj = Feedback(**feedback_in.model_dump())
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_feedback(session: Session, feedback_id: uuid.UUID) -> Optional[Feedback]:
    statement = select(Feedback).where(Feedback.id == feedback_id)
    result = session.exec(statement)
    return result.first()


def list_feedback(session: Session, limit: int = 100, offset: int = 0) -> List[Feedback]:
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


def get_prediction(session: Session, prediction_id: uuid.UUID) -> Optional[Prediction]:
    statement = select(Prediction).where(Prediction.id == prediction_id)
    result = session.exec(statement)
    return result.first()


def list_predictions(session: Session, limit: int = 100, offset: int = 0) -> List[Prediction]:
    statement = select(Prediction).offset(offset).limit(limit)
    return session.exec(statement).all()
