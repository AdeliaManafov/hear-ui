#!/usr/bin/env python3
"""Validate prediction logic and consistency"""
import requests
import json
import csv
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

def get_all_patients():
    """Get all patients from API"""
    r = requests.get(f"{BASE_URL}/patients/", params={"skip": 0, "limit": 100})
    return r.json()

def get_patient_csv_data():
    """Load original CSV data"""
    csv_path = Path(__file__).parent / "patientsData" / "sample_patients.csv"
    patients = []
    with open(csv_path, newline='', encoding='utf-8-sig') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if all((v is None or str(v).strip() == '') for v in row.values()):
                continue
            patients.append(row)
    return patients

def analyze_prediction_logic():
    """Analyze if predictions are logical based on patient features"""
    print("=" * 80)
    print("PREDICTION LOGIC VALIDATION")
    print("=" * 80)
    print()
    
    # Get patients from API
    api_patients = get_all_patients()
    csv_patients = get_patient_csv_data()
    
    print(f"Found {len(api_patients)} patients in API")
    print(f"Found {len(csv_patients)} patients in CSV")
    print()
    
    results = []
    
    for idx, patient in enumerate(api_patients):
        pid = patient['id']
        display_name = patient.get('display_name', 'Unknown')
        features = patient.get('input_features', {})
        
        print("-" * 80)
        print(f"PATIENT {idx+1}: {display_name} (ID: {pid[:8]}...)")
        print("-" * 80)
        
        # Get prediction
        r = requests.get(f"{BASE_URL}/patients/{pid}/predict")
        if r.status_code != 200:
            print(f"  [FAIL] Failed to get prediction: {r.status_code}")
            continue
        
        pred_data = r.json()
        prediction = pred_data.get('prediction', 0)
        
        # Get SHAP explanation
        r = requests.get(f"{BASE_URL}/patients/{pid}/explainer")
        if r.status_code != 200:
            print(f"  [FAIL] Failed to get SHAP: {r.status_code}")
            continue
        
        shap_data = r.json()
        base_value = shap_data.get('base_value', 0)
        shap_values = shap_data.get('shap_values', [])
        feature_names = shap_data.get('feature_names', [])
        
        # Analyze key features
        print(f"\n Prediction: {prediction:.4f} ({prediction*100:.2f}%)")
        print(f"   Base value: {base_value:.4f}")
        
        # Show key patient features
        print(f"\n Key Patient Features:")
        age = features.get('Alter [J]', 'N/A')
        gender = features.get('Geschlecht', 'N/A')
        side = features.get('Seiten', 'N/A')
        print(f"   Alter: {age} Jahre")
        print(f"   Geschlecht: {gender}")
        print(f"   Seite: {side}")
        
        # Clinical features
        tinnitus = features.get('Symptome präoperativ.Tinnitus...', 'N/A')
        schwindel = features.get('Symptome präoperativ.Schwindel...', 'N/A')
        print(f"   Tinnitus: {tinnitus}")
        print(f"   Schwindel: {schwindel}")
        
        # Diagnosis
        beginn = features.get('Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...', 'N/A')
        hoerminderung = features.get('Diagnose.Höranamnese.Hörminderung operiertes Ohr...', 'N/A')
        print(f"   Beginn Hörminderung: {beginn}")
        print(f"   Hörminderung Grad: {hoerminderung}")
        
        # Treatment
        ci = features.get('Behandlung/OP.CI Implantation', 'N/A')
        print(f"   CI Implantation: {ci}")
        
        # Outcome measurements
        pre_measure = features.get('outcome_measurments.pre.measure.', 'N/A')
        post12 = features.get('outcome_measurments.post12.measure.', 'N/A')
        post24 = features.get('outcome_measurments.post24.measure.', 'N/A')
        print(f"   Pre-OP Measure: {pre_measure}")
        print(f"   Post-12 Measure: {post12}")
        print(f"   Post-24 Measure: {post24}")
        
        # Top SHAP contributions
        if isinstance(shap_values, list) and len(shap_values) == len(feature_names):
            # Create feature -> value mapping
            contributions = list(zip(feature_names, shap_values))
            # Sort by absolute contribution
            top_contribs = sorted(contributions, key=lambda x: abs(x[1]), reverse=True)[:10]
            
            print(f"\n Top 10 Feature Contributions (SHAP):")
            for feat, val in top_contribs:
                direction = "+" if val > 0 else "-"
                print(f"   {direction} {feat[:60]:<60} {val:+.6f}")
        
        # Logical checks
        print(f"\n[OK] Logical Checks:")
        checks = []
        
        # Check 1: Prediction in valid range
        if 0 <= prediction <= 1:
            checks.append(("[OK]", "Prediction in [0, 1] range"))
        else:
            checks.append(("[FAIL]", f"Prediction OUT OF RANGE: {prediction}"))
        
        # Check 2: Clipping check
        if prediction > 0.99:
            checks.append(("[WARNING]", f"Prediction > 99% (should be clipped): {prediction*100:.2f}%"))
        elif prediction < 0.01:
            checks.append(("[WARNING]", f"Prediction < 1% (should be clipped): {prediction*100:.2f}%"))
        else:
            checks.append(("[OK]", "Prediction within clipping bounds [1%, 99%]"))
        
        # Check 3: Pre-op measure correlation
        if pre_measure != 'N/A' and pre_measure:
            try:
                pre_val = float(pre_measure)
                if pre_val > 50 and prediction > 0.5:
                    checks.append(("[OK]", f"High pre-op score ({pre_val}) → High prediction ({prediction*100:.1f}%)"))
                elif pre_val < 20 and prediction < 0.5:
                    checks.append(("[OK]", f"Low pre-op score ({pre_val}) → Low prediction ({prediction*100:.1f}%)"))
                elif pre_val > 50 and prediction < 0.3:
                    checks.append(("[WARNING]", f"High pre-op score ({pre_val}) but LOW prediction ({prediction*100:.1f}%) - unexpected"))
                elif pre_val < 20 and prediction > 0.7:
                    checks.append(("[WARNING]", f"Low pre-op score ({pre_val}) but HIGH prediction ({prediction*100:.1f}%) - unexpected"))
            except:
                pass
        
        # Check 4: Post-measure consistency (if available)
        if post12 != 'N/A' and post12 and pre_measure != 'N/A' and pre_measure:
            try:
                post_val = float(post12)
                pre_val = float(pre_measure)
                improvement = post_val - pre_val
                
                if improvement > 20 and prediction > 0.6:
                    checks.append(("[OK]", f"Large improvement ({improvement:+.0f}) matches high prediction"))
                elif improvement < 0 and prediction < 0.4:
                    checks.append(("[OK]", f"No improvement ({improvement:+.0f}) matches low prediction"))
                elif improvement > 20 and prediction < 0.3:
                    checks.append(("[WARNING]", f"Large improvement ({improvement:+.0f}) but LOW prediction - model may be wrong"))
                elif improvement < 0 and prediction > 0.7:
                    checks.append(("[WARNING]", f"No improvement ({improvement:+.0f}) but HIGH prediction - model may be wrong"))
            except:
                pass
        
        for icon, check in checks:
            print(f"   {icon} {check}")
        
        # Store results
        results.append({
            'name': display_name,
            'prediction': prediction,
            'checks': checks,
            'features': features
        })
        
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    predictions = [r['prediction'] for r in results]
    print(f" Prediction Statistics:")
    print(f"   Min:    {min(predictions)*100:.2f}%")
    print(f"   Max:    {max(predictions)*100:.2f}%")
    print(f"   Mean:   {sum(predictions)/len(predictions)*100:.2f}%")
    print(f"   Median: {sorted(predictions)[len(predictions)//2]*100:.2f}%")
    print()
    
    # Clipping violations
    over_99 = [r for r in results if r['prediction'] > 0.99]
    under_01 = [r for r in results if r['prediction'] < 0.01]
    
    if over_99:
        print(f"[WARNING]  {len(over_99)} patient(s) exceed 99% threshold:")
        for r in over_99:
            print(f"   - {r['name']}: {r['prediction']*100:.2f}%")
    
    if under_01:
        print(f"[WARNING]  {len(under_01)} patient(s) below 1% threshold:")
        for r in under_01:
            print(f"   - {r['name']}: {r['prediction']*100:.2f}%")
    
    if not over_99 and not under_01:
        print("[OK] All predictions within clipping bounds [1%, 99%]")
    
    print()
    
    # Consistency check
    print(" Consistency Check:")
    print("   Running same prediction twice to check determinism...")
    
    if api_patients:
        pid = api_patients[0]['id']
        r1 = requests.get(f"{BASE_URL}/patients/{pid}/predict")
        r2 = requests.get(f"{BASE_URL}/patients/{pid}/predict")
        
        pred1 = r1.json().get('prediction', 0)
        pred2 = r2.json().get('prediction', 0)
        
        if abs(pred1 - pred2) < 1e-10:
            print(f"   [OK] Deterministic: {pred1:.10f} == {pred2:.10f}")
        else:
            print(f"   [FAIL] Non-deterministic: {pred1:.10f} != {pred2:.10f}")
    
    print()
    print("=" * 80)
    print("[OK] VALIDATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    analyze_prediction_logic()
