from fastapi.testclient import TestClient

from app.api.routes.predict import compute_prediction_and_explanation
from app.main import app


def test_compute_prediction_and_explanation_structure_unit():
    patient = {"age": 40, "hearing_loss_duration": 5.0, "implant_type": "type_b"}
    result = compute_prediction_and_explanation(patient)
    assert "prediction" in result
    assert "explanation" in result
    assert isinstance(result["prediction"], float | int)
    assert isinstance(result["explanation"], dict)
    for key in ["age", "hearing_loss_duration", "implant_type"]:
        assert key in result["explanation"]
        assert isinstance(result["explanation"][key], float | int)


def test_predict_endpoint_returns_prediction_and_explanation_integration():
    client = TestClient(app)
    payload = {"age": 45, "hearing_loss_duration": 5.0, "implant_type": "type_b"}
    resp = client.post("/api/v1/predict/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert "explanation" in data
    assert isinstance(data["explanation"], dict)
