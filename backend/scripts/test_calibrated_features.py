#!/usr/bin/env python3
"""Test suite for calibrated model and new feature endpoints."""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_feature_names_endpoint():
    """Test the new /utils/feature-names/ endpoint."""
    print("\n🧪 Testing Feature Names Endpoint")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/utils/feature-names/")
    
    if response.status_code == 200:
        mapping = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Found {len(mapping)} feature mappings")
        print("\n  Sample mappings:")
        for i, (tech, human) in enumerate(list(mapping.items())[:5], 1):
            print(f"    {i}. {tech[:50]:<50} → {human}")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        return False


def test_feature_categories_endpoint():
    """Test the /utils/feature-categories/ endpoint."""
    print("\n🧪 Testing Feature Categories Endpoint")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/utils/feature-categories/")
    
    if response.status_code == 200:
        categories = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"📊 Found {len(categories)} categories")
        print("\n  Categories:")
        for cat_name, features in categories.items():
            print(f"    • {cat_name}: {len(features)} features")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        return False


def test_calibrated_model_predictions():
    """Test predictions with calibrated model."""
    print("\n🧪 Testing Calibrated Model Predictions")
    print("="*70)
    
    # Test with different patient profiles
    test_cases = [
        {
            "name": "Young, postlingual (should be high)",
            "data": {
                "Alter [J]": 25,
                "Geschlecht": "m",
                "Primäre Sprache": "Deutsch",
                "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
                "Symptome präoperativ.Tinnitus...": "nein",
                "Behandlung/OP.CI Implantation": "Cochlear"
            }
        },
        {
            "name": "Older, praelingual (should be lower)",
            "data": {
                "Alter [J]": 65,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
                "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "praelingual",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
                "Symptome präoperativ.Tinnitus...": "ja",
                "Behandlung/OP.CI Implantation": "Med-El"
            }
        },
        {
            "name": "Middle-aged, unknown onset",
            "data": {
                "Alter [J]": 45,
                "Geschlecht": "w",
                "Primäre Sprache": "Deutsch",
                "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "Unbekannt",
                "Diagnose.Höranamnese.Ursache....Ursache...": "Genetisch",
                "Symptome präoperativ.Tinnitus...": "nein",
                "Behandlung/OP.CI Implantation": "Cochlear"
            }
        }
    ]
    
    predictions = []
    
    for i, test in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/predict/",
                json=test["data"],
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                pred = result.get('prediction', 0.0)
                predictions.append(pred)
                
                print(f"\n  Test {i}: {test['name']}")
                print(f"    Prediction: {pred:.4f} ({pred*100:.1f}%)")
            else:
                print(f"\n  Test {i}: ❌ HTTP {response.status_code}")
                
        except Exception as e:
            print(f"\n  Test {i}: ❌ Error: {str(e)[:50]}")
    
    # Check if predictions vary
    if len(predictions) >= 2:
        unique_preds = len(set([round(p, 4) for p in predictions]))
        if unique_preds > 1:
            print(f"\n✅ Predictions vary: {unique_preds} different values")
            print(f"  Range: {min(predictions):.1%} - {max(predictions):.1%}")
            return True
        else:
            print(f"\n⚠️ All predictions are the same!")
            return False
    
    return len(predictions) > 0


def test_shap_with_new_background():
    """Test SHAP endpoint with expanded background data."""
    print("\n🧪 Testing SHAP with Expanded Background")
    print("="*70)
    
    patient_data = {
        "Alter [J]": 45,
        "Geschlecht": "w",
        "Primäre Sprache": "Deutsch",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
        "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
        "Symptome präoperativ.Tinnitus...": "ja",
        "Behandlung/OP.CI Implantation": "Cochlear"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/shap/explain",
            json=patient_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Status: {response.status_code}")
            print(f"  Prediction: {result.get('prediction', 0):.4f}")
            
            fi = result.get('feature_importance', {})
            if fi:
                print(f"  Feature Importances: {len(fi)} features")
                
                # Check if values are non-zero
                non_zero = sum(1 for v in fi.values() if abs(v) > 0.001)
                print(f"  Non-zero importances: {non_zero}/{len(fi)}")
                
                # Show top 3
                sorted_fi = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)
                print("\n  Top 3 features:")
                for feat, imp in sorted_fi[:3]:
                    print(f"    • {feat[:50]}: {imp:+.4f}")
                
                return non_zero > 0
            else:
                print("  ⚠️ No feature importances returned")
                return False
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"  {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("  CALIBRATED MODEL & NEW FEATURES TEST SUITE")
    print("="*70)
    
    # Wait for backend to be ready
    import time
    print("\n⏳ Waiting for backend to be ready...")
    time.sleep(3)
    
    results = {
        "Feature Names Endpoint": test_feature_names_endpoint(),
        "Feature Categories Endpoint": test_feature_categories_endpoint(),
        "Calibrated Model Predictions": test_calibrated_model_predictions(),
        "SHAP with New Background": test_shap_with_new_background()
    }
    
    # Summary
    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
