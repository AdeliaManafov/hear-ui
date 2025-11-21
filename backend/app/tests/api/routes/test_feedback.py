from uuid import uuid4

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


def test_create_and_get_feedback(client: TestClient, db: Session) -> None:
    payload = {
        "user_email": random_email(),
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
    assert fb.get("user_email") == payload["user_email"]
    assert fb.get("comment") == payload["comment"]


def test_get_feedback_not_found(client: TestClient) -> None:
    resp = client.get(f"{settings.API_V1_STR}/feedback/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Feedback not found"
