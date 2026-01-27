from fastapi.testclient import TestClient
from app.main import app
from app.core.model_wrapper import ModelWrapper

wrapper = ModelWrapper()
wrapper.load()
app.state.model_wrapper = wrapper
client = TestClient(app)

print("=" * 60)
print("TESTING ALL IMPROVEMENTS")
print("=" * 60)

# 1. Global Health Endpoint
print("\n[TEST 1] Global /health Endpoint")
r = client.get("/health")
print(f"  GET /health -> Status: {r.status_code}, Body: {r.json()}")
assert r.status_code == 200

# 2. Utils Health Check
print("\n[TEST 2] Utils Health Check")
r = client.get("/api/v1/utils/health-check/")
print(f"  Status: {r.status_code}")
assert r.status_code == 200

# 3. Explainer /explain
print("\n[TEST 3] Explainer /explain")
r = client.post("/api/v1/explainer/explain", json={"age": 50, "gender": "m", "include_plot": False})
print(f"  Status: {r.status_code}, Prediction: {r.json().get('prediction', 'N/A')}")
assert r.status_code == 200

# 4. Explainer /shap alias
print("\n[TEST 4] Explainer /shap Alias")
r = client.post("/api/v1/explainer/shap", json={"age": 50, "gender": "m", "include_plot": False})
print(f"  Status: {r.status_code}")
assert r.status_code == 200

# 5. Predict
print("\n[TEST 5] Predict Endpoint")
r = client.post("/api/v1/predict/", json={"age": 50, "gender": "m"})
print(f"  Status: {r.status_code}, Prediction: {r.json().get('prediction', 'N/A')}")
assert r.status_code == 200

# 6. Patients
print("\n[TEST 6] Patients CRUD")
r = client.get("/api/v1/patients/")
print(f"  Status: {r.status_code}, Count: {len(r.json())}")
assert r.status_code == 200

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
