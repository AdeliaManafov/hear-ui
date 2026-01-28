#!/usr/bin/env python3
"""Update patient display names for demo."""
import requests

API = 'http://localhost:8000/api/v1/patients/'

# Namen für die 5 Demo-Patienten
DEMO_NAMES = [
    "Schmidt, Anna",
    "Müller, Max",
    "Weber, Sofia",
    "Fischer, Paul",
    "Meyer, Lena"
]

# Hole alle Patienten
resp = requests.get(API, timeout=10)
patients = resp.json()
print(f"Found {len(patients)} patients")

# Update Namen
for idx, patient in enumerate(patients[:5]):
    patient_id = patient['id']
    name = DEMO_NAMES[idx] if idx < len(DEMO_NAMES) else f"Patient {idx+1}"
    
    try:
        r = requests.put(
            f"{API}{patient_id}",
            json={"display_name": name},
            timeout=10
        )
        if r.status_code == 200:
            print(f"Updated {patient_id}: {name}")
        else:
            print(f"Failed {patient_id}: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error updating {patient_id}: {e}")

# Verify
resp = requests.get(API, timeout=10)
for p in resp.json():
    print(f"  - {p['display_name']} (ID: {p['id'][:8]}...)")
