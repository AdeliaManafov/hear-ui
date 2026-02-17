from fastapi.testclient import TestClient


def test_predict_returns_prediction_and_explanation(client: TestClient):
    """Test that predict endpoint returns prediction and explanation."""
    payload = {"age": 45, "hearing_loss_duration": 5.0, "implant_type": "type_b"}
    resp = client.post("/api/v1/predict/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert "explanation" in data
    assert isinstance(data["explanation"], dict)
