import json

from fastapi.testclient import TestClient

from app.main import app


def test_predict_endpoint_smoke():
    client = TestClient(app)
    payload = {"age": 45, "hearing_loss_duration": 7.5, "implant_type": "type_a"}
    resp = client.post(f"/api/v1/predict/", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "prediction" in body
    assert "explanation" in body
