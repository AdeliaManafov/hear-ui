#!/usr/bin/env python3
"""Analyse der Default-Werte und deren Einfluss auf hohe Vorhersagen."""

import pickle
import numpy as np
import sys

sys.path.insert(0, '.')
from app.core.preprocessor import EXPECTED_FEATURES

# Load model
with open('app/models/logreg_best_model.pkl', 'rb') as f:
    model = pickle.load(f)

coef = model.coef_[0]
intercept = model.intercept_[0]

print('=' * 80)
print('ANALYSE: WARUM SIND DIE VORHERSAGEN SO HOCH?')
print('=' * 80)
print()
print(f'1. BASE INTERCEPT: {intercept:.4f} = {1/(1+np.exp(-intercept)):.1%} Basis-Prob.')
print()
print('2. DEFAULTS mit HOHEN POSITIVEN Koeffizienten:')
print()

# Problematic defaults in preprocessor.py
problems = [
    ('Objektive Messungen.LL..._Nicht erhoben', 'Default bei fehlenden LL-Messungen'),
    ('Objektive Messungen.4000 Hz..._Nicht erhoben', 'Default bei fehlenden 4000Hz'),
    ('Diagnose.Höranamnese.Ursache....Ursache..._unknown', 'Default bei Ursache'),
    ('Diagnose.Höranamnese.Erwerbsart..._unknown', 'Default bei Erwerbsart'),
    ('Diagnose.Höranamnese.Art der Hörstörung..._Cochleär', 'Default bei Hörstörung'),
]

total = 0
for fname, reason in problems:
    idx = EXPECTED_FEATURES.index(fname)
    c = coef[idx]
    total += c
    print(f'  {fname[:55]:57s} {c:+.4f}')

print()
print(f'  SUMME Default-Beiträge: {total:+.4f}')
print()
print(f'3. RESULTIERENDE BASIS-VORHERSAGE (bei fehlenden Daten):')
base_logit = intercept + total
base_prob = 1 / (1 + np.exp(-base_logit))
print(f'   {intercept:.3f} (Base) + {total:.3f} (Defaults) = {base_logit:.3f} (Logit)')
print(f'   Wahrscheinlichkeit: {base_prob:.1%}')
print()
print('4. LÖSUNG: Defaults in preprocessor.py ändern, sodass KEINE')
print('   One-Hot-Features aktiviert werden, wenn Daten fehlen.')
print('=' * 80)
