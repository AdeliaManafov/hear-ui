#!/usr/bin/env python3
"""Analyze the new model and compare with old."""

import os
from datetime import datetime

try:
    import joblib
    USE_JOBLIB = True
except ImportError:
    import pickle
    USE_JOBLIB = False

MODEL_PATH = "/app/app/models/logreg_best_model.pkl"

print("=" * 70)
print("NEUE MODEL-ANALYSE")
print("=" * 70)

# Datei-Info
if os.path.exists(MODEL_PATH):
    size = os.path.getsize(MODEL_PATH)
    mtime = os.path.getmtime(MODEL_PATH)
    modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nDatei:")
    print(f"  Pfad: {MODEL_PATH}")
    print(f"  Größe: {size:,} Bytes ({size/1024:.1f} KB)")
    print(f"  Geändert: {modified}")
else:
    print(f"ERROR: {MODEL_PATH} nicht gefunden!")
    exit(1)

# Model laden und analysieren
print(f"\nLade Modell mit: {'joblib' if USE_JOBLIB else 'pickle'}")
try:
    if USE_JOBLIB:
        model = joblib.load(MODEL_PATH)
    else:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    print("✅ Modell erfolgreich geladen!")
except Exception as e:
    print(f"❌ Fehler beim Laden: {e}")
    print("\nVersuche alternative Methode...")
    try:
        import pickle
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        print("✅ Mit pickle erfolgreich!")
    except Exception as e2:
        print(f"❌ Auch mit pickle fehlgeschlagen: {e2}")
        exit(1)

print(f"\nModell-Typ: {type(model).__name__}")
print(f"Modell-Klasse: {model.__class__.__module__}.{model.__class__.__name__}")

# Features
n_features = getattr(model, "n_features_in_", "unbekannt")
print(f"\nErwartete Features: {n_features}")

# Koeffizienten
if hasattr(model, "coef_"):
    coef = model.coef_
    print(f"Koeffizienten Shape: {coef.shape}")
    print(f"Koeffizienten Min: {coef.min():.4f}")
    print(f"Koeffizienten Max: {coef.max():.4f}")
    print(f"Koeffizienten Mean: {coef.mean():.4f}")

# Intercept
if hasattr(model, "intercept_"):
    intercept = model.intercept_
    print(f"\nIntercept: {intercept}")
    if isinstance(intercept, (list, tuple)) or hasattr(intercept, "__len__"):
        import numpy as np
        base_prob = 1 / (1 + np.exp(-float(intercept[0])))
        print(f"Basis-Wahrscheinlichkeit: {base_prob:.1%}")

# Weitere Attribute
print(f"\nWeitere Attribute:")
for attr in ["classes_", "penalty", "C", "solver", "max_iter"]:
    if hasattr(model, attr):
        print(f"  {attr}: {getattr(model, attr)}")

# Test-Vorhersage
print("\n" + "=" * 70)
print("TEST-VORHERSAGEN")
print("=" * 70)

from app.core.model_wrapper import ModelWrapper
w = ModelWrapper()

tests = [
    ("Leer (alle Defaults)", {}),
    ("30J, weiblich", {"Alter [J]": 30, "Geschlecht": "w"}),
    ("30J, männlich", {"Alter [J]": 30, "Geschlecht": "m"}),
    ("50J, weiblich", {"Alter [J]": 50, "Geschlecht": "w"}),
    ("70J, männlich", {"Alter [J]": 70, "Geschlecht": "m"}),
]

for name, data in tests:
    try:
        prob = w.predict(data)[0]
        print(f"  {name:25s}: {prob:.1%}")
    except Exception as e:
        print(f"  {name:25s}: ERROR - {e}")
