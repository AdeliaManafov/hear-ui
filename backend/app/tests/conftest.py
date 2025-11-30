from collections.abc import Generator
import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app


def _db_available() -> bool:
    """Check if database is available without raising."""
    try:
        from app.core.db import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    """Database session fixture - only used when DB is available."""
    try:
        from app.core.db import engine, init_db
        with Session(engine) as session:
            init_db(session)
            yield session
    except Exception as e:
        pytest.skip(f"Database not available: {e}")


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    # Authentication removed; fixture intentionally unavailable.
    pytest.skip("auth fixtures removed")


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    pytest.skip("auth fixtures removed")
