#!/usr/bin/env python3
"""Test alle API-Endpunkte mit den 5 neuen Patienten."""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 80)
print("API-ENDPUNKT-TESTS")
print("=" * 80)

# 1. Health Check
print("\n1. Health Check")
r = requests.get(f"{BASE_URL}/utils/health-check/")
print(f"   Status: {r.status_code} - {r.json()}")

# 2. Model Info
print("\n2. Model Info")
r = requests.get(f"{BASE_URL}/utils/model-info/")
data = r.json()
print(f"   Status: {r.status_code}")
print(f"   Modell geladen: {data.get('loaded')}")
print(f"   Features: {data.get('n_features')}")

# 3. Feature Names
print("\n3. Feature Names")
r = requests.get(f"{BASE_URL}/utils/feature-names/")
features = r.json()
print(f"   Status: {r.status_code}")
print(f"   Anzahl Features: {len(features.get('features', []))}")

# 4. Liste Patienten
print("\n4. Liste Patienten")
r = requests.get(f"{BASE_URL}/patients/")
patients = r.json()
print(f"   Status: {r.status_code}")
print(f"   Anzahl Patienten: {len(patients)}")

if patients:
    patient_id = patients[0]["id"]
    display_name = patients[0].get("display_name", "Unbenannt")
    
    # 5. Einzelnen Patienten abrufen
    print(f"\n5. Patient abrufen: {display_name}")
    r = requests.get(f"{BASE_URL}/patients/{patient_id}")
    print(f"   Status: {r.status_code}")
    patient = r.json()
    print(f"   Name: {patient.get('display_name')}")
    print(f"   Features: {len(patient.get('input_features', {}))}")
    
    # 6. Validierung
    print(f"\n6. Patient validieren")
    r = requests.get(f"{BASE_URL}/patients/{patient_id}/validate")
    print(f"   Status: {r.status_code}")
    validation = r.json()
    print(f"   Valid: {validation.get('valid')}")
    print(f"   Fehlende Features: {len(validation.get('missing_features', []))}")
    
    # 7. Vorhersage für Patient
    print(f"\n7. Vorhersage für Patient")
    r = requests.get(f"{BASE_URL}/patients/{patient_id}/predict")
    print(f"   Status: {r.status_code}")
    prediction = r.json()
    print(f"   Vorhersage: {prediction.get('prediction', 0):.1%}")
    print(f"   Erklärung vorhanden: {prediction.get('explanation') is not None}")
    
    # 8. SHAP Explanation
    print(f"\n8. SHAP Explanation für Patient")
    r = requests.get(f"{BASE_URL}/patients/{patient_id}/explain")
    print(f"   Status: {r.status_code}")
    explain = r.json()
    print(f"   Prediction: {explain.get('prediction', 0):.1%}")
    print(f"   Top Features: {len(explain.get('top_features', []))}")
    if explain.get('top_features'):
        print(f"   Top 3:")
        for feat in explain['top_features'][:3]:
            print(f"      - {feat['name']}: {feat['value']} (Beitrag: {feat['contribution']:.4f})")

# 9. Direkte Vorhersage (ohne Patient)
print("\n9. Direkte Vorhersage")
test_data = {
    "Alter [J]": 40,
    "Geschlecht": "w",
    "Seiten": "L",
    "outcome_measurments.pre.measure.": 30
}
r = requests.post(f"{BASE_URL}/predict/", json=test_data)
print(f"   Status: {r.status_code}")
result = r.json()
print(f"   Vorhersage: {result.get('prediction', 0):.1%}")

# 10. SHAP Visualisierung
print("\n10. SHAP Visualisierung")
r = requests.post(f"{BASE_URL}/explainer/shap-visualization/", json=test_data)
print(f"   Status: {r.status_code}")
shap_result = r.json()
print(f"   Prediction: {shap_result.get('prediction', 0):.1%}")
print(f"   Top Features: {len(shap_result.get('top_features', []))}")

# 11. Patient erstellen
print("\n11. Neuen Patient erstellen")
new_patient = {
    "display_name": "Test API Patient",
    "input_features": {
        "Alter [J]": 55,
        "Geschlecht": "m"
    }
}
r = requests.post(f"{BASE_URL}/patients/", json=new_patient)
print(f"   Status: {r.status_code}")
if r.status_code in [200, 201]:
    new_id = r.json().get("id")
    print(f"   Erstellt: {new_id}")
    
    # 12. Patient aktualisieren
    print("\n12. Patient aktualisieren")
    update_data = {
        "display_name": "Updated Test Patient"
    }
    r = requests.put(f"{BASE_URL}/patients/{new_id}", json=update_data)
    print(f"   Status: {r.status_code}")
    
    # 13. Patient löschen
    print("\n13. Patient löschen")
    r = requests.delete(f"{BASE_URL}/patients/{new_id}")
    print(f"   Status: {r.status_code}")

# 14. Feedback erstellen
print("\n14. Feedback erstellen")
if patients:
    feedback = {
        "prediction_value": 0.75,
        "patient_input_features": patients[0].get("input_features", {}),
        "feedback_text": "Test-Feedback via API",
        "rating": 4
    }
    r = requests.post(f"{BASE_URL}/feedback/", json=feedback)
    print(f"   Status: {r.status_code}")
    if r.status_code in [200, 201]:
        feedback_id = r.json().get("id")
        print(f"   Erstellt: {feedback_id}")

print("\n" + "=" * 80)
print("ALLE TESTS ABGESCHLOSSEN!")
print("=" * 80)
