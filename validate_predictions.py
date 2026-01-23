#!/usr/bin/env python3
"""
Validierung der Vorhersagen: Manuelle Berechnung vs. Model-Prediction

Dieses Skript zeigt GENAU wie LogisticRegression die Vorhersagen berechnet
und vergleicht manuelle Berechnungen mit dem Model.
"""
import requests
import numpy as np

BASE_URL = 'http://localhost:8000/api/v1'

print('='*80)
print('VORHERSAGE-VALIDIERUNG: Wie berechnet das Model?')
print('='*80)
print()
print('LogisticRegression verwendet die Formel:')
print('  1. Logit = Intercept + Σ(Koeffizient_i × Feature_i)')
print('  2. Probability = 1 / (1 + e^(-Logit))  [Sigmoid-Funktion]')
print()
print('='*80)

# Hole einen Patienten
patients = requests.get(f'{BASE_URL}/patients/').json()

for patient_num in [0, 1, 2]:  # Teste 3 Patienten
    patient = patients[patient_num]
    pid = patient['id']
    name = patient.get('display_name', 'Unbekannt')
    
    print(f'\n{"="*80}')
    print(f'PATIENT {patient_num + 1}: {name}')
    print('='*80)
    
    # Hole Prediction vom API
    pred_result = requests.get(f'{BASE_URL}/patients/{pid}/predict').json()
    api_prediction = pred_result['prediction']
    
    # Hole Explainer (mit Feature Importance)
    expl_result = requests.get(f'{BASE_URL}/patients/{pid}/explainer').json()
    base_value = expl_result['base_value']
    feature_importance = expl_result['feature_importance']
    
    # Berechne manuell
    print(f'\nSchritt 1: Intercept (Base Value)')
    print(f'  Intercept = {base_value:.6f}')
    
    # Zeige die wichtigsten Features
    print(f'\nSchritt 2: Feature-Beiträge (Top 10)')
    sorted_features = sorted(feature_importance.items(), 
                            key=lambda x: abs(x[1]), reverse=True)[:10]
    
    total_contribution = 0
    for feat, contrib in sorted_features:
        total_contribution += contrib
        if abs(contrib) > 0.001:
            print(f'  {feat[:55]:57s} {contrib:+8.4f}')
    
    # Summiere ALLE Features
    all_contributions = sum(feature_importance.values())
    print(f'\nSchritt 3: Summe ALLER Feature-Beiträge')
    print(f'  Σ Features = {all_contributions:.6f}')
    
    # Berechne Logit
    manual_logit = base_value + all_contributions
    print(f'\nSchritt 4: Logit berechnen')
    print(f'  Logit = {base_value:.6f} + {all_contributions:.6f} = {manual_logit:.6f}')
    
    # Berechne Probability mit Sigmoid
    manual_probability = 1 / (1 + np.exp(-manual_logit))
    print(f'\nSchritt 5: Sigmoid-Funktion anwenden')
    print(f'  P = 1 / (1 + e^(-{manual_logit:.6f}))')
    print(f'  P = {manual_probability:.6f} = {manual_probability:.1%}')
    
    # Vergleiche mit API
    print(f'\n{"─"*80}')
    print(f'VERGLEICH:')
    print(f'  API Prediction:      {api_prediction:.6f} ({api_prediction:.1%})')
    print(f'  Manuelle Berechnung: {manual_probability:.6f} ({manual_probability:.1%})')
    print(f'  Differenz:           {abs(api_prediction - manual_probability):.9f}')
    
    if abs(api_prediction - manual_probability) < 0.0001:
        print(f'  Status: ✅ KORREKT - Berechnungen stimmen überein!')
    else:
        print(f'  Status: ⚠️  ABWEICHUNG - Prüfung erforderlich!')
    
    # Medizinische Plausibilität
    print(f'\n{"─"*80}')
    print(f'MEDIZINISCHE PLAUSIBILITÄT:')
    
    # Analysiere positive und negative Faktoren
    positive_factors = [(f, v) for f, v in sorted_features if v > 0.5]
    negative_factors = [(f, v) for f, v in sorted_features if v < -0.5]
    
    print(f'\n  Stark POSITIVE Faktoren (erhöhen Vorhersage):')
    if positive_factors:
        for feat, val in positive_factors[:5]:
            print(f'    • {feat[:50]:52s} (+{val:.2f})')
    else:
        print(f'    Keine stark positiven Faktoren')
    
    print(f'\n  Stark NEGATIVE Faktoren (senken Vorhersage):')
    if negative_factors:
        for feat, val in negative_factors[:5]:
            print(f'    • {feat[:50]:52s} ({val:.2f})')
    else:
        print(f'    Keine stark negativen Faktoren')
    
    # Interpretation
    print(f'\n  Interpretation:')
    if api_prediction > 0.8:
        print(f'    🔴 SEHR HOCH ({api_prediction:.1%})')
        print(f'    → Patient hat stark positive Indikatoren')
        print(f'    → Möglicherweise bereits fortgeschrittene Behandlung')
    elif api_prediction > 0.5:
        print(f'    🟡 MODERAT ({api_prediction:.1%})')
        print(f'    → Ausgeglichenes Risikoprofil')
    else:
        print(f'    🟢 NIEDRIG ({api_prediction:.1%})')
        print(f'    → Überwiegend negative Faktoren im Modell')

print(f'\n\n{"="*80}')
print('VALIDIERUNGS-ZUSAMMENFASSUNG')
print('='*80)
print()
print('✅ Die Predictions werden KORREKT berechnet, wenn:')
print('   • Manuelle Berechnung = API Prediction (Differenz < 0.0001)')
print('   • Formel: P = 1 / (1 + e^(-(Intercept + Σ Beiträge)))')
print()
print('⚠️  100% Vorhersagen bedeuten:')
print('   • Logit > 10 (extrem positive Feature-Kombination)')
print('   • e^(-10) ≈ 0.000045 → P ≈ 0.99995 ≈ 100%')
print()
print('❓ Ist das medizinisch plausibel?')
print('   → Hängt vom Trainings-Datensatz ab!')
print('   → Wenn das Modell auf "Erfolg nach CI" trainiert wurde,')
print('     könnte ein Patient mit CI + Hörgerät + anderen positiven')
print('     Faktoren tatsächlich ~100% "Erfolg" haben.')
print()
print('🔍 Empfehlung zur Validierung:')
print('   1. Prüfen Sie das Original-Trainings-Dataset')
print('   2. Was ist das TARGET? (post24 measure?)')
print('   3. Gibt es Patienten mit ähnlichen Features im Training?')
print('   4. Was war deren Outcome?')
print('='*80)
