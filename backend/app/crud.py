import uuid
from typing import Any, Optional
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate


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
