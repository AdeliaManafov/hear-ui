#!/usr/bin/env python3
"""
Demo: Model Card Version Management

Zeigt wie man das Versionierungssystem für Model Cards verwendet.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.models.model_card.versioned_model_card import ModelCardManager


def main():
    print("=" * 70)
    print("Model Card Version Management Demo")
    print("=" * 70)
    print()
    
    # 1. Aktive Version anzeigen
    print("1️⃣  Aktive Version:")
    print("-" * 70)
    active_version = ModelCardManager.get_active_version()
    print(f"   ✅ Active: {active_version}")
    print()
    
    # 2. Alle Versionen auflisten
    print("2️⃣  Alle Versionen (Historie):")
    print("-" * 70)
    versions = ModelCardManager.list_all_versions()
    
    for i, v in enumerate(versions, 1):
        status_emoji = "✅" if v["status"] == "active" else "🔒"
        print(f"   {i}. {status_emoji} {v['version']} ({v['model_type']})")
        print(f"      Deployed: {v['deployment_date']}")
        if v["retired_date"]:
            print(f"      Retired:  {v['retired_date']}")
        print(f"      Accuracy: {v['accuracy']:.1%}")
        print()
    
    # 3. Aktive Model Card laden
    print("3️⃣  Aktive Model Card Details:")
    print("-" * 70)
    card = ModelCardManager.load_card()
    
    print(f"   Name:         {card['name']}")
    print(f"   Version:      {card['version']}")
    print(f"   Model Type:   {card['model_type']}")
    print(f"   Deployed:     {card['deployment_date']}")
    print(f"   Status:       {card['status']}")
    print()
    
    print("   📊 Metrics (Test Set):")
    metrics = card["metrics"]["test_set"]
    print(f"      - Accuracy:   {metrics['accuracy']:.1%}")
    print(f"      - Precision:  {metrics['precision']:.1%}")
    print(f"      - Recall:     {metrics['recall']:.1%}")
    print(f"      - F1 Score:   {metrics['f1_score']:.2f}")
    print(f"      - ROC AUC:    {metrics['roc_auc']:.2f}")
    print()
    
    print("   ⚠️  Limitations:")
    for lim in card["limitations"]:
        print(f"      - {lim}")
    print()
    
    print("   📝 Changelog:")
    print(f"      {card['changelog']}")
    print()
    
    # 4. Vergleich: v1 vs v2 vs v3
    print("4️⃣  Performance-Entwicklung:")
    print("-" * 70)
    
    v1 = ModelCardManager.load_card("v1_logreg_2025-11-15")
    v2 = ModelCardManager.load_card("v2_randomforest_2026-01-20")
    v3 = ModelCardManager.load_card("v3_randomforest_2026-02-17")
    
    print("   Version | Model Type          | Accuracy | F1 Score | ROC AUC")
    print("   --------|---------------------|----------|----------|--------")
    
    for version_card in [v1, v2, v3]:
        m = version_card["metrics"]["test_set"]
        model_type = version_card["model_type"][:19]  # Truncate
        print(f"   {version_card['version']:<7} | {model_type:<19} | "
              f"{m['accuracy']:>7.1%} | {m['f1_score']:>8.2f} | {m['roc_auc']:>7.2f}")
    
    print()
    improvement_v2 = (v2["metrics"]["test_set"]["accuracy"] - 
                      v1["metrics"]["test_set"]["accuracy"])
    improvement_v3 = (v3["metrics"]["test_set"]["accuracy"] - 
                      v2["metrics"]["test_set"]["accuracy"])
    
    print(f"   📈 v1 → v2: +{improvement_v2:.1%} accuracy improvement")
    print(f"   📈 v2 → v3: +{improvement_v3:.1%} accuracy improvement")
    print()
    
    # 5. Beispiel: Neue Version erstellen
    print("5️⃣  Beispiel: Neue Version erstellen")
    print("-" * 70)
    print("""
   from app.models.model_card.versioned_model_card import ModelCardManager
   
   # Neue Version erstellen
   ModelCardManager.create_new_version(
       version_id="v4_xgboost_2026-03-15",
       model_type="XGBoostClassifier",
       metrics={
           "accuracy": 0.81,
           "f1_score": 0.78,
           "precision": 0.76,
           "recall": 0.81,
           "roc_auc": 0.85
       },
       changelog="Upgraded to XGBoost with feature engineering. "
                 "Improved accuracy from 0.76 to 0.81.",
       training={
           "dataset_size": 150,
           "features_count": 45,
           "training_date": "2026-03-10"
       },
       limitations=[
           "Model trained on limited dataset (N=150)",
           "Requires careful hyperparameter tuning",
           "Higher computational cost than Random Forest"
       ]
   )
   
   # Alte Version archivieren
   ModelCardManager.retire_version(
       "v3_randomforest_2026-02-17",
       reason="Replaced by XGBoost with better performance"
   )
   
   # Neue Version aktivieren
   ModelCardManager.set_active_version("v4_xgboost_2026-03-15")
    """)
    
    print("=" * 70)
    print("✅ Demo abgeschlossen!")
    print("=" * 70)


if __name__ == "__main__":
    main()
