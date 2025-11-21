import csv
import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _make_csv(rows):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
    return output.getvalue().encode("utf-8")


def test_upload_csv_and_predict_basic():
    rows = [{"Alter": 45, "Seiten": "R", "Geschlecht": "m"}, {"Alter": 30, "Seiten": "L", "Geschlecht": "w"}]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/predict/upload", files={"file": ("patients.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2
    assert isinstance(data["results"], list)
    assert "prediction" in data["results"][0]
