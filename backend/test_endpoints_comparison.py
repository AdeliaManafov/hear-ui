"""Quick test to compare /predict/simple vs /explainer/explain predictions."""

import requests

BASE_URL = "http://localhost:8000/api/v1"

# Test data
test_cases = [
    {
        "name": "Minimal data",
        "data": {"Alter [J]": 45},
    },
    {
        "name": "With gender",
        "data": {"Alter [J]": 45, "Geschlecht": "m"},
    },
    {
        "name": "More fields",
        "data": {
            "Alter [J]": 65,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Symptome präoperativ.Tinnitus...": "nein",
            "Behandlung/OP.CI Implantation": "Cochlear",
        },
    },
]

for test in test_cases:
    print(f"\n{'=' * 60}")
    print(f"Test: {test['name']}")
    print(f"Data: {test['data']}")
    print(f"{'=' * 60}")

    # Test /predict/simple
    try:
        resp1 = requests.post(f"{BASE_URL}/predict/simple", json=test["data"], timeout=5)
        if resp1.ok:
            pred1 = resp1.json().get("prediction")
            print(f"✓ /predict/simple:       {pred1:.4f} ({pred1*100:.1f}%)")
        else:
            print(f"✗ /predict/simple:       Error {resp1.status_code}: {resp1.text[:100]}")
    except Exception as e:
        print(f"✗ /predict/simple:       Exception: {e}")

    # Test /explainer/explain
    try:
        resp2 = requests.post(
            f"{BASE_URL}/explainer/explain?method=shap&include_plot=false",
            json=test["data"],
            timeout=10,
        )
        if resp2.ok:
            data = resp2.json()
            pred2 = data.get("prediction")
            print(f"✓ /explainer/explain:    {pred2:.4f} ({pred2*100:.1f}%)")

            # Check if predictions match
            if pred1 and pred2 and abs(pred1 - pred2) < 0.001:
                print(f"  ✓ Predictions MATCH")
            else:
                print(f"  ✗ Predictions DIFFER: Δ = {abs(pred1 - pred2):.6f}")
                
            # Show top 3 features from explanation
            if "feature_importance" in data:
                features = sorted(
                    data["feature_importance"].items(), key=lambda x: abs(x[1]), reverse=True
                )[:3]
                print(f"  Top features:")
                for feat, importance in features:
                    print(f"    {feat[:50]}: {importance:+.3f}")
        else:
            print(f"✗ /explainer/explain:    Error {resp2.status_code}: {resp2.text[:100]}")
    except Exception as e:
        print(f"✗ /explainer/explain:    Exception: {e}")

print(f"\n{'=' * 60}")
print("Test complete")
