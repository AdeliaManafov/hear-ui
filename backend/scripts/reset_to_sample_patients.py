#!/usr/bin/env python3
"""Reset database to only contain the 5 sample patients from sample_patients.csv.

Usage:
  cd backend
  python scripts/reset_to_sample_patients.py

This script will:
1. Delete ALL existing patients from the database
2. Import only the 5 patients from data/sample_patients.csv
3. Set display_name for each patient based on ID
"""
import os
import sys
import csv
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select, text
from app.core.config import settings
from app.db import engine
from app.models import Patient, PatientCreate
from app import crud


CSV_PATH = Path(__file__).parent.parent.parent / "data" / "sample_patients.csv"


def parse_csv_row(row: dict) -> dict:
    """Convert a CSV row to patient input_features dict."""
    # Filter out empty values and clean up keys
    features = {}
    for key, value in row.items():
        if value and str(value).strip():
            # Clean key (remove BOM if present)
            clean_key = key.lstrip('\ufeff').strip()
            features[clean_key] = value.strip()
    return features


def main():
    if not CSV_PATH.exists():
        print(f"❌ CSV file not found: {CSV_PATH}")
        sys.exit(1)
    
    print(f"📂 Using CSV: {CSV_PATH}")
    print(f"📊 Database: {settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}")
    
    # Confirm action
    print("\n⚠️  WARNING: This will DELETE ALL existing patients!")
    confirm = input("Type 'yes' to continue: ")
    if confirm.lower() != 'yes':
        print("Aborted.")
        sys.exit(0)
    
    with Session(engine) as session:
        # Count existing patients
        existing_count = session.exec(select(Patient)).all()
        print(f"\n📊 Current patients in DB: {len(existing_count)}")
        
        # Delete all patients
        print("🗑️  Deleting all patients...")
        session.exec(text("DELETE FROM patient"))
        session.commit()
        print("✅ All patients deleted")
        
        # Read CSV and import patients
        print(f"\n📥 Importing patients from CSV...")
        imported = 0
        
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows
                if not row.get('ID') or not row.get('ID').strip():
                    continue
                
                patient_id = row.get('ID', '').strip()
                features = parse_csv_row(row)
                
                # Create display name from patient ID and some identifying info
                gender = features.get('Geschlecht', '?')
                age = features.get('Alter [J]', '?')
                display_name = f"Patient {patient_id} ({gender}, {age}J)"
                
                # Create patient
                patient_create = PatientCreate(
                    input_features=features,
                    display_name=display_name
                )
                
                try:
                    patient = crud.create_patient(session=session, patient_in=patient_create)
                    print(f"  ✅ Created: {display_name} (ID: {patient.id})")
                    imported += 1
                except Exception as e:
                    print(f"  ❌ Failed to create patient {patient_id}: {e}")
        
        print(f"\n🎉 Import complete! {imported} patients imported.")
        
        # Verify count
        final_count = crud.count_patients(session=session)
        print(f"📊 Final patient count: {final_count}")


if __name__ == "__main__":
    main()
