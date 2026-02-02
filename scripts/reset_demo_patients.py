#!/usr/bin/env python3
"""Delete all patients and import from CSV for demo presentation."""
import requests
import sys

API = 'http://localhost:8000/api/v1/patients/'

# 1. Get all patient IDs
print("Fetching current patients...")
resp = requests.get(API, timeout=10)
patients = resp.json()
print(f"Found {len(patients)} patients to delete")

# 2. Delete all patients
deleted = 0
for patient in patients:
    patient_id = patient['id']
    try:
        r = requests.delete(f"{API}{patient_id}", timeout=10)
        if r.status_code in (200, 204):
            deleted += 1
        else:
            print(f"Failed to delete {patient_id}: {r.status_code}")
    except Exception as e:
        print(f"Error deleting {patient_id}: {e}")

print(f"Deleted {deleted}/{len(patients)} patients")

# 3. Import from CSV
print("\nImporting patients from CSV...")
import subprocess
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
import_script = os.path.join(script_dir, 'import_patients.py')
result = subprocess.run([sys.executable, import_script], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr, file=sys.stderr)

# 4. Verify
resp = requests.get(API, timeout=10)
final_count = len(resp.json())
print(f"\nFinal patient count: {final_count}")
