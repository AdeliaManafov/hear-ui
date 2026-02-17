#!/usr/bin/env python3
"""Test SHAP explanation to verify positive AND negative contributions."""

import sys

import requests

# Test patient data
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
print("Testing SHAP Explanation (should show BOTH positive AND negative values)")
print("=" * 70)

# Test /explainer endpoint
try:
    response = requests.post(
        "http://localhost:8000/api/v1/explainer/explain",
        json=patient_data,
        timeout=30,
    )

    if response.status_code == 200:
        data = response.json()
        feature_importance = data.get("feature_importance", {})

        print(f"\n✓ Prediction: {data.get('prediction', 'N/A'):.3f}")
        print(f"✓ Base value: {data.get('base_value', 'N/A'):.3f}")
        print("\n📊 Top 10 Feature Contributions (SHAP values):")

        # Sort by absolute value
        sorted_features = sorted(
            feature_importance.items(), key=lambda x: abs(x[1]), reverse=True
        )[:10]

        positive_count = 0
        negative_count = 0

        for i, (feature_name, contribution) in enumerate(sorted_features, 1):
            direction = "🟢" if contribution > 0 else "🔴" if contribution < 0 else "⚪"
            print(f"  {i:2d}. {direction} {feature_name:40s}: {contribution:+.4f}")

            if contribution > 0:
                positive_count += 1
            elif contribution < 0:
                negative_count += 1

        print("\n" + "=" * 70)
        print(f"Positive contributions: {positive_count}")
        print(f"Negative contributions: {negative_count}")
        print(f"Zero contributions: {10 - positive_count - negative_count}")

        if negative_count > 0:
            print("\n✅ SUCCESS: SHAP shows BOTH positive AND negative contributions!")
        else:
            print(
                "\n⚠️  WARNING: Only positive values detected. SHAP may not be working correctly."
            )

    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Exception occurred: {e}")
    sys.exit(1)
