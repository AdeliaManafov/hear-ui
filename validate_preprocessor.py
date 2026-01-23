#!/usr/bin/env python3
"""Validate preprocessor logic and edge cases."""
import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

print('='*80)
print('PREPROCESSOR-LOGIK VALIDIERUNG')
print('='*80)

# Test cases with different feature combinations
test_cases = [
    {
        'name': 'Komplett leer',
        'data': {},
        'expected_range': (0.25, 0.40)  # Should be around base intercept
    },
    {
        'name': 'Nur Alter',
        'data': {'Alter [J]': 30},
        'expected_range': (0.25, 0.45)
    },
    {
        'name': 'Alter + Geschlecht',
        'data': {'Alter [J]': 45, 'Geschlecht': 'w'},
        'expected_range': (0.25, 0.50)
    },
    {
        'name': 'Mit CI-Implantation',
        'data': {
            'Alter [J]': 50,
            'Geschlecht': 'w',
            'Behandlung/OP.CI Implantation': 'Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile CI532 (Slim Modiolar)'
        },
        'expected_range': (0.50, 1.0)
    },
    {
        'name': 'Mit LL-Messung (explicit)',
        'data': {
            'Alter [J]': 40,
            'Objektive Messungen.LL...': 'Keine Reizantwort'
        },
        'expected_range': (0.20, 0.80)
    },
    {
        'name': 'Mit unknown Ursache (explicit)',
        'data': {
            'Alter [J]': 45,
            'Diagnose.Höranamnese.Ursache....Ursache...': 'unknown'
        },
        'expected_range': (0.10, 0.50)
    }
]

print('\nTest-Fälle:')
print('-'*80)

for i, test in enumerate(test_cases, 1):
    r = requests.post(f'{BASE_URL}/explainer/explain', json=test['data'])
    if r.status_code == 200:
        result = r.json()
        pred = result['prediction']
        expected_min, expected_max = test['expected_range']
        
        # Check prediction range
        in_range = expected_min <= pred <= expected_max
        status = '✅' if in_range else '⚠️'
        
        # Count active features
        fi = result['feature_importance']
        active_count = sum(1 for v in fi.values() if abs(v) > 0.001)
        
        print(f'{i}. {test["name"]:30s} → {pred:.1%} ({active_count} Features aktiv) {status}')
        
        # Show top contributors
        top3 = sorted(fi.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
        for feat, val in top3:
            if abs(val) > 0.001:
                print(f'     {feat[:45]:47s} {val:+.4f}')
    else:
        print(f'{i}. {test["name"]:30s} → ERROR {r.status_code}')

# Check that explicit "Nicht erhoben" activates the feature
print('\n' + '='*80)
print('EXPLICIT vs IMPLICIT Defaults')
print('='*80)

# Without explicit value (should NOT activate "Nicht erhoben")
implicit = requests.post(f'{BASE_URL}/explainer/explain', json={'Alter [J]': 40}).json()
implicit_fi = implicit['feature_importance']

# With explicit "Nicht erhoben" (SHOULD activate)
explicit = requests.post(f'{BASE_URL}/explainer/explain', json={
    'Alter [J]': 40,
    'Objektive Messungen.LL...': 'Nicht erhoben'
}).json()
explicit_fi = explicit['feature_importance']

ll_feat = 'Objektive Messungen.LL..._Nicht erhoben'

print(f'\nImplicit (keine LL-Angabe):')
print(f'  {ll_feat}: {implicit_fi.get(ll_feat, 0):.4f}')
print(f'  Vorhersage: {implicit["prediction"]:.1%}')

print(f'\nExplicit ("Nicht erhoben" angegeben):')
print(f'  {ll_feat}: {explicit_fi.get(ll_feat, 0):.4f}')
print(f'  Vorhersage: {explicit["prediction"]:.1%}')

if abs(implicit_fi.get(ll_feat, 0)) < 0.001 and abs(explicit_fi.get(ll_feat, 0)) > 0.1:
    print('\n✅ KORREKT: Implicit setzt KEINE Defaults, Explicit aktiviert Features')
else:
    print(f'\n❌ FEHLER: Implicit={implicit_fi.get(ll_feat, 0):.4f}, Explicit={explicit_fi.get(ll_feat, 0):.4f}')

# Edge case: all fields explicitly set to None/empty
print('\n' + '='*80)
print('EDGE CASES')
print('='*80)

edge_cases = [
    ('Null values', {'Alter [J]': None, 'Geschlecht': None}),
    ('Empty strings', {'Primäre Sprache': '', 'Geschlecht': ''}),
    ('Mixed null/empty', {'Alter [J]': 30, 'Geschlecht': None, 'Primäre Sprache': ''}),
]

for name, data in edge_cases:
    r = requests.post(f'{BASE_URL}/predict/', json=data)
    if r.status_code == 200:
        pred = r.json()['prediction']
        print(f'✅ {name:20s} → {pred:.1%}')
    else:
        print(f'❌ {name:20s} → ERROR {r.status_code}')

print('\n' + '='*80)
