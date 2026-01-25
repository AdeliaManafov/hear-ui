#!/usr/bin/env python3
"""Debug-Script um exakte Feature-Werte zu sehen."""

import sys
from pathlib import Path

backend_root = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_root))

from app.core.model_wrapper import ModelWrapper
from app.core.preprocessor import preprocess_patient_data, EXPECTED_FEATURES

# Test-Patient MIT Kopfschmerzen
patient_with_headache = {
    "Alter [J]": 30,
    "Geschlecht": "w",
    "Symptome präoperativ.Kopfschmerzen...": "Vorhanden",
    "Symptome präoperativ.Schwindel...": "Kein",
    "outcome_measurments.pre.measure.": 0
}

# Test-Patient OHNE Kopfschmerzen
patient_without_headache = {
    "Alter [J]": 30,
    "Geschlecht": "w",
    "Symptome präoperativ.Kopfschmerzen...": "Keine",
    "Symptome präoperativ.Schwindel...": "Kein",
    "outcome_measurments.pre.measure.": 0
}

print("="*80)
print("KOPFSCHMERZEN-VERGLEICH")
print("="*80)

for label, patient in [("MIT Kopfschmerzen", patient_with_headache), 
                       ("OHNE Kopfschmerzen", patient_without_headache)]:
    print(f"\n{label}:")
    print(f"Input: {patient}")
    
    features = preprocess_patient_data(patient)
    print(f"\nPreprocessed shape: {features.shape}")
    
    # Convert to numpy if DataFrame
    import numpy as np
    if hasattr(features, 'values'):
        feature_array = features.values
    else:
        feature_array = np.array(features)
    
    # Finde Kopfschmerzen-Feature
    headache_idx = EXPECTED_FEATURES.index("Symptome präoperativ.Kopfschmerzen...")
    headache_value = feature_array[0][headache_idx]
    print(f"Kopfschmerzen-Feature-Wert (Index {headache_idx}): {headache_value}")
    
    # Prediction
    wrapper = ModelWrapper()
    pred = wrapper.predict(patient, clip=True)
    pred_val = pred[0] if hasattr(pred, '__len__') else pred
    print(f"Prediction: {pred_val:.4f} ({pred_val*100:.2f}%)")
    
    # Zeige alle nicht-null Features
    print("\nAlle gesetzten Features (Wert != 0.0):")
    for i, val in enumerate(feature_array[0]):
        if val != 0.0 and i < len(EXPECTED_FEATURES):
            print(f"  [{i:2d}] {EXPECTED_FEATURES[i]:<60} = {val:.4f}")

print("\n" + "="*80)
print("ANALYSE")
print("="*80)

# Berechne Differenz
import numpy as np
features_with_df = preprocess_patient_data(patient_with_headache)
features_without_df = preprocess_patient_data(patient_without_headache)
features_with = features_with_df.values[0] if hasattr(features_with_df, 'values') else np.array(features_with_df)[0]
features_without = features_without_df.values[0] if hasattr(features_without_df, 'values') else np.array(features_without_df)[0]
diff = features_with - features_without

print("\nFeature-Differenzen:")
for i, d in enumerate(diff):
    if abs(d) > 0.0001 and i < len(EXPECTED_FEATURES):
        print(f"  {EXPECTED_FEATURES[i]:<60} Diff: {d:+.4f}")

# Lade Koeffizienten
wrapper = ModelWrapper()
model = wrapper.model
if hasattr(model, 'coef_'):
    coef = model.coef_[0][headache_idx]
    print(f"\nKopfschmerzen-Koeffizient: {coef:.4f}")
    print(f"Erwartete Prediction-Differenz: {coef * 1.0:.4f} (wenn Kopfschmerzen=1)")
