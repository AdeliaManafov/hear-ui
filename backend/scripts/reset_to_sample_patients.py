#!/usr/bin/env python3
"""Reset database to only contain the 5 sample patients from sample_patients.csv.

Usage:
  # From host (with backend directory in path):
  cd backend
  python scripts/reset_to_sample_patients.py

  # Inside Docker container:
  docker compose exec backend python scripts/reset_to_sample_patients.py

  # Non-interactive (CI/automation):
  echo yes | docker compose exec -T backend python scripts/reset_to_sample_patients.py

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

from sqlalchemy import create_engine, text
from sqlmodel import Session, select
from app.core.config import settings
from app.models.patient_record import Patient, PatientCreate
from app import crud


# Support both container and host paths
CSV_PATH_CONTAINER = Path("/app/data/sample_patients.csv")
CSV_PATH_HOST = Path(__file__).parent.parent.parent / "data" / "sample_patients.csv"

if CSV_PATH_CONTAINER.exists():
    CSV_PATH = CSV_PATH_CONTAINER
else:
    CSV_PATH = CSV_PATH_HOST


def parse_csv_row(row: dict) -> dict:
    """Convert a CSV row to patient input_features dict.
    
    Handles BOM in CSV headers and filters out empty values.
    """
    features = {}
    for key, value in row.items():
        if value and str(value).strip():
            # Clean key (remove BOM if present)
            clean_key = key.lstrip('\ufeff').strip()
            features[clean_key] = value.strip()
    return features


def find_id_key(fieldnames: list[str] | None) -> str | None:
    """Find the ID column header, handling BOM."""
    if not fieldnames:
        return None
    for key in fieldnames:
        if key and key.lstrip('\ufeff').strip().lower() == 'id':
            return key
    return None


def main():
    if not CSV_PATH.exists():
        print(f"❌ CSV file not found at either:")
        print(f"   Container: {CSV_PATH_CONTAINER}")
        print(f"   Host: {CSV_PATH_HOST}")
        sys.exit(1)
    
    print(f"📂 Using CSV: {CSV_PATH}")
    print(f"📊 Database: {settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}")
    
    # Create engine from settings (robust approach that works in container and host)
    db_url = str(settings.SQLALCHEMY_DATABASE_URI)
    engine = create_engine(db_url)
    
    # Confirm action (support non-interactive mode for CI)
    print("\n⚠️  WARNING: This will DELETE ALL existing patients!")
    try:
        confirm = input("Type 'yes' to continue: ")
        if confirm.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
    except EOFError:
        # Non-interactive mode (e.g., piped input)
        print("Running in non-interactive mode (assuming 'yes')")
    
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
            
            # Find ID column (handle BOM)
            id_key = find_id_key(reader.fieldnames)
            if not id_key:
                print("❌ Could not find 'ID' column in CSV")
                sys.exit(2)
            
            for row in reader:
                # Skip empty rows (use BOM-aware id_key)
                patient_id = row.get(id_key, '').strip()
                if not patient_id:
                    continue
                
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
