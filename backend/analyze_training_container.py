#!/usr/bin/env python3
"""Container-Version: Analyse des Trainings."""
import pickle
import numpy as np
import pandas as pd

print('='*80)
print('MODELL-TRAININGS-ANALYSE (Container)')
print('='*80)

# Sample-Daten
print('\n1. TARGET aus sample_patients.csv:')
print('-'*80)
print('outcome_measurments.post24.measure.:')
print('  Werte: [0.0, 15.0, 40.0, 55.0]')
print('  Interpretation: Hör-Messwerte (vermutlich Perzentile)')
print('  → Je höher, desto besser das Outcome')

# Model laden
with open('/app/app/models/logreg_best_model.pkl', 'rb') as f:
    model = pickle.load(f)

from app.core.preprocessor import EXPECTED_FEATURES

intercept = model.intercept_[0]
coef = model.coef_[0]

print(f'\n2. MODELL-PARAMETER:')
print('-'*80)
print(f'Intercept: {intercept:.4f}')
print(f'Basis-Wahrscheinlichkeit: {1/(1+np.exp(-intercept)):.1%}')

# Top Features
top_positive = sorted(zip(EXPECTED_FEATURES, coef), key=lambda x: x[1], reverse=True)[:10]
top_negative = sorted(zip(EXPECTED_FEATURES, coef), key=lambda x: x[1])[:10]

print(f'\nTop 10 POSITIVE Koeffizienten:')
for feat, c in top_positive:
    print(f'  {feat[:50]:52s} +{c:.4f}')

print(f'\nTop 10 NEGATIVE Koeffizienten:')
for feat, c in top_negative:
    print(f'  {feat[:50]:52s} {c:.4f}')

# Berechne Szenarien
print(f'\n3. SZENARIEN FÜR HOHE VORHERSAGEN:')
print('-'*80)

print(f'\nSzenario: Alle Top-5 positiven Features aktiv')
sum_top5 = sum(c for _, c in top_positive[:5])
logit = intercept + sum_top5
prob = 1 / (1 + np.exp(-logit))
print(f'  Σ Top-5: {sum_top5:.4f}')
print(f'  Logit: {logit:.4f}')
print(f'  Probability: {prob:.1%}')

print(f'\nSzenario: Top-10 positive Features aktiv')
sum_top10 = sum(c for _, c in top_positive[:10])
logit = intercept + sum_top10
prob = 1 / (1 + np.exp(-logit))
print(f'  Σ Top-10: {sum_top10:.4f}')
print(f'  Logit: {logit:.4f}')
print(f'  Probability: {prob:.1%}')

print(f'\nBenötigt für 99.9% (≈100%):')
needed_logit = 6.91  # ln(999) für P=0.999
needed_sum = needed_logit - intercept
print(f'  Logit: {needed_logit:.2f}')
print(f'  Benötigte Σ Features: {needed_sum:.4f}')
print(f'  Anzahl Top-Features: ~{needed_sum/top_positive[0][1]:.1f}')

print(f'\n4. INTERPRETATION:')
print('-'*80)
print(f'''
Das Modell sagt die WAHRSCHEINLICHKEIT eines guten Outcomes vorher.

TARGET: post24 Messwert (0-55, höher = besser)
- Modell wurde wahrscheinlich auf binäre Klassifikation trainiert:
  • Erfolg = post24 > Schwellwert (z.B. > 30)
  • Misserfolg = post24 < Schwellwert

100% Vorhersage bedeutet:
✓ Das Modell ist sich SEHR SICHER, dass dieser Patient
  die Erfolgskriterien erfüllen wird
✓ Basiert auf der Kombination stark positiver Features
✓ Ähnliche Patienten im Training hatten fast alle Erfolg

ABER:
⚠️  100% bedeutet NICHT "garantiert"
⚠️  Es bedeutet: "höchste modellierte Wahrscheinlichkeit"
⚠️  Unsicherheit/Confidence Intervals fehlen

EMPFEHLUNG:
→ Zeigen Sie Vorhersagen mit Kontext an:
  "Sehr hohe Erfolgswahrscheinlichkeit (>95%)"
  statt "100% Erfolg garantiert"
''')
print('='*80)
