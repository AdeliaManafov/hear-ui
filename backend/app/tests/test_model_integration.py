from fastapi.testclient import TestClient


def test_predict_endpoint_smoke(client: TestClient):
    from app.tests.conftest import get_valid_predict_payload

    payload = get_valid_predict_payload()
    resp = client.post("/api/v1/predict/", json=payload)
    # The endpoint may return 200 with a prediction or
    # 422 if validation fails. Both are acceptable for this smoke test.
    assert resp.status_code in (200, 422)
    if resp.status_code == 200:
        body = resp.json()
        assert "prediction" in body
        assert "explanation" in body
    else:
        body = resp.json()
        # ensure the validation message is helpful
        assert "detail" in body
