#!/usr/bin/env python3
import csv
import json
import requests
from pathlib import Path

CSV = Path(__file__).resolve().parents[1] / 'data' / 'sample_patients.csv'
API = 'http://localhost:8000/api/v1/patients/'

if not CSV.exists():
    print('CSV not found:', CSV)
    raise SystemExit(1)

with open(CSV, newline='', encoding='utf-8') as fh:
    reader = csv.DictReader(fh)
    count = 0
    for row in reader:
        # skip rows that are entirely empty
        if all((v is None or str(v).strip() == '') for v in row.values()):
            continue
        # build input_features: keep all columns except ID as features
        features = {k: (v if v != '' else None) for k, v in row.items()}
        display_name = None
        # if there is an ID field, use it for display_name
        if 'ID' in features and features['ID']:
            display_name = f"patient-{features['ID']}"
        payload = {
            'input_features': features,
            'display_name': display_name
        }
        try:
            r = requests.post(API, json=payload, timeout=10)
            if r.status_code in (200, 201):
                print('Created:', r.json().get('id'))
                count += 1
            else:
                print('Failed:', r.status_code, r.text)
        except Exception as e:
            print('Error posting:', e)

print('Imported total:', count)
