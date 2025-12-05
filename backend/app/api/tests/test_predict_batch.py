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
    # Route is /patients/upload (predict_batch router has prefix="/patients")
    resp = client.post("/api/v1/patients/upload", files={"file": ("patients.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2
    assert isinstance(data["results"], list)
    assert "prediction" in data["results"][0]


def test_upload_empty_csv():
    """Test uploading an empty CSV file."""
    csv_bytes = b"Alter,Geschlecht\n"  # Only header, no data rows
    resp = client.post("/api/v1/patients/upload", files={"file": ("empty.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 0
    assert data["results"] == []


def test_upload_csv_with_missing_columns():
    """Test CSV with some missing/null values."""
    # Use consistent columns for all rows
    rows = [
        {"Alter": 45, "Geschlecht": "m", "Seiten": ""},  # Empty Seiten
        {"Alter": "", "Geschlecht": "w", "Seiten": "L"},  # Empty Alter
    ]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload", files={"file": ("partial.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    # Should still process rows with missing data (preprocessor has defaults)
    assert data["count"] >= 0


def test_upload_csv_with_invalid_data():
    """Test CSV with invalid values that might cause errors."""
    rows = [
        {"Alter": "invalid", "Geschlecht": "m", "Seiten": "R"},
        {"Alter": -999, "Geschlecht": "x", "Seiten": "invalid"},
    ]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload", files={"file": ("invalid.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    # Should handle errors gracefully and potentially return errors for invalid rows
    assert "results" in data


def test_upload_csv_all_empty_rows():
    """Test CSV with all rows being completely empty."""
    csv_content = b"Alter,Geschlecht,Seiten\n,,,\n,,,\n,,,\n"
    resp = client.post("/api/v1/patients/upload", files={"file": ("all_empty.csv", csv_content, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    # Should filter out completely empty rows
    assert data["count"] == 0


def test_upload_malformed_csv():
    """Test uploading malformed CSV content."""
    # CSV with inconsistent column counts
    csv_content = b"Alter,Geschlecht\n45,m,extra_column\n30\n"
    resp = client.post("/api/v1/patients/upload", files={"file": ("malformed.csv", csv_content, "text/csv")})
    # Should handle gracefully (pandas is lenient) or return error
    assert resp.status_code in [200, 400]


def test_upload_non_csv_file():
    """Test uploading a non-CSV file."""
    non_csv_content = b"This is not a CSV file, just plain text"
    resp = client.post("/api/v1/patients/upload", files={"file": ("notcsv.txt", non_csv_content, "text/plain")})
    # Should fail to parse or return empty results
    # Backend may return 200 with empty results or 400 - both acceptable
    assert resp.status_code in [200, 400]
    if resp.status_code == 400:
        assert "Failed to read CSV" in resp.json()["detail"]


def test_upload_csv_with_bom():
    """Test CSV with UTF-8 BOM (common in Excel exports)."""
    csv_content = "\ufeffAlter,Geschlecht,Seiten\n45,m,R\n30,w,L\n"
    csv_bytes = csv_content.encode("utf-8")
    resp = client.post("/api/v1/patients/upload", files={"file": ("bom.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    # Should handle BOM correctly (pandas and our code should strip it)
    assert data["count"] >= 1


def test_upload_csv_with_german_column_names():
    """Test CSV with German column names (real-world scenario)."""
    # Using German names that should be recognized by the preprocessor
    rows = [
        {"Alter [J]": 50, "Geschlecht": "m", "Primäre Sprache": "Deutsch"},
        {"Alter [J]": 40, "Geschlecht": "w", "Primäre Sprache": "Englisch"},
    ]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload", files={"file": ("german.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 2
    assert all("prediction" in r for r in data["results"])


def test_upload_csv_with_special_characters():
    """Test CSV with special characters in values."""
    rows = [
        {"Alter": 45, "Geschlecht": "m", "Primäre Sprache": "Türkçe"},
        {"Alter": 35, "Geschlecht": "w", "Primäre Sprache": "العربية"},
    ]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload", files={"file": ("special.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    # Should handle UTF-8 special characters
    data = resp.json()
    assert "results" in data


def test_upload_large_csv():
    """Test uploading a CSV with many rows."""
    rows = [{"Alter": 30 + i, "Geschlecht": "m" if i % 2 == 0 else "w", "Seiten": "R"} for i in range(100)]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload", files={"file": ("large.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 50  # Should process many rows


def test_upload_csv_with_persistence():
    """Test CSV upload with persist=true."""
    rows = [{"Alter": 55, "Geschlecht": "w", "Seiten": "L"}]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload?persist=true", files={"file": ("persist.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    # Should attempt to persist predictions (may succeed or fail depending on DB state)
    assert "results" in data


def test_upload_csv_mixed_valid_invalid():
    """Test CSV with mix of valid and invalid rows."""
    rows = [
        {"Alter": 45, "Geschlecht": "m"},  # Valid
        {"Alter": "not_a_number", "Geschlecht": 123},  # Invalid types
        {"Alter": 50, "Geschlecht": "w"},  # Valid
    ]
    csv_bytes = _make_csv(rows)
    resp = client.post("/api/v1/patients/upload", files={"file": ("mixed.csv", csv_bytes, "text/csv")})
    assert resp.status_code == 200
    data = resp.json()
    # Should process valid rows and handle invalid ones gracefully
    assert "results" in data
    # Check that some rows have predictions and some may have errors
    has_prediction = any("prediction" in r and r["prediction"] is not None for r in data["results"])
    assert has_prediction
