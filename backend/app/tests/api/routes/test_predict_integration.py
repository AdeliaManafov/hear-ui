from sqlmodel import select

from app.core.config import settings
from app.models import Prediction


def test_predict_persists_prediction(client, db):
    payload = {"age": 50, "hearing_loss_duration": 8.0, "implant_type": "type_a"}
    resp = client.post(f"{settings.API_V1_STR}/predict/?persist=true", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data

    # Verify a Prediction row was created in the DB
    statement = select(Prediction)
    result = db.exec(statement).first()
    assert result is not None
    assert result.input_features is not None
    assert result.input_features.get("age") == payload["age"]
    assert isinstance(result.prediction, float)
