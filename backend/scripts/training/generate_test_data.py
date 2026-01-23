"""Generate synthetic test data for calibration validation.

This creates realistic patient data with simulated outcomes.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def generate_test_patients(n_samples=200, random_state=42):
    """Generate synthetic patient data with outcomes.
    
    Args:
        n_samples: Number of patients to generate
        random_state: Random seed for reproducibility
        
    Returns:
        DataFrame with patient features and 'Erfolg' column (0 or 1)
    """
    np.random.seed(random_state)
    
    patients = []
    
    for i in range(n_samples):
        # Generate patient features
        age = np.clip(np.random.normal(50, 12), 18, 85)
        gender = np.random.choice(['m', 'w'], p=[0.45, 0.55])
        language = np.random.choice(['Deutsch', 'Englisch', 'Andere'], p=[0.7, 0.2, 0.1])
        
        onset = np.random.choice(
            ['postlingual', 'praelingual', 'perilingual'],
            p=[0.6, 0.3, 0.1]
        )
        
        cause = np.random.choice(
            ['Unbekannt', 'Genetisch', 'Lärm', 'Meningitis'],
            p=[0.5, 0.25, 0.15, 0.1]
        )
        
        tinnitus = np.random.choice(['ja', 'nein'], p=[0.4, 0.6])
        
        implant = np.random.choice(
            ['Cochlear', 'Advanced Bionics', 'Med-El'],
            p=[0.5, 0.3, 0.2]
        )
        
        # Simulate realistic outcome based on features
        # Postlingual patients have better outcomes
        success_prob = 0.5  # Base probability
        
        if onset == 'postlingual':
            success_prob += 0.3
        elif onset == 'praelingual':
            success_prob -= 0.2
        
        # Age factor (middle-aged better)
        if 30 <= age <= 60:
            success_prob += 0.1
        elif age > 70:
            success_prob -= 0.15
        
        # Tinnitus slightly negative
        if tinnitus == 'ja':
            success_prob -= 0.05
        
        # Genetic cause is slightly better
        if cause == 'Genetisch':
            success_prob += 0.05
        
        # Add some randomness
        success_prob += np.random.normal(0, 0.1)
        success_prob = np.clip(success_prob, 0.1, 0.95)
        
        # Determine outcome
        success = 1 if np.random.random() < success_prob else 0
        
        patient = {
            'Alter [J]': int(age),
            'Geschlecht': gender,
            'Primäre Sprache': language,
            'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...': onset,
            'Diagnose.Höranamnese.Ursache....Ursache...': cause,
            'Symptome präoperativ.Tinnitus...': tinnitus,
            'Behandlung/OP.CI Implantation': implant,
            'Erfolg': success
        }
        
        patients.append(patient)
    
    df = pd.DataFrame(patients)
    return df


if __name__ == "__main__":
    # Create output directory
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    print("🔧 Generating synthetic test data...")
    
    # Generate test set (200 patients)
    df_test = generate_test_patients(n_samples=200, random_state=42)
    
    output_path = data_dir / "test_patients_synthetic.csv"
    df_test.to_csv(output_path, index=False)
    
    print(f"[OK] Created {len(df_test)} test patients")
    print(f"[STATS] Success rate: {df_test['Erfolg'].mean():.1%}")
    print(f"💾 Saved to: {output_path}")
    
    # Show distribution
    print("\n📈 Distribution:")
    print(f"   Postlingual: {(df_test['Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...'] == 'postlingual').mean():.1%}")
    print(f"   With Tinnitus: {(df_test['Symptome präoperativ.Tinnitus...'] == 'ja').mean():.1%}")
    print(f"   Age range: {df_test['Alter [J]'].min()}-{df_test['Alter [J]'].max()} years")
    print(f"   Mean age: {df_test['Alter [J]'].mean():.1f} years")
