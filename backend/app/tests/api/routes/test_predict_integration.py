import pytest
from sqlmodel import select

from app.core.config import settings
from app.models import Prediction


@pytest.mark.integration
def test_predict_persists_prediction(client, db):
    from app.tests.conftest import get_valid_predict_payload

    payload = get_valid_predict_payload()
    resp = client.post(f"{settings.API_V1_STR}/predict/?persist=true", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data

    # Verify a Prediction row was created in the DB
    statement = select(Prediction)
    results = db.exec(statement).all()
    # At least one prediction should exist
    assert len(results) > 0
    # Latest prediction should be a float
    assert isinstance(results[-1].prediction, float)
