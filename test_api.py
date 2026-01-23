#!/usr/bin/env python3
"""Test all API endpoints."""
import json
import requests

BASE_URL = 'http://localhost:8000/api/v1'

# Get first patient ID
r = requests.get(f'{BASE_URL}/patients/')
patients = r.json()
pid = patients[0]['id']

print('=' * 80)
print('API ENDPUNKT-TESTS')
print('=' * 80)
print()

tests = [
    ('Health Check', 'GET', '/utils/health', None),
    ('Model Info', 'GET', '/utils/model-info', None),
    ('Patienten Liste', 'GET', '/patients/', None),
    ('Patient Einzeln', 'GET', f'/patients/{pid}', None),
    ('Patient Vorhersage', 'GET', f'/patients/{pid}/predict', None),
    ('Patient Explainer', 'GET', f'/patients/{pid}/explainer', None),
    ('Explainer POST', 'POST', '/explainer/explain', {'Alter [J]': 50, 'Geschlecht': 'w'}),
    ('Predict POST', 'POST', '/predict/', {'Alter [J]': 50, 'Geschlecht': 'w'}),
]

for name, method, path, data in tests:
    url = BASE_URL + path
    try:
        if method == 'GET':
            r = requests.get(url, timeout=5)
        else:
            r = requests.post(url, json=data, timeout=5)
        
        status = 'OK' if r.status_code < 400 else 'FAIL'
        detail = ''
        if r.status_code == 200:
            j = r.json()
            if 'prediction' in j:
                detail = f"({j['prediction']:.1%})"
            elif 'total' in j:
                detail = f"({j['total']} items)"
            elif isinstance(j, list):
                detail = f'({len(j)} items)'
        print(f'{status:4s} {name:25s} {method:4s} {path[:35]:37s} {r.status_code} {detail}')
    except Exception as e:
        print(f'FAIL {name:25s} {method:4s} {path[:35]:37s} ERROR: {e}')

print('=' * 80)
