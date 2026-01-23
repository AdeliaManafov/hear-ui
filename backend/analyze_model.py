#!/usr/bin/env python3
"""Deep-dive into model coefficients and baseline behavior."""

from app.core.model_wrapper import ModelWrapper
from app.core.preprocessor import EXPECTED_FEATURES, preprocess_patient_data
import numpy as np

def main():
    w = ModelWrapper()
    
    print("=" * 60)
    print("WARUM SIND DIE VORHERSAGEN SO HOCH?")
    print("=" * 60)
    
    # 1. Intercept-Analyse
    intercept = w.model.intercept_[0]
    print(f"\n1. INTERCEPT (Basis-Wert): {intercept:.4f}")
    
    # Sigmoid des Intercepts = Basis-Wahrscheinlichkeit wenn alle Features 0 sind
    base_prob = 1 / (1 + np.exp(-intercept))
    print(f"   -> Basis-Wahrscheinlichkeit (alle Features=0): {base_prob:.1%}")
    print(f"   -> Das erklärt die hohe Basis-Vorhersage!")
    
    # 2. Koeffizienten-Analyse
    coef = w.model.coef_[0]
    print(f"\n2. KOEFFIZIENTEN-ANALYSE")
    print(f"   Anzahl: {len(coef)}")
    print(f"   Min: {coef.min():.4f}")
    print(f"   Max: {coef.max():.4f}")
    print(f"   Mittelwert: {coef.mean():.4f}")
    
    # Top positive und negative Koeffizienten
    print(f"\n3. TOP 10 POSITIVE KOEFFIZIENTEN (erhöhen Vorhersage)")
    sorted_idx = np.argsort(coef)[::-1]
    for i in range(10):
        idx = sorted_idx[i]
        print(f"   {EXPECTED_FEATURES[idx]}: +{coef[idx]:.4f}")
    
    print(f"\n4. TOP 10 NEGATIVE KOEFFIZIENTEN (senken Vorhersage)")
    for i in range(10):
        idx = sorted_idx[-(i+1)]
        print(f"   {EXPECTED_FEATURES[idx]}: {coef[idx]:.4f}")
    
    # 3. Was passiert bei einem realistischen Patienten?
    print("\n" + "=" * 60)
    print("DETAILLIERTE VORHERSAGE FÜR REALISTISCHEN PATIENTEN")
    print("=" * 60)
    
    realistic_patient = {
        "Alter [J]": 55,
        "Geschlecht": "w",
        "Seiten": "L",
        "Symptome präoperativ.Tinnitus...": 1,
        "outcome_measurments.pre.measure.": 25,
        "abstand": 365,
        "Diagnose.Höranamnese.Hörminderung operiertes Ohr...": 3,
    }
    
    X = preprocess_patient_data(realistic_patient)
    prob = w.predict(realistic_patient)[0]
    
    print(f"\nInput: {realistic_patient}")
    print(f"Vorhersage: {prob:.1%}")
    
    # Beiträge aufschlüsseln
    print("\nBeiträge der einzelnen Features zum Log-Odds:")
    contributions = coef * X.values[0]
    non_zero = [(EXPECTED_FEATURES[i], contributions[i], X.values[0][i]) 
                for i in range(len(contributions)) if abs(contributions[i]) > 0.01]
    non_zero.sort(key=lambda x: abs(x[1]), reverse=True)
    
    total_contrib = sum(c[1] for c in non_zero)
    print(f"\nIntercept: +{intercept:.4f}")
    for name, contrib, value in non_zero[:15]:
        sign = "+" if contrib > 0 else ""
        print(f"  {name} (Wert={value:.2f}): {sign}{contrib:.4f}")
    print(f"\nSumme Feature-Beiträge: {total_contrib:.4f}")
    print(f"Log-Odds gesamt: {intercept + total_contrib:.4f}")
    print(f"-> Wahrscheinlichkeit: {prob:.1%}")

if __name__ == "__main__":
    main()
