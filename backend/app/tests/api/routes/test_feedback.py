"""Tests for Feedback API routes."""

from uuid import uuid4
import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.utils import random_lower_string


def _db_available() -> bool:
    """Check if database is reachable."""
    try:
        from app.core.db import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# Mark all tests in this module to skip if DB is not available
pytestmark = pytest.mark.skipif(
    not _db_available(),
    reason="Database not available - run with docker compose up db"
)


def test_create_and_get_feedback(client: TestClient, db: Session) -> None:
    payload = {
        "comment": random_lower_string(),
    }
    resp = client.post(f"{settings.API_V1_STR}/feedback/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    feedback_id = data["id"]

    get_resp = client.get(f"{settings.API_V1_STR}/feedback/{feedback_id}")
    assert get_resp.status_code == 200
    fb = get_resp.json()
    assert fb.get("comment") == payload["comment"]


def test_get_feedback_not_found(client: TestClient) -> None:
    resp = client.get(f"{settings.API_V1_STR}/feedback/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Feedback not found"
