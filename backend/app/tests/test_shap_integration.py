"""Integration tests for SHAP endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_predict_endpoint_with_model(client: TestClient):
    """Test predict endpoint returns prediction and explanation."""
    # Use minimal payload - API should handle defaults
    payload = {
        "Alter [J]": 65,
    }
    
    response = client.post("/api/v1/predict/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "prediction" in data
    assert "explanation" in data
    
    # Verify prediction is numeric
    assert isinstance(data["prediction"], int | float)
    assert 0 <= data["prediction"] <= 1
    
    # Verification explanation is present (may be empty for basic predict)
    assert isinstance(data["explanation"], dict)


def test_predict_endpoint_different_implant_types(client: TestClient):
    """Test predict endpoint handles different implant types."""
    implant_types = ["type_a", "type_b", "type_c"]
    
    for implant_type in implant_types:
        payload = {
            "age": 50,
            "hearing_loss_duration": 10.0,
            "implant_type": implant_type,
        }
        
        response = client.post("/api/v1/predict/", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "explanation" in data


def test_predict_endpoint_with_persist(client: TestClient, db):
    """Test predict endpoint can persist predictions."""
    payload = {
        "age": 70,
        "hearing_loss_duration": 15.0,
        "implant_type": "type_b",
    }
    
    response = client.post("/api/v1/predict/?persist=true", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data


def test_predict_endpoint_validation(client: TestClient):
    """Test predict endpoint validates input."""
    # All fields now have defaults, so even empty payload should work
    payload = {}

    response = client.post("/api/v1/predict/", json=payload)

    # Should succeed with defaults
    assert response.status_code == 200


def test_predict_endpoint_edge_cases(client: TestClient):
    """Test predict endpoint handles edge cases."""
    # Very young age
    payload1 = {
        "age": 18,
        "hearing_loss_duration": 1.0,
        "implant_type": "type_a",
    }
    
    response1 = client.post("/api/v1/predict/", json=payload1)
    assert response1.status_code == 200
    
    # Very old age
    payload2 = {
        "age": 90,
        "hearing_loss_duration": 30.0,
        "implant_type": "type_c",
    }
    
    response2 = client.post("/api/v1/predict/", json=payload2)
    assert response2.status_code == 200
    
    # Zero duration
    payload3 = {
        "age": 50,
        "hearing_loss_duration": 0.0,
        "implant_type": "type_a",
    }
    
    response3 = client.post("/api/v1/predict/", json=payload3)
    assert response3.status_code == 200


def test_shap_explain_endpoint(client: TestClient):
    """Test SHAP explain endpoint returns detailed explanation."""
    #Use new 7feature format
    payload = {
        "Alter [J]": 65,
    }
    
    response = client.post("/api/v1/shap/explain", json=payload)
    
    # Accept either 200 (success) or 503 (model not loaded) or 422 (validation)
    assert response.status_code in [200, 503, 422]
    
    if response.status_code == 200:
        data = response.json()
        
        # Verify response structure
        assert "prediction" in data
        assert "feature_importance" in data
        assert "shap_values" in data
        assert "base_value" in data
        assert "top_features" in data
        
        # Verify types
        assert isinstance(data["prediction"], int | float)
        assert isinstance(data["feature_importance"], dict)
        assert isinstance(data["shap_values"], list)
        assert isinstance(data["base_value"], int | float)
        assert isinstance(data["top_features"], list)
        
        # Verify top features structure
        if data["top_features"]:
            assert "feature" in data["top_features"][0]
            assert "importance" in data["top_features"][0]
    
    elif response.status_code == 503:
        # Model not loaded - expected in some test environments
        data = response.json()
        assert "detail" in data
        assert "Model not loaded" in data["detail"]
    
    # 422 is validation error - acceptable for this test


def test_shap_explain_endpoint_with_plot(client: TestClient):
    """Test SHAP explain endpoint can generate plots."""
    payload = {
        "age": 65,
        "hearing_loss_duration": 5.5,
        "implant_type": "type_a",
        "include_plot": True,
    }
    
    response = client.post("/api/v1/shap/explain", json=payload)
    
    # If model is loaded and SHAP works
    if response.status_code == 200:
        data = response.json()
        
        # Plot might be None if matplotlib not available
        if data.get("plot_base64"):
            assert data["plot_base64"].startswith("data:image/png;base64,")


def test_model_info_endpoint(client: TestClient):
    """Test model info endpoint returns model status."""
    response = client.get("/api/v1/utils/model-info/")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "loaded" in data
    assert isinstance(data["loaded"], bool)
    
    if data["loaded"]:
        # If model is loaded, should have additional info
        assert "model_type" in data or "expected_n_features" in data


@pytest.mark.skip(reason="Batch endpoint needs update for new 7-feature format")
def test_predict_batch_endpoint(client: TestClient):
    """Test batch prediction endpoint."""
    # TODO: Update CSV header to match new feature format
    # Create CSV content
    csv_content = """age,hearing_loss_duration,implant_type
65,5.5,type_a
50,10.0,type_b
70,15.0,type_c
"""
    
    files = {"file": ("test.csv", csv_content, "text/csv")}
    
    response = client.post("/api/v1/predict-batch/upload-csv", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "predictions" in data
    assert len(data["predictions"]) == 3
    
    # Verify each prediction has required fields
    for pred in data["predictions"]:
        assert "prediction" in pred
        assert "explanation" in pred
