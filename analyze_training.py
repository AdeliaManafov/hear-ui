#!/usr/bin/env python3
"""
Analyse: Was trainiert das Modell eigentlich?

Dieses Skript untersucht:
1. Was ist das TARGET (outcome_measurments.post24)?
2. Welche Werte sind im Training möglich?
3. Ist 100% realistisch?
"""
import pandas as pd
import pickle
import numpy as np

print('='*80)
print('MODELL-TRAININGS-ANALYSE')
print('='*80)

# 1. Sample-Daten laden
print('\n1. SAMPLE-DATEN ANALYSIEREN')
print('-'*80)
df = pd.read_csv('patientsData/sample_patients.csv')
print(f'Anzahl Patienten: {len(df)}')
print(f'\nVerfügbare Spalten ({len(df.columns)}):')
for col in df.columns:
    print(f'  - {col}')

# 2. TARGET analysieren
print(f'\n2. TARGET-VARIABLE ANALYSIEREN')
print('-'*80)

outcome_cols = [c for c in df.columns if 'outcome' in c.lower()]
print(f'Outcome-Spalten: {outcome_cols}')

if outcome_cols:
    for col in outcome_cols:
        values = df[col].dropna()
        print(f'\n{col}:')
        print(f'  Min: {values.min()}, Max: {values.max()}, Median: {values.median()}')
        print(f'  Werte: {sorted(values.unique())}')

# 3. Model laden und inspizieren
print(f'\n3. MODELL-PARAMETER ANALYSIEREN')
print('-'*80)

with open('backend/app/models/logreg_best_model.pkl', 'rb') as f:
    model = pickle.load(f)

intercept = model.intercept_[0]
print(f'Intercept: {intercept:.4f}')
print(f'Basis-Wahrscheinlichkeit (ohne Features): {1/(1+np.exp(-intercept)):.1%}')

# Analysiere Koeffizienten
coef = model.coef_[0]
print(f'\nKoeffizienten-Statistik:')
print(f'  Min: {coef.min():.4f}')
print(f'  Max: {coef.max():.4f}')
print(f'  Mittelwert: {coef.mean():.4f}')
print(f'  Std: {coef.std():.4f}')

# Wichtigste Features
from backend.app.core.preprocessor import EXPECTED_FEATURES
top_positive = sorted(zip(EXPECTED_FEATURES, coef), key=lambda x: x[1], reverse=True)[:5]
top_negative = sorted(zip(EXPECTED_FEATURES, coef), key=lambda x: x[1])[:5]

print(f'\nTop 5 POSITIVE Koeffizienten (erhöhen Erfolg):')
for feat, c in top_positive:
    print(f'  {feat[:50]:52s} +{c:.4f}')

print(f'\nTop 5 NEGATIVE Koeffizienten (senken Erfolg):')
for feat, c in top_negative:
    print(f'  {feat[:50]:52s} {c:.4f}')

# 4. Simulations-Szenarien
print(f'\n4. SIMULATIONS-SZENARIEN: Wann erreicht man 100%?')
print('-'*80)

# Szenario 1: Nur positive Features
print(f'\nSzenario 1: Alle TOP-5 positiven Features aktiv')
logit_scenario1 = intercept + sum(c for _, c in top_positive)
prob_scenario1 = 1 / (1 + np.exp(-logit_scenario1))
print(f'  Logit: {logit_scenario1:.4f}')
print(f'  Probability: {prob_scenario1:.1%}')

# Szenario 2: Gemischt
print(f'\nSzenario 2: Top 3 positive + Top 2 negative')
logit_scenario2 = intercept + sum(c for _, c in top_positive[:3]) + sum(c for _, c in top_negative[:2])
prob_scenario2 = 1 / (1 + np.exp(-logit_scenario2))
print(f'  Logit: {logit_scenario2:.4f}')
print(f'  Probability: {prob_scenario2:.1%}')

# Szenario 3: Extremfall
print(f'\nSzenario 3: Wann erreicht man genau 100.0% (gerundet)?')
print(f'  Benötigter Logit: ~10 (für P > 0.9999)')
needed_sum = 10 - intercept
print(f'  Benötigte Σ Features: {needed_sum:.4f}')
print(f'  Das ist erreichbar durch: ~{needed_sum/top_positive[0][1]:.1f} top Features')

# 5. Sample-Patienten nachrechnen
print(f'\n5. SAMPLE-PATIENTEN AUS CSV')
print('-'*80)

for i, row in df.iterrows():
    name = row.get('ID', f'Patient {i+1}')
    pre = row.get('outcome_measurments.pre.measure.', 'N/A')
    post12 = row.get('outcome_measurments.post12.measure.', 'N/A')
    post24 = row.get('outcome_measurments.post24.measure.', 'N/A')
    
    print(f'\nPatient {i+1}: {name}')
    print(f'  Pre:    {pre}')
    print(f'  Post12: {post12}')
    print(f'  Post24: {post24} ← TARGET')
    
    # Verbesserung berechnen
    if pd.notna(pre) and pd.notna(post24):
        improvement = post24 - pre
        print(f'  Verbesserung: {improvement:+.0f}')

print(f'\n{"="*80}')
print('INTERPRETATION & EMPFEHLUNGEN')
print('='*80)
print('''
1. TARGET-DEFINITION prüfen:
   • Ist post24 die Ziel-Variable?
   • Ist es ein Klassifikationsproblem (Erfolg/Misserfolg)?
   • Oder Regression (kontinuierlicher Wert)?

2. MEDIZINISCHE PLAUSIBILITÄT von 100%:
   ✅ PLAUSIBEL wenn:
      - Target = "Verbesserung > X%" oder "Erfolgreiche CI-Anpassung"
      - Patient hat ALLE positiven Indikatoren
      - Trainingsdaten zeigen ähnliche Patienten mit 100% Erfolg
   
   ⚠️  SKEPTISCH wenn:
      - Keine Patienten im Training mit ähnlichen Features
      - Model ist auf unbalanciertem Dataset trainiert
      - Koeffizienten sind nicht kalibriert

3. VALIDIERUNGS-SCHRITTE:
   a) Lade Original-Trainingsdaten
   b) Prüfe: Gibt es Patienten mit features wie Schmidt, Paul?
   c) Prüfe deren Outcome (post24)
   d) Vergleiche mit Model-Vorhersage
   
4. KALIBRIERUNG prüfen:
   • sklearn.calibration.calibration_curve()
   • Vergleiche vorhergesagte vs. tatsächliche Häufigkeiten
   • Bei großer Abweichung: Model re-kalibrieren

5. CLINICAL DECISION RULE:
   • 100% sollte NICHT als "garantierter Erfolg" interpretiert werden
   • Sondern: "höchste Erfolgswahrscheinlichkeit basierend auf Trainingsdaten"
   • Empfehlung: Zeige Confidence Intervals an
''')
print('='*80)
