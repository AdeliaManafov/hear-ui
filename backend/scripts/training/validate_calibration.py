"""Script to validate model calibration and reliability.

This script checks if predicted probabilities match actual outcomes.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss, roc_auc_score, log_loss
from pathlib import Path


def load_test_data(csv_path: str):
    """Load test data with true outcomes."""
    df = pd.read_csv(csv_path)
    
    # Annahme: CSV hat Spalte 'Erfolg' (0 oder 1) für echtes Outcome
    # und alle anderen Spalten sind Features
    y_true = df['Erfolg'].values
    X = df.drop(columns=['Erfolg'])
    
    return X, y_true


def evaluate_calibration(model_path: str, test_csv: str, output_dir: str = "validation_results"):
    """Evaluate model calibration and generate report.
    
    Args:
        model_path: Path to trained pipeline
        test_csv: Path to test data CSV with 'Erfolg' column
        output_dir: Directory to save plots and report
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load model and data
    print("📂 Loading model...")
    pipeline = joblib.load(model_path)
    
    print("📂 Loading test data...")
    X_test, y_true = load_test_data(test_csv)
    
    # Get predictions
    print("🔮 Generating predictions...")
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    y_pred_binary = (y_pred_proba > 0.5).astype(int)
    
    # ==================== CALIBRATION CURVE ====================
    print("\n📊 Analyzing calibration...")
    
    # Calculate calibration curve
    fraction_of_positives, mean_predicted_value = calibration_curve(
        y_true, y_pred_proba, n_bins=10, strategy='quantile'
    )
    
    # Plot calibration curve
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Perfect calibration line
    ax.plot([0, 1], [0, 1], 'k--', label='Perfekt kalibriert')
    
    # Actual calibration
    ax.plot(mean_predicted_value, fraction_of_positives, 's-', 
            label='Unser Modell', markersize=10, linewidth=2)
    
    ax.set_xlabel('Vorhergesagte Wahrscheinlichkeit', fontsize=14)
    ax.set_ylabel('Tatsächliche Erfolgsrate', fontsize=14)
    ax.set_title('Kalibrierungskurve\n(Näher an Diagonale = besser)', fontsize=16)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    calibration_plot_path = f"{output_dir}/calibration_curve.png"
    plt.savefig(calibration_plot_path, dpi=300, bbox_inches='tight')
    print(f"✅ Calibration curve saved to {calibration_plot_path}")
    plt.close()
    
    # ==================== RELIABILITY DIAGRAM ====================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Calibration curve with confidence
    ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Perfekt')
    ax1.plot(mean_predicted_value, fraction_of_positives, 'o-', 
             markersize=8, label='Modell')
    
    # Add error bars
    bins = np.digitize(y_pred_proba, np.linspace(0, 1, 11))
    for i in range(1, 11):
        mask = bins == i
        if mask.sum() > 0:
            stderr = np.sqrt(fraction_of_positives[i-1] * (1 - fraction_of_positives[i-1]) / mask.sum())
            ax1.errorbar(mean_predicted_value[i-1], fraction_of_positives[i-1], 
                        yerr=1.96*stderr, fmt='none', color='red', alpha=0.5)
    
    ax1.set_xlabel('Vorhergesagte Wahrscheinlichkeit', fontsize=12)
    ax1.set_ylabel('Tatsächliche Rate', fontsize=12)
    ax1.set_title('Calibration mit 95% Konfidenz', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Right: Histogram of predictions
    ax2.hist(y_pred_proba[y_true == 1], bins=20, alpha=0.5, label='Erfolg (1)', color='green')
    ax2.hist(y_pred_proba[y_true == 0], bins=20, alpha=0.5, label='Misserfolg (0)', color='red')
    ax2.set_xlabel('Vorhergesagte Wahrscheinlichkeit', fontsize=12)
    ax2.set_ylabel('Anzahl Patienten', fontsize=12)
    ax2.set_title('Verteilung der Vorhersagen', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    reliability_plot_path = f"{output_dir}/reliability_diagram.png"
    plt.savefig(reliability_plot_path, dpi=300, bbox_inches='tight')
    print(f"✅ Reliability diagram saved to {reliability_plot_path}")
    plt.close()
    
    # ==================== METRICS ====================
    print("\n📈 Computing calibration metrics...")
    
    # Brier Score (lower is better, 0 = perfect)
    brier = brier_score_loss(y_true, y_pred_proba)
    
    # Log Loss (lower is better)
    logloss = log_loss(y_true, y_pred_proba)
    
    # AUC-ROC
    auc = roc_auc_score(y_true, y_pred_proba)
    
    # Accuracy
    accuracy = (y_pred_binary == y_true).mean()
    
    # Expected Calibration Error (ECE)
    ece = np.mean(np.abs(fraction_of_positives - mean_predicted_value))
    
    # ==================== REPORT ====================
    report = f"""
    ╔══════════════════════════════════════════════════════════╗
    ║         MODELL-KALIBRIERUNGS-BERICHT                     ║
    ╚══════════════════════════════════════════════════════════╝
    
    📊 KALIBRIERUNGS-METRIKEN
    ─────────────────────────────────────────────────────────
    
    🎯 Brier Score:              {brier:.4f}
       ├─ Bedeutung: Je niedriger, desto besser
       ├─ Perfekt: 0.0
       └─ Interpretation: {"✅ SEHR GUT" if brier < 0.1 else "⚠️ VERBESSERUNGSBEDARF" if brier < 0.2 else "❌ SCHLECHT"}
    
    📉 Log Loss:                 {logloss:.4f}
       ├─ Bedeutung: Je niedriger, desto besser
       └─ Interpretation: {"✅ GUT" if logloss < 0.5 else "⚠️ MITTEL" if logloss < 1.0 else "❌ SCHLECHT"}
    
    🎲 Expected Calibration Error (ECE):  {ece:.4f}
       ├─ Bedeutung: Durchschnittliche Abweichung
       ├─ Perfekt: 0.0
       └─ Interpretation: {"✅ EXZELLENT" if ece < 0.05 else "✅ GUT" if ece < 0.1 else "⚠️ MITTEL" if ece < 0.15 else "❌ SCHLECHT"}
    
    
    📈 ALLGEMEINE PERFORMANCE
    ─────────────────────────────────────────────────────────
    
    🔍 AUC-ROC:                  {auc:.4f}
       └─ Interpretation: {"✅ EXZELLENT" if auc > 0.9 else "✅ GUT" if auc > 0.8 else "⚠️ MITTEL" if auc > 0.7 else "❌ SCHLECHT"}
    
    ✓  Accuracy:                 {accuracy:.1%}
    
    
    📋 INTERPRETATION
    ─────────────────────────────────────────────────────────
    """
    
    # Add interpretation based on ECE
    if ece < 0.05:
        report += """
    ✅ EXZELLENTE KALIBRIERUNG!
    
    Die vorhergesagten Wahrscheinlichkeiten sind sehr zuverlässig.
    Wenn das Modell "70% Erfolg" sagt, kannst du dem vertrauen.
    
    Empfehlung: Modell ist produktionsreif!
        """
    elif ece < 0.1:
        report += """
    ✅ GUTE KALIBRIERUNG
    
    Die Wahrscheinlichkeiten sind weitgehend zuverlässig.
    Kleine Abweichungen sind normal und akzeptabel.
    
    Empfehlung: Modell kann verwendet werden. Optional: 
    Platt Scaling oder Isotonic Regression für perfekte Kalibrierung.
        """
    elif ece < 0.15:
        report += """
    ⚠️ MODERATE KALIBRIERUNG
    
    Die Wahrscheinlichkeiten weichen teilweise ab.
    Das Modell könnte zu optimistisch oder pessimistisch sein.
    
    Empfehlung: Kalibrierung mit Platt Scaling oder 
    Isotonic Regression dringend empfohlen!
        """
    else:
        report += """
    ❌ SCHLECHTE KALIBRIERUNG
    
    Die Wahrscheinlichkeiten sind NICHT zuverlässig!
    Modell sagt z.B. "90%", aber echte Rate ist nur 60%.
    
    Empfehlung: 
    1. Mehr Trainingsdaten sammeln
    2. Modell neu trainieren mit class_weight='balanced'
    3. Kalibrierung mit CalibratedClassifierCV durchführen
        """
    
    report += f"""
    
    📊 DETAILLIERTE CALIBRATION-BINS
    ─────────────────────────────────────────────────────────
    
    Bin | Vorhergesagt | Tatsächlich | Abweichung | Anzahl
    ────┼──────────────┼─────────────┼────────────┼────────
    """
    
    # Add bin details
    for i, (pred, actual) in enumerate(zip(mean_predicted_value, fraction_of_positives)):
        mask = bins == (i + 1)
        count = mask.sum()
        deviation = abs(pred - actual)
        status = "✅" if deviation < 0.1 else "⚠️" if deviation < 0.2 else "❌"
        report += f"  {i+1:2d} | {pred:12.1%} | {actual:11.1%} | {deviation:10.1%} | {count:6d} {status}\n"
    
    report += """
    ╚══════════════════════════════════════════════════════════╝
    """
    
    print(report)
    
    # Save report
    report_path = f"{output_dir}/calibration_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✅ Full report saved to {report_path}")
    
    # ==================== RECOMMENDATIONS ====================
    if ece > 0.1:
        print("\n🔧 VERBESSERUNGSVORSCHLAG:")
        print("   Führe Isotonic Calibration durch:")
        print("   ```python")
        print("   from sklearn.calibration import CalibratedClassifierCV")
        print("   calibrated = CalibratedClassifierCV(pipeline, method='isotonic', cv=5)")
        print("   calibrated.fit(X_train, y_train)")
        print("   ```")
    
    return {
        'brier_score': brier,
        'log_loss': logloss,
        'ece': ece,
        'auc': auc,
        'accuracy': accuracy
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python validate_calibration.py <model_path> <test_csv>")
        print("\nExample:")
        print("  python backend/scripts/validate_calibration.py \\")
        print("         backend/app/models/logreg_best_pipeline.pkl \\")
        print("         data/test_patients.csv")
        print("\nNote: test_csv must have 'Erfolg' column (0 or 1)")
        sys.exit(1)
    
    model_path = sys.argv[1]
    test_csv = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "validation_results"
    
    metrics = evaluate_calibration(model_path, test_csv, output_dir)
    
    print("\n" + "="*60)
    print("✅ Validation complete!")
    print(f"📂 Results saved in: {output_dir}/")
    print("="*60)
