from fastapi.testclient import TestClient


def test_predict_returns_prediction_and_explanation(client: TestClient):
    """Test that predict endpoint returns prediction and explanation."""
    from app.tests.conftest import get_valid_predict_payload

    payload = get_valid_predict_payload()
    resp = client.post("/api/v1/predict/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert "explanation" in data
    assert isinstance(data["explanation"], dict)
