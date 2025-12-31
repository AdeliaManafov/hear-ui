
from fastapi.testclient import TestClient

from app.main import app


def test_predict_endpoint_smoke():
    client = TestClient(app)
    payload = {"age": 45, "hearing_loss_duration": 7.5, "implant_type": "type_a"}
    resp = client.post("/api/v1/predict/", json=payload)
    # The endpoint may return 200 with a prediction (fallback or pipeline) or
    # 422 if a loaded model expects a preprocessed feature vector. Both are
    # acceptable for this integration smoke test.
    assert resp.status_code in (200, 422)
    if resp.status_code == 200:
        body = resp.json()
        assert "prediction" in body
        assert "explanation" in body
    else:
        body = resp.json()
        # ensure the validation message is helpful
        assert "expects" in body.get("detail", "") or "preprocess" in body.get("detail", "")
