"""Generate enhanced background data for SHAP with realistic patient distributions."""

import pandas as pd
import numpy as np
from pathlib import Path

def generate_realistic_background(n_samples=100, random_state=42):
    """Generate realistic patient background data.
    
    Args:
        n_samples: Number of patients to generate
        random_state: Random seed for reproducibility
        
    Returns:
        DataFrame with realistic patient distributions
    """
    np.random.seed(random_state)
    
    patients = []
    
    for i in range(n_samples):
        # Age: Normal distribution around 45-55, realistic range
        age = np.clip(np.random.normal(50, 15), 18, 85)
        
        # Gender: Slightly more female patients (typical in CI population)
        gender = np.random.choice(['m', 'w'], p=[0.45, 0.55])
        
        # Language: Realistic distribution for German hospital
        language = np.random.choice(
            ['Deutsch', 'Englisch', 'Arabisch', 'Türkisch', 'Andere'],
            p=[0.65, 0.15, 0.08, 0.07, 0.05]
        )
        
        # Onset: Postlingual is most common (60%), then prelingual
        onset = np.random.choice(
            ['postlingual', 'praelingual', 'perilingual', '< 1 y', '1-5 y', '> 20 y', 'Unbekannt'],
            p=[0.40, 0.20, 0.10, 0.10, 0.10, 0.05, 0.05]
        )
        
        # Cause: Most cases are unknown or genetic
        cause = np.random.choice(
            ['Unbekannt', 'Genetisch', 'Lärm', 'Meningitis', 'Syndromal', 'Posttraumatisch'],
            p=[0.45, 0.25, 0.12, 0.08, 0.06, 0.04]
        )
        
        # Tinnitus: About 40% have tinnitus
        tinnitus = np.random.choice(
            ['ja', 'nein', 'Vorhanden', 'Kein'],
            p=[0.30, 0.50, 0.10, 0.10]
        )
        
        # Implant type: Cochlear is most common
        implant = np.random.choice(
            ['Cochlear', 'Med-El', 'Advanced Bionics'],
            p=[0.50, 0.30, 0.20]
        )
        
        patient = {
            'Alter [J]': age,
            'Geschlecht': gender,
            'Primäre Sprache': language,
            'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...': onset,
            'Diagnose.Höranamnese.Ursache....Ursache...': cause,
            'Symptome präoperativ.Tinnitus...': tinnitus,
            'Behandlung/OP.CI Implantation': implant
        }
        
        patients.append(patient)
    
    df = pd.DataFrame(patients)
    return df


if __name__ == "__main__":
    # Generate background data
    print("🔧 Generating realistic background data for SHAP...")
    
    df = generate_realistic_background(n_samples=100, random_state=42)
    
    # Save to models directory
    output_path = Path(__file__).parent.parent / "app" / "models" / "background_sample.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    
    print(f"✅ Created {len(df)} background patients")
    print(f"💾 Saved to: {output_path}")
    
    # Show statistics
    print("\n📊 Distribution:")
    print(f"  Age range: {df['Alter [J]'].min():.0f}-{df['Alter [J]'].max():.0f} years")
    print(f"  Mean age: {df['Alter [J]'].mean():.1f} years")
    print(f"  Gender: {(df['Geschlecht'] == 'w').sum()} female, {(df['Geschlecht'] == 'm').sum()} male")
    
    print("\n  Onset distribution:")
    for onset, count in df['Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...'].value_counts().head(5).items():
        print(f"    {onset}: {count}")
    
    print("\n  Language distribution:")
    for lang, count in df['Primäre Sprache'].value_counts().head(5).items():
        print(f"    {lang}: {count}")
