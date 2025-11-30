#!/usr/bin/env python3
"""Test all patients from real CSV and generate report."""

import pandas as pd
import requests
import json
from collections import Counter

# Lade CSV
csv_path = '/Users/adeliamanafov/hearUI_project/hear-ui/data/sample_patients.csv'
df = pd.read_csv(csv_path)

print("="*80)
print("  VOLLSTÄNDIGER TEST MIT ALLEN PATIENTEN  ".center(80))
print("="*80)

# Spalten die das Modell braucht
columns_needed = [
    'Alter [J]',
    'Geschlecht',
    'Primäre Sprache',
    'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...',
    'Diagnose.Höranamnese.Ursache....Ursache...',
    'Symptome präoperativ.Tinnitus...',
    'Behandlung/OP.CI Implantation'
]

print(f"\n📊 Datensatz: {len(df)} Patienten")
print(f"API Endpoint: http://localhost:8000/api/v1/predict/")

results = []
errors = []

for idx in range(len(df)):
    row = df.iloc[idx]
    
    # Erstelle Patient-Dict - skip None/NaN values
    patient = {}
    for col in columns_needed:
        value = row.get(col)
        # Only include non-null values, let API use defaults for missing
        if pd.notna(value):
            patient[col] = value
    
    # API-Call
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/predict/",
            json=patient,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            pred = result.get('prediction', 0.0)
            
            results.append({
                'row': idx,
                'alter': patient.get('Alter [J]', 'N/A'),
                'onset': patient.get('Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...', 'N/A'),
                'geschlecht': patient.get('Geschlecht', 'N/A'),
                'prediction': pred
            })
        else:
            errors.append({
                'row': idx,
                'status': response.status_code,
                'error': response.text[:100]
            })
    except Exception as e:
        errors.append({
            'row': idx,
            'error': str(e)[:100]
        })

print(f"\n✅ Erfolgreiche Vorhersagen: {len(results)}/{len(df)}")
print(f"❌ Fehler: {len(errors)}")

if results:
    predictions = [r['prediction'] for r in results]
    
    print("\n" + "="*80)
    print("  STATISTIK  ".center(80))
    print("="*80)
    
    print(f"\n📈 Vorhersage-Verteilung:")
    print(f"  Minimum:     {min(predictions):.4f} ({min(predictions)*100:.1f}%)")
    print(f"  Maximum:     {max(predictions):.4f} ({max(predictions)*100:.1f}%)")
    print(f"  Durchschnitt: {sum(predictions)/len(predictions):.4f} ({sum(predictions)/len(predictions)*100:.1f}%)")
    print(f"  Median:      {sorted(predictions)[len(predictions)//2]:.4f}")
    
    # Anzahl unterschiedlicher Werte
    unique_rounded = len(set([round(p, 4) for p in predictions]))
    print(f"\n🎯 Unique Vorhersagen: {unique_rounded}")
    
    if unique_rounded == 1:
        print("  ❌ PROBLEM: Alle Vorhersagen sind identisch!")
    elif unique_rounded < 5:
        print(f"  ⚠️  NUR {unique_rounded} verschiedene Werte - Modell könnte zu einfach sein")
    else:
        print(f"  ✅ GUT: {unique_rounded} verschiedene Vorhersagen")
    
    # Verteilung nach Kategorien
    print(f"\n📊 Verteilung nach Onset-Typ:")
    onset_groups = {}
    for r in results:
        onset = r['onset'][:15] if isinstance(r['onset'], str) else 'Unknown'
        if onset not in onset_groups:
            onset_groups[onset] = []
        onset_groups[onset].append(r['prediction'])
    
    for onset, preds in sorted(onset_groups.items()):
        avg = sum(preds) / len(preds)
        print(f"  {onset:<20}: {len(preds):2d} Patienten, Ø {avg:.1%}")
    
    # Top 5 und Bottom 5
    sorted_results = sorted(results, key=lambda x: x['prediction'], reverse=True)
    
    print(f"\n🔝 TOP 5 (Beste Prognose):")
    for i, r in enumerate(sorted_results[:5], 1):
        print(f"  {i}. Patient {r['row']:2d}: {r['prediction']:.1%} "
              f"(Onset: {str(r['onset'])[:15]})")
    
    print(f"\n⬇️  BOTTOM 5 (Schlechteste Prognose):")
    for i, r in enumerate(sorted_results[-5:], 1):
        print(f"  {i}. Patient {r['row']:2d}: {r['prediction']:.1%} "
              f"(Onset: {str(r['onset'])[:15]})")

if errors:
    print(f"\n❌ FEHLER ({len(errors)}):")
    for err in errors[:5]:  # Zeige erste 5
        print(f"  Row {err['row']}: {err.get('error', 'Unknown error')[:60]}")

print("\n" + "="*80)
print("\n✅ TEST ABGESCHLOSSEN\n")

# Speichere Ergebnisse
results_df = pd.DataFrame(results)
results_df.to_csv('test_results_all_patients.csv', index=False)
print(f"💾 Ergebnisse gespeichert: test_results_all_patients.csv")
