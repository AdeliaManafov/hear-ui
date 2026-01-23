#!/usr/bin/env python3
"""Reset database to only sample patients."""

from app.api.deps import get_db
from app.models import Patient, Prediction, Feedback
from sqlalchemy import delete

db = next(get_db())
try:
    # Lösche alle Predictions
    pred_count = db.execute(delete(Prediction)).rowcount
    print(f"Gelöscht: {pred_count} Predictions")
    
    # Lösche alle Feedbacks
    feed_count = db.execute(delete(Feedback)).rowcount
    print(f"Gelöscht: {feed_count} Feedbacks")
    
    # Lösche alle Patienten
    pat_count = db.execute(delete(Patient)).rowcount
    print(f"Gelöscht: {pat_count} Patienten")
    
    db.commit()
    print("\n✅ Datenbank geleert!")
finally:
    db.close()
