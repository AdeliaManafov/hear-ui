#!/usr/bin/env python3
"""Koeffizienten-Analyse via API."""
import requests
import numpy as np

data = requests.post('http://localhost:8000/api/v1/explainer/explain', 
                     json={}).json()
fi = data['feature_importance']
base = data['base_value']

sorted_features = sorted(fi.items(), key=lambda x: x[1], reverse=True)

print('='*80)
print('MODELL-KOEFFIZIENTEN & PLAUSIBILITÄT')
print('='*80)
print(f'\nIntercept: {base:.4f} → Basis: {1/(1+np.exp(-base)):.1%}')

print('\nTop 10 POSITIVE Koeffizienten:')
for i, (feat, coef) in enumerate(sorted_features[:10], 1):
    if coef > 0:
        print(f'{i:2d}. {feat[:50]:52s} +{coef:.4f}')

print('\nTop 10 NEGATIVE Koeffizienten:')
negative = sorted(fi.items(), key=lambda x: x[1])[:10]
for i, (feat, coef) in enumerate(negative, 1):
    if coef < 0:
        print(f'{i:2d}. {feat[:50]:52s} {coef:.4f}')

print('\n' + '='*80)
print('SZENARIEN: Wann erreicht man 100%?')
print('='*80)

top_positive = [v for k, v in sorted_features if v > 0][:10]

for n in [3, 5, 10]:
    sum_coef = sum(top_positive[:n])
    logit = base + sum_coef
    prob = 1 / (1 + np.exp(-logit))
    print(f'\nTop {n} positive Features:')
    print(f'  Σ = {sum_coef:.4f}, Logit = {logit:.4f}, P = {prob:.1%}')

needed_logit = 6.91
needed_sum = needed_logit - base
print(f'\nFür 99.9% (≈100%): Benötigte Σ = {needed_sum:.4f}')
if top_positive[0] > 0:
    print(f'  ≈ {needed_sum/top_positive[0]:.1f} top-Features')

print('\n' + '='*80)
print('ANTWORT: IST 100% PLAUSIBEL?')
print('='*80)
print('''
✅ JA - mathematisch und medizinisch:
   • Logit > 7 ist bei 10+ positiven Features erreichbar
   • Z.B.: CI + Hörgerät + gute Prognose-Faktoren
   • Sigmoid-Funktion: Logit 7 → 99.9% → gerundet 100%

⚠️  ABER beachten:
   • 100% = "höchste Modell-Wahrscheinlichkeit"
   • NICHT = "garantierter klinischer Erfolg"
   • Individuelle Unterschiede bleiben

🔍 SO PRÜFEN SIE DIE KORREKTHEIT:

1. MATHEMATISCHE VALIDIERUNG (siehe validate_predictions.py):
   ✓ Manuelle Berechnung = API Prediction?
   ✓ Formel: P = 1/(1 + e^(-(Intercept + Σ Features)))

2. MEDIZINISCHE VALIDIERUNG:
   • Original-Trainingsdaten prüfen
   • Gibt es ähnliche Patienten?
   • Was war deren tatsächliches Outcome (post24)?
   • Kalibrierung: Predicted vs. Actual

3. STATISTISCHE VALIDIERUNG:
   • Calibration Curve erstellen
   • Brier Score berechnen  
   • Confusion Matrix (wenn Schwellwert definiert)

📊 TARGET: outcome_measurments.post24.measure
   • Werte: 0-55 (Perzentile)
   • Höher = besseres Outcome
   • Modell prediziert P(Erfolg), wobei "Erfolg" 
     wahrscheinlich als post24 > Schwellwert definiert ist

💡 EMPFEHLUNG FÜR UI:
   Zeigen Sie statt "100%":
   → "Sehr hohe Erfolgswahrscheinlichkeit (>95%)"
   → "Basierend auf ähnlichen historischen Fällen"
   → Confidence Intervals wenn verfügbar
   → Hinweis: "Individuelle Ergebnisse können variieren"
''')
print('='*80)
