"""Quick calibration check without plots (no matplotlib needed)."""

import numpy as np
import pandas as pd
import joblib
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, roc_auc_score, log_loss


def quick_calibration_check(model_path: str, test_csv: str):
    """Quick calibration evaluation without plots.
    
    Args:
        model_path: Path to trained pipeline
        test_csv: Path to test CSV with 'Erfolg' column
    """
    print("📂 Loading model...")
    pipeline = joblib.load(model_path)
    
    print("📂 Loading test data...")
    df = pd.read_csv(test_csv)
    y_true = df['Erfolg'].values
    X_test = df.drop(columns=['Erfolg'])
    
    print("🔮 Generating predictions...")
    
    # Check if model is classifier or regressor
    try:
        y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    except AttributeError:
        # Regressor - use predict() and clip to [0, 1]
        y_pred_proba = np.clip(pipeline.predict(X_test), 0, 1)
    
    y_pred_binary = (y_pred_proba > 0.5).astype(int)
    
    print("\n" + "="*70)
    print("[STATS] KALIBRIERUNGS-BERICHT".center(70))
    print("="*70)
    
    # Calibration curve
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_true, y_pred_proba, n_bins=10, strategy='quantile'
    )
    
    # Metrics
    brier = brier_score_loss(y_true, y_pred_proba)
    logloss = log_loss(y_true, y_pred_proba)
    auc = roc_auc_score(y_true, y_pred_proba)
    accuracy = (y_pred_binary == y_true).mean()
    ece = np.mean(np.abs(fraction_of_positives - mean_predicted_value))
    
    print(f"\n🎯 KALIBRIERUNGS-METRIKEN")
    print("-" * 70)
    print(f"  Brier Score:              {brier:.4f}", end="")
    if brier < 0.1:
        print("  [OK] SEHR GUT")
    elif brier < 0.2:
        print("  [WARN]  OK")
    else:
        print("  [FAIL] SCHLECHT")
    
    print(f"  Log Loss:                 {logloss:.4f}", end="")
    if logloss < 0.5:
        print("  [OK] GUT")
    elif logloss < 1.0:
        print("  [WARN]  MITTEL")
    else:
        print("  [FAIL] SCHLECHT")
    
    print(f"  Expected Calibration Error: {ece:.4f}", end="")
    if ece < 0.05:
        print("  [OK] EXZELLENT")
    elif ece < 0.1:
        print("  [OK] GUT")
    elif ece < 0.15:
        print("  [WARN]  MITTEL")
    else:
        print("  [FAIL] SCHLECHT")
    
    print(f"\n📈 ALLGEMEINE PERFORMANCE")
    print("-" * 70)
    print(f"  AUC-ROC:                  {auc:.4f}", end="")
    if auc > 0.9:
        print("  [OK] EXZELLENT")
    elif auc > 0.8:
        print("  [OK] GUT")
    elif auc > 0.7:
        print("  [WARN]  MITTEL")
    else:
        print("  [FAIL] SCHLECHT")
    
    print(f"  Accuracy:                 {accuracy:.1%}")
    print(f"  True Success Rate:        {y_true.mean():.1%}")
    print(f"  Predicted Avg:            {y_pred_proba.mean():.1%}")
    
    print(f"\n📋 CALIBRATION BINS")
    print("-" * 70)
    print("Bin | Vorhergesagt | Tatsächlich | Abweichung | Anzahl | Status")
    print("-" * 70)
    
    bins = np.digitize(y_pred_proba, np.linspace(0, 1, 11))
    for i, (pred, actual) in enumerate(zip(mean_predicted_value, fraction_of_positives)):
        mask = bins == (i + 1)
        count = mask.sum()
        deviation = abs(pred - actual)
        status = "[OK]" if deviation < 0.1 else "[WARN] " if deviation < 0.2 else "[FAIL]"
        print(f" {i+1:2d} | {pred:11.1%} | {actual:11.1%} | {deviation:10.1%} | {count:6d} | {status}")
    
    print("\n" + "="*70)
    print("💡 INTERPRETATION")
    print("="*70)
    
    if ece < 0.05:
        print("""
[OK] EXZELLENTE KALIBRIERUNG!

Die vorhergesagten Wahrscheinlichkeiten sind sehr zuverlässig.
Wenn das Modell "70% Erfolg" sagt, kannst du dem vertrauen.

>  Empfehlung: Modell ist produktionsreif!
        """)
    elif ece < 0.1:
        print("""
[OK] GUTE KALIBRIERUNG

Die Wahrscheinlichkeiten sind weitgehend zuverlässig.
Kleine Abweichungen sind normal und akzeptabel.

>  Empfehlung: Modell kann verwendet werden.
    Optional: Isotonic Regression für perfekte Kalibrierung.
        """)
    elif ece < 0.15:
        print("""
[WARN]  MODERATE KALIBRIERUNG

Die Wahrscheinlichkeiten weichen teilweise ab.
Das Modell könnte zu optimistisch oder pessimistisch sein.

>  Empfehlung: Kalibrierung mit Isotonic Regression empfohlen!
        """)
    else:
        print("""
[FAIL] SCHLECHTE KALIBRIERUNG

Die Wahrscheinlichkeiten sind NICHT zuverlässig!

>  Empfehlung:
    1. Mehr Trainingsdaten sammeln
    2. Modell mit CalibratedClassifierCV neu trainieren
    3. Feature Engineering überprüfen
        """)
    
    print("="*70)
    
    if ece > 0.1:
        print("\n🔧 VERBESSERUNGS-CODE:")
        print("""
from sklearn.calibration import CalibratedClassifierCV
import joblib

# Lade Modell
pipeline = joblib.load('backend/app/models/logreg_best_pipeline.pkl')

# Kalibriere
calibrated = CalibratedClassifierCV(pipeline, method='isotonic', cv=5)
calibrated.fit(X_train, y_train)

# Speichere
joblib.dump(calibrated, 'backend/app/models/logreg_calibrated.pkl')
        """)
    
    return {
        'brier': brier,
        'ece': ece,
        'auc': auc,
        'accuracy': accuracy
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python quick_calibration_check.py <model_path> <test_csv>")
        print("\nExample:")
        print("  python backend/scripts/quick_calibration_check.py \\")
        print("         backend/app/models/logreg_best_pipeline.pkl \\")
        print("         data/test_patients_synthetic.csv")
        sys.exit(1)
    
    model_path = sys.argv[1]
    test_csv = sys.argv[2]
    
    metrics = quick_calibration_check(model_path, test_csv)
    
    print(f"\n[OK] Validation complete!")
    print(f"   ECE: {metrics['ece']:.4f} | Brier: {metrics['brier']:.4f} | AUC: {metrics['auc']:.4f}")
