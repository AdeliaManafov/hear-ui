#!/usr/bin/env python3
"""Show database statistics."""

from app.api.deps import get_db
from app.models import Patient
from sqlalchemy import func

db = next(get_db())
try:
    total_patients = db.query(func.count(Patient.id)).scalar()
    print("=" * 60)
    print("DATENBANK-STATISTIK")
    print("=" * 60)
    print(f"Anzahl Patienten: {total_patients}")
    
    if total_patients > 0:
        print(f"\nBeispiel-Patienten (erste 10):")
        patients = db.query(Patient).limit(10).all()
        for i, p in enumerate(patients, 1):
            name = getattr(p, "display_name", None) or "Unbenannt"
            features = p.input_features or {}
            age = features.get("Alter [J]", features.get("age", "?"))
            gender = features.get("Geschlecht", features.get("gender", "?"))
            print(f"  {i}. {name} | Alter: {age} | Geschlecht: {gender} | ID: {str(p.id)[:8]}...")
    else:
        print("\n⚠️  Keine Patienten in der Datenbank!")
finally:
    db.close()
