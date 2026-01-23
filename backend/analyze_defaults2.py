#!/usr/bin/env python3
"""Analyse der Default-Werte."""
import pickle
import numpy as np
with open('app/models/logreg_best_model.pkl', 'rb') as f:
    model = pickle.load(f)
from app.core.preprocessor import EXPECTED_FEATURES
coef = model.coef_[0]
intercept = model.intercept_[0]
print('=' * 80)
print('ANALYSE: WARUM SIND DIE VORHERSAGEN SO HOCH?')
print('=' * 80)
print()
print('1. BASE INTERCEPT:', round(intercept, 4), '=', round(1/(1+np.exp(-intercept))*100, 1), '% Basis')
print()
print('2. DEFAULTS mit HOHEN Koeffizienten:')
print()
problems = [
    'Objektive Messungen.LL..._Nicht erhoben',
    'Objektive Messungen.4000 Hz..._Nicht erhoben',
    'Diagnose.Höranamnese.Ursache....Ursache..._unknown',
    'Diagnose.Höranamnese.Erwerbsart..._unknown',
    'Diagnose.Höranamnese.Art der Hörstörung..._Cochleär',
]
total = 0
for fname in problems:
    idx = EXPECTED_FEATURES.index(fname)
    c = coef[idx]
    total += c
    print('  ', fname[:55].ljust(57), round(c, 4))
print()
print('  SUMME Default-Beiträge:', round(total, 4))
print()
print('3. RESULTIERENDE BASIS-VORHERSAGE:')
base_logit = intercept + total
base_prob = 1 / (1 + np.exp(-base_logit))
print('   Intercept + Defaults =', round(base_logit, 3), '(Logit)')
print('   Wahrscheinlichkeit:', round(base_prob*100, 1), '%')
print('=' * 80)
