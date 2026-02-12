#!/usr/bin/env python3
"""Vergleiche beide Explainer-Endpoints"""

import json
import requests

patient_data = {
    "Alter [J]": 30,
    "Geschlecht": "w",
    "Primäre Sprache": "Deutsch",
    "Seiten": "L", 
    "Symptome präoperativ.Tinnitus...": "Vorhanden",
    "Symptome präoperativ.Schwindel...": "Kein",
    "outcome_measurments.pre.measure.": 40,
    "abstand": 828,
}

print("=" * 70)
print("COMPARISON: /explainer/explain vs /patients/{id}/explainer")
print("=" * 70)

# Test 1: /explainer/explain endpoint
print("\n1️⃣  Testing: /api/v1/explainer/explain")
try:
    response = requests.post(
        "http://localhost:8000/api/v1/explainer/explain",
        json=patient_data,
        timeout=30,
    )
    
    if response.status_code == 200:
        data = response.json()
        feature_importance = data.get("feature_importance", {})
        
        # Count positive and negative
        positive = sum(1 for v in feature_importance.values() if v > 0)
        negative = sum(1 for v in feature_importance.values() if v < 0)
        
        print(f"   Status: ✅ SUCCESS")
        print(f"   Prediction: {data.get('prediction', 'N/A'):.3f}")
        print(f"   Positive contributions: {positive}")
        print(f"   Negative contributions: {negative}")
        
        # Show top 5
        sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
        print(f"\n   Top 5 features:")
        for i, (name, val) in enumerate(sorted_features, 1):
            direction = "🟢" if val > 0 else "🔴" if val < 0 else "⚪"
            print(f"     {i}. {direction} {name[:40]:40s}: {val:+.4f}")
    else:
        print(f"   Status: ❌ FAILED ({response.status_code})")
        print(f"   {response.text}")
except Exception as e:
    print(f"   Exception: {e}")

# Test 2: Create patient and use /patients/{id}/explainer
print("\n\\n2️⃣  Testing: /api/v1/patients/{id}/explainer") 
try:
    # Create patient first
    create_response = requests.post(
        "http://localhost:8000/api/v1/patients/",
        json={
            "display_name": "Test Patient for Comparison",
            "input_features": patient_data
        },
        timeout=10
    )
    
    if create_response.status_code == 200:
        patient_id = create_response.json()["id"]
        print(f"   Created patient: {patient_id}")
        
        # Test explainer endpoint
        response = requests.get(
            f"http://localhost:8000/api/v1/patients/{patient_id}/explainer",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            feature_importance = data.get("feature_importance", {})
            
            # Count positive and negative
            positive = sum(1 for v in feature_importance.values() if v > 0)
            negative = sum(1 for v in feature_importance.values() if v < 0)
            
            print(f"   Status: ✅ SUCCESS")
            print(f"   Prediction: {data.get('prediction', 'N/A'):.3f}")
            print(f"   Positive contributions: {positive}")
            print(f"   Negative contributions: {negative}")
            
            # Show top 5
            sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)[:5]
            print(f"\n   Top 5 features:")
            for i, (name, val) in enumerate(sorted_features, 1):
                direction = "🟢" if val > 0 else "🔴" if val < 0 else "⚪"
                print(f"     {i}. {direction} {name[:40]:40s}: {val:+.4f}")
        else:
            print(f"   Status: ❌ FAILED ({response.status_code})")
            print(f"   {response.text}")
    else:
        print(f"   Status: ❌ Failed to create patient ({create_response.status_code})")
        print(f"   {create_response.text}")
except Exception as e:
    print(f"   Exception: {e}")

print("\\n" + "=" * 70)
