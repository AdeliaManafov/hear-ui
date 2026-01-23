#!/usr/bin/env python3
"""Comprehensive API validation and consistency checks."""
import json
import requests
from typing import Dict, Any

BASE_URL = 'http://localhost:8000/api/v1'

class APITester:
    def __init__(self):
        self.results = []
        self.errors = []
        
    def test(self, name: str, method: str, path: str, data: Dict = None, expected_status: int = 200):
        """Test an API endpoint."""
        url = BASE_URL + path
        try:
            if method == 'GET':
                r = requests.get(url, timeout=5)
            elif method == 'POST':
                r = requests.post(url, json=data, timeout=5)
            elif method == 'PUT':
                r = requests.put(url, json=data, timeout=5)
            elif method == 'DELETE':
                r = requests.delete(url, timeout=5)
            
            passed = r.status_code == expected_status
            status_icon = '✅' if passed else '❌'
            
            result = {
                'name': name,
                'method': method,
                'path': path,
                'status_code': r.status_code,
                'expected': expected_status,
                'passed': passed,
                'response': r.json() if r.status_code < 500 else None
            }
            self.results.append(result)
            
            print(f'{status_icon} {name:30s} {method:6s} {r.status_code} (expected {expected_status})')
            
            return result
            
        except Exception as e:
            self.errors.append({'name': name, 'error': str(e)})
            print(f'❌ {name:30s} ERROR: {e}')
            return None
    
    def validate_consistency(self):
        """Validate prediction consistency."""
        print('\n' + '='*80)
        print('KONSISTENZ-VALIDIERUNG')
        print('='*80)
        
        # Test 1: Same input should give same prediction
        print('\n1. Identische Eingaben sollten identische Vorhersagen liefern:')
        test_input = {'Alter [J]': 45, 'Geschlecht': 'w', 'Primäre Sprache': 'Deutsch'}
        
        pred1 = requests.post(f'{BASE_URL}/predict/', json=test_input).json()['prediction']
        pred2 = requests.post(f'{BASE_URL}/predict/', json=test_input).json()['prediction']
        
        if abs(pred1 - pred2) < 0.0001:
            print(f'   ✅ Konsistent: {pred1:.6f} == {pred2:.6f}')
        else:
            print(f'   ❌ INKONSISTENT: {pred1:.6f} != {pred2:.6f}')
            self.errors.append({'test': 'consistency', 'values': [pred1, pred2]})
        
        # Test 2: Explainer prediction should match predict endpoint
        print('\n2. Explainer-Vorhersage sollte mit Predict-Endpunkt übereinstimmen:')
        pred_result = requests.post(f'{BASE_URL}/predict/', json=test_input).json()
        expl_result = requests.post(f'{BASE_URL}/explainer/explain', json=test_input).json()
        
        pred_val = pred_result['prediction']
        expl_val = expl_result['prediction']
        
        if abs(pred_val - expl_val) < 0.0001:
            print(f'   ✅ Konsistent: Predict={pred_val:.6f}, Explainer={expl_val:.6f}')
        else:
            print(f'   ❌ INKONSISTENT: Predict={pred_val:.6f}, Explainer={expl_val:.6f}')
            self.errors.append({'test': 'predict_vs_explainer', 'values': [pred_val, expl_val]})
        
        # Test 3: Empty input should give base prediction
        print('\n3. Leere Eingabe sollte Basis-Vorhersage liefern:')
        empty_result = requests.post(f'{BASE_URL}/explainer/explain', json={}).json()
        base_value = empty_result['base_value']
        prediction = empty_result['prediction']
        
        # Convert logit to probability
        import math
        expected_prob = 1 / (1 + math.exp(-base_value))
        
        if abs(prediction - expected_prob) < 0.01:
            print(f'   ✅ Plausibel: Base={base_value:.4f} → Prob={prediction:.1%} (erwartet {expected_prob:.1%})')
        else:
            print(f'   ⚠️  Abweichung: Base={base_value:.4f} → Prob={prediction:.1%} (erwartet {expected_prob:.1%})')
        
        # Test 4: Check feature contributions sum correctly
        print('\n4. Feature-Beiträge sollten zur Vorhersage passen:')
        fi = expl_result['feature_importance']
        total_contribution = sum(fi.values())
        logit = base_value + total_contribution
        expected_prob_from_fi = 1 / (1 + math.exp(-logit))
        
        if abs(expl_val - expected_prob_from_fi) < 0.01:
            print(f'   ✅ Konsistent: Σ Features={total_contribution:.4f}, Vorhersage={expl_val:.1%}')
        else:
            print(f'   ⚠️  Abweichung: Base+Σ={logit:.4f} → {expected_prob_from_fi:.1%}, aber Vorhersage={expl_val:.1%}')
        
        # Test 5: Check patient endpoint consistency
        print('\n5. Patienten-Endpunkt Konsistenz:')
        patients = requests.get(f'{BASE_URL}/patients/').json()
        if patients:
            pid = patients[0]['id']
            patient_pred = requests.get(f'{BASE_URL}/patients/{pid}/predict').json()['prediction']
            patient_expl = requests.get(f'{BASE_URL}/patients/{pid}/explainer').json()['prediction']
            
            if abs(patient_pred - patient_expl) < 0.0001:
                print(f'   ✅ Konsistent: Predict={patient_pred:.1%}, Explainer={patient_expl:.1%}')
            else:
                print(f'   ❌ INKONSISTENT: Predict={patient_pred:.1%}, Explainer={patient_expl:.1%}')
                self.errors.append({'test': 'patient_endpoints', 'values': [patient_pred, patient_expl]})
    
    def check_defaults(self):
        """Check that defaults don't inflate predictions."""
        print('\n' + '='*80)
        print('DEFAULT-WERTE ÜBERPRÜFUNG')
        print('='*80)
        
        # Test minimal vs empty input
        minimal = {'Alter [J]': 30}
        empty = {}
        
        minimal_result = requests.post(f'{BASE_URL}/explainer/explain', json=minimal).json()
        empty_result = requests.post(f'{BASE_URL}/explainer/explain', json=empty).json()
        
        print(f'\nLeere Eingabe: {empty_result["prediction"]:.1%}')
        print(f'Nur Alter=30:  {minimal_result["prediction"]:.1%}')
        
        # Check which features are active
        minimal_fi = minimal_result['feature_importance']
        active_features = {k: v for k, v in minimal_fi.items() if abs(v) > 0.01}
        
        print(f'\nAktive Features (nur Alter=30): {len(active_features)}')
        for feat, imp in sorted(active_features.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
            print(f'  {feat[:50]:52s} {imp:+.4f}')
        
        # Check for problematic defaults
        problematic = [
            'Objektive Messungen.LL..._Nicht erhoben',
            'Objektive Messungen.4000 Hz..._Nicht erhoben',
            'Diagnose.Höranamnese.Ursache....Ursache..._unknown',
            'Diagnose.Höranamnese.Erwerbsart..._unknown',
        ]
        
        print('\nProblematische Default-Features (sollten NICHT aktiv sein):')
        any_active = False
        for feat in problematic:
            if feat in active_features:
                print(f'  ❌ AKTIV: {feat} = {active_features[feat]:+.4f}')
                any_active = True
                self.errors.append({'test': 'problematic_defaults', 'feature': feat})
        
        if not any_active:
            print('  ✅ Keine problematischen Defaults aktiv')
    
    def summary(self):
        """Print summary."""
        print('\n' + '='*80)
        print('ZUSAMMENFASSUNG')
        print('='*80)
        
        total_tests = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        failed = total_tests - passed
        
        print(f'\nAPI-Tests: {passed}/{total_tests} bestanden')
        if self.errors:
            print(f'\nFehler gefunden: {len(self.errors)}')
            for err in self.errors:
                print(f'  - {err}')
        else:
            print('\n✅ Alle Validierungen bestanden!')

if __name__ == '__main__':
    tester = APITester()
    
    print('='*80)
    print('UMFASSENDE API-VALIDIERUNG')
    print('='*80)
    print()
    
    # Get patient ID for tests
    patients = requests.get(f'{BASE_URL}/patients/').json()
    pid = patients[0]['id'] if patients else None
    
    # Core API tests
    print('KERN-API-ENDPUNKTE:')
    print('-'*80)
    tester.test('Model Info', 'GET', '/utils/model-info')
    tester.test('Patienten Liste', 'GET', '/patients/')
    
    if pid:
        tester.test('Patient Details', 'GET', f'/patients/{pid}')
        tester.test('Patient Vorhersage', 'GET', f'/patients/{pid}/predict')
        tester.test('Patient Explainer', 'GET', f'/patients/{pid}/explainer')
    
    tester.test('Predict (POST)', 'POST', '/predict/', {'Alter [J]': 45, 'Geschlecht': 'w'})
    tester.test('Explainer (POST)', 'POST', '/explainer/explain', {'Alter [J]': 45})
    
    # Validation tests
    tester.validate_consistency()
    tester.check_defaults()
    
    # Summary
    tester.summary()
