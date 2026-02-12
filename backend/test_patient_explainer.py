#!/usr/bin/env python3
"""Test /patients/{id}/explainer endpoint"""

import json

import requests

# Get first patient
try:
    response = requests.get("http://localhost:8000/api/v1/patients/", timeout=10)
    patients = response.json()

    if not patients or len(patients) == 0:
        print("⚠️  No patients in database. Create one first.")
        exit(1)

    patient_id = patients[0]["id"]
    print(f"Testing patient ID: {patient_id}")

    # Test explainer endpoint
    response = requests.get(
        f"http://localhost:8000/api/v1/patients/{patient_id}/explainer", timeout=30
    )

    if response.status_code == 200:
        data = response.json()
        feature_importance = data.get("feature_importance", {})

        print(f"\n✓ Prediction: {data.get('prediction', 'N/A'):.3f}")
        print(f"✓ Total features: {len(feature_importance)}")

        # Sort by absolute value
        sorted_features = sorted(
            feature_importance.items(), key=lambda x: abs(x[1]), reverse=True
        )[:10]

        positive_count = 0
        negative_count = 0
        zero_count = 0

        print("\n📊 Top 10 Features:")
        for i, (feature_name, contribution) in enumerate(sorted_features, 1):
            direction = "🟢" if contribution > 0 else "🔴" if contribution < 0 else "⚪"
            print(f"  {i:2d}. {direction} {feature_name:40s}: {contribution:+.4f}")

            if contribution > 0:
                positive_count += 1
            elif contribution < 0:
                negative_count += 1
            else:
                zero_count += 1

        print("\n" + "=" * 70)
        print(
            f"Positive: {positive_count}, Negative: {negative_count}, Zero: {zero_count}"
        )

        if negative_count > 0:
            print("\n✅ SUCCESS: Endpoint returns positive AND negative values!")
        else:
            print("\n⚠️  WARNING: Only positive values detected!")
            print("\nFull feature_importance dict:")
            print(json.dumps(feature_importance, indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    import traceback

    print(f"❌ Exception: {e}")
    traceback.print_exc()
