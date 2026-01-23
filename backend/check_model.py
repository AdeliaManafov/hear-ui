#!/usr/bin/env python3
"""Script to check model and preprocessor consistency."""

from app.core.model_wrapper import ModelWrapper
from app.core.preprocessor import EXPECTED_FEATURES, preprocess_patient_data
import numpy as np

def main():
    w = ModelWrapper()
    print("=" * 50)
    print("MODELL-INFO")
    print("=" * 50)
    print(f"Modell geladen: {w.is_loaded()}")
    print(f"Modell-Typ: {type(w.model).__name__}")

    # Was erwartet das Modell?
    expected_by_model = getattr(w.model, "n_features_in_", "unbekannt")
    print(f"Features vom Modell erwartet: {expected_by_model}")
    
    # Modell-Koeffizienten
    if hasattr(w.model, "coef_"):
        coef = w.model.coef_
        print(f"Koeffizienten Shape: {coef.shape}")
        print(f"Intercept: {w.model.intercept_}")
    
    print()
    print("=" * 50)
    print("PREPROCESSOR-INFO")
    print("=" * 50)
    print(f"EXPECTED_FEATURES Liste: {len(EXPECTED_FEATURES)} Features")

    # Test-Preprocessing
    test_input = {"Alter [J]": 50, "Geschlecht": "m"}
    X = preprocess_patient_data(test_input)
    print(f"Preprocessor Output Shape: {X.shape}")
    print(f"Features nach Preprocessing: {X.shape[1]}")

    print()
    print("=" * 50)
    print("KONSISTENZ-CHECK")
    print("=" * 50)
    if expected_by_model == X.shape[1]:
        print("✅ MATCH: Modell und Preprocessor sind konsistent!")
    else:
        print(f"❌ WARNUNG: Modell erwartet {expected_by_model}, Preprocessor liefert {X.shape[1]}")
    
    print()
    print("=" * 50)
    print("FEATURE-LISTE (erste 20)")
    print("=" * 50)
    for i, f in enumerate(EXPECTED_FEATURES[:20]):
        print(f"  {i}: {f}")
    print(f"  ... und {len(EXPECTED_FEATURES) - 20} weitere")
    
    print()
    print("=" * 50)
    print("TEST-VORHERSAGEN")
    print("=" * 50)
    
    # Verschiedene Test-Szenarien
    scenarios = [
        {"name": "Leerer Input (alle Defaults)", "data": {}},
        {"name": "Minimal (50J, männlich)", "data": {"Alter [J]": 50, "Geschlecht": "m"}},
        {"name": "Minimal (50J, weiblich)", "data": {"Alter [J]": 50, "Geschlecht": "w"}},
        {"name": "Jung (25J)", "data": {"Alter [J]": 25, "Geschlecht": "m"}},
        {"name": "Alt (75J)", "data": {"Alter [J]": 75, "Geschlecht": "w"}},
        {"name": "Mit Tinnitus", "data": {"Alter [J]": 50, "Geschlecht": "m", "Symptome präoperativ.Tinnitus...": 1}},
        {"name": "Mit pre-measure", "data": {"Alter [J]": 50, "Geschlecht": "m", "outcome_measurments.pre.measure.": 30}},
    ]
    
    for s in scenarios:
        try:
            prob = w.predict(s["data"])[0]
            print(f"  {s['name']}: {prob:.1%}")
        except Exception as e:
            print(f"  {s['name']}: FEHLER - {e}")

if __name__ == "__main__":
    main()
