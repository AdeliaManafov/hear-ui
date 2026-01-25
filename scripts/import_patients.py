#!/usr/bin/env python3
import csv
import json
from pathlib import Path
import requests

CSV = Path(__file__).resolve().parents[1] / 'patientsData' / 'sample_patients.csv'
API = 'http://localhost:8000/api/v1/patients/'

FEMALE_FIRST_NAMES = [
    "Anna", "Maria", "Lena", "Sofia", "Lea", "Mia", "Emilia", "Hannah",
    "Johanna", "Laura", "Sarah", "Julia"
]
MALE_FIRST_NAMES = [
    "Max", "Paul", "Leon", "Jonas", "Lukas", "Noah", "Ben", "Finn",
    "Elias", "Felix", "Julian", "Tim"
]
LAST_NAMES = [
    "Muster", "Schmidt", "Meyer", "Schneider", "Fischer", "Weber",
    "Wagner", "Becker", "Hoffmann", "Schulz", "Koch", "Bauer"
]


def _pick_name(idx: int, gender: str | None) -> str:
    gender_norm = (gender or "").strip().lower()
    if gender_norm in {"w", "f", "female"}:
        first = FEMALE_FIRST_NAMES[idx % len(FEMALE_FIRST_NAMES)]
    elif gender_norm in {"m", "male"}:
        first = MALE_FIRST_NAMES[idx % len(MALE_FIRST_NAMES)]
    else:
        combined = FEMALE_FIRST_NAMES + MALE_FIRST_NAMES
        first = combined[idx % len(combined)]
    last = LAST_NAMES[idx % len(LAST_NAMES)]
    return f"{last}, {first}"

if not CSV.exists():
    print('CSV not found:', CSV)
    raise SystemExit(1)

with open(CSV, newline='', encoding='utf-8-sig') as fh:
    reader = csv.DictReader(fh)
    count = 0
    row_index = 0
    for row in reader:
        # skip rows that are entirely empty
        if all((v is None or str(v).strip() == '') for v in row.values()):
            continue
        # build input_features: keep all columns except ID as features
        features = {k: (v if v != '' else None) for k, v in row.items()}
        display_name = _pick_name(row_index, features.get("Geschlecht"))
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
        row_index += 1

print('Imported total:', count)
