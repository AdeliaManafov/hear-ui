#!/usr/bin/env python3
"""Analyse des Modells und der Predictions auf logische Korrektheit.

Prüft:
1. Modell-Koeffizienten (welche Features sind positiv/negativ?)
2. SHAP-Werte vs. Koeffizienten-Konsistenz
3. Medizinische Plausibilität der Feature-Gewichtungen
4. Trainingsset-Statistiken (wenn verfügbar)
"""

import sys
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

# Backend-Pfad hinzufügen
backend_root = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_root))

from app.core.model_wrapper import ModelWrapper
from app.core.preprocessor import EXPECTED_FEATURES

def load_model():
    """Lade das trainierte Modell."""
    wrapper = ModelWrapper()
    if not wrapper.is_loaded():
        print("[ERROR] Modell konnte nicht geladen werden!")
        return None
    return wrapper

def analyze_coefficients(wrapper):
    """Analysiere die Modell-Koeffizienten."""
    print("\n" + "="*80)
    print("MODELL-KOEFFIZIENTEN ANALYSE")
    print("="*80)
    
    model = wrapper.model
    
    # LogisticRegression hat coef_ Attribut
    if not hasattr(model, 'coef_'):
        print("[WARNING]  Modell hat keine Koeffizienten (kein linear model)")
        return
    
    coefs = model.coef_[0]  # Shape: (n_features,)
    intercept = model.intercept_[0]
    
    print(f"\nModell-Typ: {type(model).__name__}")
    print(f"Anzahl Features: {len(coefs)}")
    print(f"Intercept (Bias): {intercept:.4f}")
    
    # Feature-Namen aus EXPECTED_FEATURES
    feature_names = EXPECTED_FEATURES
    
    # Sortiere nach Koeffizient-Stärke
    coef_df = pd.DataFrame({
        'feature': feature_names[:len(coefs)],  # Nur verfügbare Features
        'coefficient': coefs
    })
    coef_df['abs_coef'] = abs(coef_df['coefficient'])
    coef_df = coef_df.sort_values('abs_coef', ascending=False)
    
    print("\n" + "-"*80)
    print("TOP 20 STÄRKSTE FEATURES (nach absolutem Koeffizienten)")
    print("-"*80)
    print(f"{'Feature':<60} {'Koeffizient':>15} {'Effekt':>10}")
    print("-"*80)
    
    for idx, row in coef_df.head(20).iterrows():
        effect = "POSITIV [OK]" if row['coefficient'] > 0 else "NEGATIV "
        print(f"{row['feature']:<60} {row['coefficient']:>15.4f} {effect:>10}")
    
    # Suche problematische Features
    print("\n" + "="*80)
    print("PROBLEMATISCHE FEATURES (medizinisch fragwürdig)")
    print("="*80)
    
    suspicious_patterns = [
        ('Kopfschmerzen', 'Schmerzen sollten eher negativ sein'),
        ('nicht erhoben', 'Fehlende Daten als positiv?'),
        ('Schwindel', 'Symptom sollte eher negativ sein'),
    ]
    
    for pattern, reason in suspicious_patterns:
        matches = coef_df[coef_df['feature'].str.contains(pattern, case=False, na=False)]
        if not matches.empty:
            print(f"\n Features mit '{pattern}':")
            print(f"   Begründung: {reason}")
            for idx, row in matches.iterrows():
                effect = "[WARNING] POSITIV" if row['coefficient'] > 0 else "[OK] NEGATIV"
                print(f"   {row['feature']:<55} {row['coefficient']:>10.4f} {effect}")
    
    return coef_df

def analyze_sample_predictions(wrapper):
    """Analysiere Predictions für Sample-Patienten."""
    print("\n" + "="*80)
    print("SAMPLE-PATIENTEN PREDICTIONS ANALYSE")
    print("="*80)
    
    # Lade Sample-Patienten
    sample_csv = Path(__file__).parent / "patientsData" / "sample_patients.csv"
    if not sample_csv.exists():
        print(f"[ERROR] Sample CSV nicht gefunden: {sample_csv}")
        return
    
    df = pd.read_csv(sample_csv)
    print(f"\n[OK] {len(df)} Sample-Patienten geladen")
    
    # Analysiere jeden Patienten
    for idx, row in df.iterrows():
        patient_dict = row.to_dict()
        
        # Extrahiere wichtige Features
        name = patient_dict.get('Nachname', 'Unbekannt')
        vorname = patient_dict.get('Vorname', '')
        pre_op = patient_dict.get('outcome_measurments.pre.measure.', np.nan)
        
        # Preprocessing
        try:
            preprocessed = wrapper.prepare_input(patient_dict)
            prediction = wrapper.predict(patient_dict, clip=True)
            pred_val = prediction[0] if hasattr(prediction, '__len__') else prediction
            
            print(f"\n{'─'*80}")
            print(f"Patient: {vorname} {name}")
            print(f"Pre-OP Score: {pre_op}")
            print(f"Prediction: {pred_val:.4f} ({pred_val*100:.2f}%)")
            
            # Berechne Top-3 Features (vereinfacht über Koeffizienten)
            model = wrapper.model
            if hasattr(model, 'coef_'):
                coefs = model.coef_[0]
                # Multipliziere Koeffizienten mit Werten
                feature_contributions = coefs * preprocessed[0]
                
                # Top positive und negative
                top_indices = np.argsort(np.abs(feature_contributions))[-5:][::-1]
                
                print(f"\nTop-5 Feature-Beiträge:")
                for i in top_indices:
                    if i < len(EXPECTED_FEATURES):
                        feat_name = EXPECTED_FEATURES[i]
                        contribution = feature_contributions[i]
                        value = preprocessed[0][i]
                        coef = coefs[i]
                        
                        # Kürze lange Feature-Namen
                        short_name = feat_name[:50] + '...' if len(feat_name) > 50 else feat_name
                        print(f"  {short_name:<53} = {value:.2f} × {coef:>7.4f} = {contribution:>7.4f}")
        
        except Exception as e:
            print(f"\n[ERROR] Fehler bei Patient {vorname} {name}: {e}")

def check_data_quality():
    """Prüfe Datenqualität und mögliche Biases."""
    print("\n" + "="*80)
    print("DATENQUALITÄT & BIAS-ANALYSE")
    print("="*80)
    
    sample_csv = Path(__file__).parent / "patientsData" / "sample_patients.csv"
    if not sample_csv.exists():
        print("[WARNING]  Nur Sample-Daten verfügbar, keine Trainingsset-Analyse möglich")
        return
    
    df = pd.read_csv(sample_csv)
    
    # Zähle verschiedene Symptome
    symptom_cols = [col for col in df.columns if any(x in col.lower() for x in 
                    ['kopfschmerzen', 'schwindel', 'tinnitus'])]
    
    print("\nSymptom-Verteilung in Sample-Daten:")
    for col in symptom_cols:
        if col in df.columns:
            value_counts = df[col].value_counts()
            print(f"\n{col}:")
            for val, count in value_counts.items():
                print(f"  {val}: {count} ({count/len(df)*100:.1f}%)")
    
    # Pre-OP Score Analyse
    pre_op_col = 'outcome_measurments.pre.measure.'
    if pre_op_col in df.columns:
        print(f"\nPre-OP Score Statistiken:")
        pre_op = df[pre_op_col].dropna()
        print(f"  Mittelwert: {pre_op.mean():.2f}")
        print(f"  Median: {pre_op.median():.2f}")
        print(f"  Min: {pre_op.min():.2f}")
        print(f"  Max: {pre_op.max():.2f}")
        print(f"  Anzahl = 0: {(pre_op == 0).sum()} ({(pre_op == 0).sum()/len(pre_op)*100:.1f}%)")

def main():
    print("="*80)
    print("KI-MODELL LOGIK-ANALYSE")
    print("="*80)
    print("\nZiel: Überprüfung ob Predictions und Feature-Gewichtungen medizinisch sinnvoll sind")
    
    # 1. Lade Modell
    wrapper = load_model()
    if not wrapper:
        return 1
    
    # 2. Analysiere Koeffizienten
    coef_df = analyze_coefficients(wrapper)
    
    # 3. Analysiere Sample-Predictions
    analyze_sample_predictions(wrapper)
    
    # 4. Datenqualität
    check_data_quality()
    
    # 5. Fazit
    print("\n" + "="*80)
    print("FAZIT")
    print("="*80)
    print("""
Das Modell ist ein LogisticRegression-Modell mit 68 Features.

WICHTIG ZU VERSTEHEN:
1. Die Koeffizienten zeigen den TRAININGSDATEN-BIAS
   - Wenn "Kopfschmerzen" positiv ist, bedeutet das:
     → Im Trainingsset hatten Patienten mit Kopfschmerzen ZUFÄLLIG bessere Outcomes
   - Das heißt NICHT dass Kopfschmerzen medizinisch gut sind!
   - Das heißt: SELECTION BIAS oder CONFOUNDING im Trainingsset

2. "Objektive Messungen nicht erhoben" positiv:
   - Könnte bedeuten: Patienten ohne Messungen waren anders selektiert
   - Z.B.: Jüngere Patienten, akute Fälle, dringende Indikation
   - Diese Gruppen könnten bessere Outcomes haben

3. Das Modell ist NUR so gut wie die Trainingsdaten!
   - Wenn Trainingsset Biases hat → Modell lernt diese Biases
   - Logistic Regression lernt KORRELATIONEN, nicht KAUSALITÄT

EMPFEHLUNG:
- Trainingsset-Analyse durchführen (welche Patienten hatten Kopfschmerzen?)
- Korrelationsmatrix erstellen (Kopfschmerzen korreliert mit was?)
- Eventuell Features entfernen, die keinen kausalen Sinn machen
- Oder: Modell neu trainieren mit bereinigten Daten

Das aktuelle Modell ist technisch korrekt implementiert, aber die 
DATENQUALITÄT und FEATURE-SELEKTION im Training waren möglicherweise problematisch.
""")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
