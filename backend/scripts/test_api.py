#!/usr/bin/env python3
"""Comprehensive API tests for HEAR backend."""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

def print_section(title: str):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def run_endpoint(name: str, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict:
    """Test an endpoint and return response."""
    url = f"{BASE_URL}/{endpoint}"
    
    print(f"\n🧪 Testing: {name}")
    print(f"   {method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            print(f"   Payload: {json.dumps(data, indent=2)}")
            response = requests.post(url, json=data, timeout=30)
        
        print(f"   Status: {response.status_code}", end="")
        
        if response.status_code == 200:
            print(" ✅")
        elif response.status_code < 500:
            print(" ⚠️")
        else:
            print(" ❌")
        
        try:
            result = response.json()
            print(f"   Response preview: {json.dumps(result, indent=2)[:200]}...")
            return {"status": response.status_code, "data": result}
        except:
            print(f"   Response (text): {response.text[:100]}")
            return {"status": response.status_code, "data": response.text}
            
    except requests.exceptions.Timeout:
        print("   ❌ TIMEOUT")
        return {"status": 408, "error": "Timeout"}
    except requests.exceptions.ConnectionError:
        print("   ❌ CONNECTION ERROR")
        return {"status": 503, "error": "Connection refused"}
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return {"status": 500, "error": str(e)}


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         HEAR BACKEND - COMPREHENSIVE TEST SUITE         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    results = {}
    
    # ==================== HEALTH CHECKS ====================
    print_section("1️⃣  HEALTH & INFO ENDPOINTS")
    
    results['health'] = run_endpoint(
        "Health Check",
        "GET",
        "utils/health-check/"
    )
    
    results['model_info'] = run_endpoint(
        "Model Info",
        "GET",
        "utils/model-info/"
    )
    
    # ==================== PREDICTION TESTS ====================
    print_section("2️⃣  PREDICTION ENDPOINT")
    
    # Test 1: Simple prediction
    results['predict_simple'] = run_endpoint(
        "Simple Prediction",
        "POST",
        "predict/",
        {
            "age": 45,
            "hearing_loss_duration": 5,
            "implant_type": "type_a"
        }
    )
    
    # Test 2: Different patient profile
    results['predict_varied'] = run_endpoint(
        "Varied Profile",
        "POST",
        "predict/",
        {
            "age": 65,
            "hearing_loss_duration": 15,
            "implant_type": "type_b"
        }
    )
    
    # ==================== SHAP TESTS ====================
    print_section("3️⃣  SHAP EXPLANATION ENDPOINT")
    
    # Test 1: Full SHAP with all fields
    results['shap_full'] = run_endpoint(
        "Full SHAP Request",
        "POST",
        "shap/explain",
        {
            "Alter [J]": 45,
            "Geschlecht": "w",
            "Primäre Sprache": "Deutsch",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
            "Symptome präoperativ.Tinnitus...": "ja",
            "Behandlung/OP.CI Implantation": "Cochlear"
        }
    )
    
    # Test 2: Different profile for SHAP
    results['shap_different'] = run_endpoint(
        "Different Profile SHAP",
        "POST",
        "shap/explain",
        {
            "Alter [J]": 30,
            "Geschlecht": "m",
            "Primäre Sprache": "Englisch",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "praelingual",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Genetisch",
            "Symptome präoperativ.Tinnitus...": "nein",
            "Behandlung/OP.CI Implantation": "Med-El"
        }
    )
    
    # ==================== VALIDATION ====================
    print_section("4️⃣  RESPONSE VALIDATION")
    
    validation_passed = True
    
    # Validate prediction response
    if results['predict_simple']['status'] == 200:
        pred_data = results['predict_simple']['data']
        if 'prediction' in pred_data:
            pred_val = pred_data['prediction']
            if 0 <= pred_val <= 1:
                print(f"✅ Prediction value valid: {pred_val:.4f}")
            else:
                print(f"❌ Prediction out of range: {pred_val}")
                validation_passed = False
        else:
            print("❌ Missing 'prediction' key")
            validation_passed = False
    
    # Validate SHAP response
    if results['shap_full']['status'] == 200:
        shap_data = results['shap_full']['data']
        
        required_keys = ['prediction', 'feature_importance', 'top_features']
        for key in required_keys:
            if key in shap_data:
                print(f"✅ SHAP has '{key}'")
            else:
                print(f"❌ SHAP missing '{key}'")
                validation_passed = False
        
        # Check feature importances
        if 'feature_importance' in shap_data:
            fi = shap_data['feature_importance']
            if isinstance(fi, dict) and len(fi) > 0:
                print(f"✅ Feature importance has {len(fi)} features")
                # Show top 3
                sorted_fi = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)
                print("   Top 3 features:")
                for feat, imp in sorted_fi[:3]:
                    print(f"     - {feat}: {imp:+.4f}")
            else:
                print("⚠️  Feature importance is empty or invalid")
                validation_passed = False
        
        # Check top features
        if 'top_features' in shap_data:
            top_f = shap_data['top_features']
            if isinstance(top_f, list) and len(top_f) > 0:
                print(f"✅ Top features list has {len(top_f)} items")
            else:
                print("⚠️  Top features list is empty")
    
    # ==================== SUMMARY ====================
    print_section("📊 TEST SUMMARY")
    
    total_tests = len([k for k in results.keys() if not k.startswith('_')])
    passed_tests = len([r for r in results.values() if r.get('status') == 200])
    
    print(f"\nTotal endpoints tested: {total_tests}")
    print(f"Successful (200): {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    
    if passed_tests == total_tests and validation_passed:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit(main())
