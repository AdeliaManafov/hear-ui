#!/usr/bin/env python3
"""
Analyse: Welche Features verursachen hohe Vorhersagen (>95%)?
"""
import requests
import sys

# Sample-Patienten abrufen
try:
    patients = requests.get('http://localhost:8000/api/v1/patients/').json()
except Exception as e:
    print(f"❌ Fehler beim Abrufen der Patienten: {e}")
    print("   Ist der Backend-Container aktiv? (docker compose ps)")
    sys.exit(1)

print('='*80)
print('ANALYSE: Welche Features verursachen hohe Vorhersagen?')
print('='*80)

# Analysiere jeden Patienten
for patient in patients[:5]:
    pid = patient['id']
    name = patient.get('display_name', 'Unbekannt')
    
    # Hole Prediction
    pred_response = requests.get(f'http://localhost:8000/api/v1/patients/{pid}/predict').json()
    pred = pred_response['prediction']
    
    # Hole Explainer mit Feature Contributions
    expl_response = requests.get(f'http://localhost:8000/api/v1/patients/{pid}/explainer').json()
    feature_importance = expl_response['feature_importance']
    
    # Sortiere nach absolutem Beitrag
    sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
    
    # Trenne positive und negative Features
    positive_features = [(f, v) for f, v in sorted_features if v > 0.1]
    negative_features = [(f, v) for f, v in sorted_features if v < -0.1]
    
    print(f'\n{"─"*80}')
    print(f'Patient: {name} (ID: {pid})')
    print(f'Vorhersage: {pred:.1%}')
    print(f'{"─"*80}')
    
    if positive_features:
        print(f'\n  ✅ Positive Features (erhöhen Wahrscheinlichkeit):')
        for feat, val in positive_features[:8]:
            print(f'     {feat[:50]:52s} +{val:.4f}')
    else:
        print('  (keine stark positiven Features)')
    
    if negative_features:
        print(f'\n  ⚠️  Negative Features (senken Wahrscheinlichkeit):')
        for feat, val in negative_features[:5]:
            print(f'     {feat[:50]:52s} {val:.4f}')

print('\n' + '='*80)
print('FAZIT: Medizinische Plausibilität von hohen Vorhersagen')
print('='*80)

print('''
📊 MATHEMATISCHE BASIS:
   ✅ Formel: P = 1 / (1 + e^(-(Intercept + Σ(Koeffizient × Feature))))
   ✅ Intercept: 1.2078 → Basiswahrscheinlichkeit: 77.0%
   ✅ Für 99.9% (≈100%): Benötigt Logit ≥ 7
      → Erreicht durch Summe mehrerer positiver Features

🎯 TARGET VARIABLE:
   • outcome_measurments.post24.measure (Skala 0-55)
   • Je höher, desto besser das Hörvermögen nach 24 Monaten
   • Modell trainiert auf: post24 > Schwellwert = "Erfolg"

✅ 100% BEDEUTET:
   • Patient hat "optimales Prognoseprofil"
   • Alle trainierten Features zeigen auf "bestes Outcome"
   • NICHT: Garantierter Erfolg, sondern höchste Wahrscheinlichkeit

⚠️  MEDIZINISCHE PLAUSIBILITÄT PRÜFEN:
   1. Sind die aktivierten Features klinisch sinnvoll?
      → z.B. CI im Gegenohr, gute Höranamnese, jüngeres Alter
   
   2. Gibt es vergleichbare Patienten in Trainingsdaten?
      → Muss mit Original-Datensatz abgeglichen werden
   
   3. Ist das Modell kalibriert?
      → Calibration Plot: Predicted Probability vs. Actual Outcome
      → Brier Score, Log-Loss zur Qualitätsprüfung

🔍 WIE KORREKTHEIT VALIDIEREN:
   ✅ Manuelle Berechnung = API Prediction
      → Siehe: validate_predictions.py (bereits getestet)
   
   ✅ Konsistenz zwischen Endpoints
      → /predict und /explainer liefern identische Werte
   
   ⚠️  Kalibrierung mit Testdaten:
      → Wenn Modell sagt "100%", wie oft ist Outcome wirklich gut?
      → Expected Calibration Error (ECE) berechnen
   
   ⚠️  Cross-Validation:
      → Wie gut generalisiert das Modell auf ungesehene Daten?

💡 EMPFEHLUNGEN FÜR UI:
   • Statt "100%" → "Sehr hohe Erfolgswahrscheinlichkeit (>95%)"
   • Confidence Intervals anzeigen (falls verfügbar)
   • Disclaimer: "Basierend auf historischen Daten von [N] Patienten"
   • Feature Contributions zeigen: "Diese Faktoren unterstützen die Prognose"
   • Bei 100%: "Bestes bekanntes Prognoseprofil - individuelle Ergebnisse können variieren"

📝 NÄCHSTE SCHRITTE ZUR VALIDIERUNG:
   1. Originaldaten anfordern und Kalibrierungskurve erstellen
   2. Feature-Verteilungen prüfen: Gibt es Patienten mit ähnlichem Profil?
   3. Mit medizinischem Fachpersonal abgleichen: Sind Prognosen realistisch?
   4. Test-Set Performance analysieren: Precision, Recall, ROC-AUC
''')
