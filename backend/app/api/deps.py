from collections.abc import Generator
from typing import Annotated

from sqlmodel import Session
from fastapi import Depends

from app.core.db import engine
from app.models import User


def get_db() -> Generator[Session, None, None]:
    """Database session dependency."""
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(session: SessionDep) -> User:
    """
    Authentication has been disabled for this project per request.
    For compatibility, return a default local superuser so routes that expect
    a `current_user` continue to work without requiring tokens.
    """
    # Create a lightweight User object (not persisted) to act as admin for demos
    user = User(
        email="local@dev",
        full_name="Local Dev",
        is_active=True,
        is_superuser=True,
        hashed_password="",
    )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """Pass-through: current_user is already a superuser in demo mode."""
    return current_user
