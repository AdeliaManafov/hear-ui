# CSV-Daten und Modell-Kompatibilität

## Übersicht

Das KI-Modell (`logreg_best_model.pkl`) wurde mit einem spezifischen Feature-Set trainiert.
Die CSV-Datei `Dummy Data_Cochlear Implant.csv` enthält mehr Spalten als das Modell benötigt.

## CSV-Spalten (34 Spalten)

| CSV-Spalte | Verwendet im Modell | Anmerkung |
|------------|---------------------|-----------|
| `ID` |  Nein | Nur Identifikator |
| `Geschlecht` |  Ja | → `Geschlecht_m`, `Geschlecht_w` (one-hot) |
| `Alter [J]` |  Ja | Numerisch |
| `Primäre Sprache` |  Nein | Nicht im Training |
| `Weitere Sprachen` |  Nein | Nicht im Training |
| `Deutsch Sprachbarriere` |  Nein | Nicht im Training |
| `non-verbal` |  Nein | Nicht im Training |
| `Eltern m. Schwerhörigkeit` |  Nein | Familienhistorie nicht im Training |
| `Geschwister m. SH` |  Nein | Familienhistorie nicht im Training |
| `Seiten` |  Ja | L=1, R=2 |
| `Symptome präoperativ.Geschmack...` |  Ja | Binär (0/1) |
| `Symptome präoperativ.Tinnitus...` |  Ja | Binär (0/1) |
| `Symptome präoperativ.Schwindel...` |  Ja | Binär (0/1) |
| `Symptome präoperativ.Otorrhoe...` |  Ja | Binär (0/1) |
| `Symptome präoperativ.Kopfschmerzen...` |  Ja | Binär (0/1) |
| `Bildgebung, präoperativ.Typ...` |  Nein | Nur `.Befunde...` wird verwendet |
| `Bildgebung, präoperativ.Befunde...` |  Ja | One-hot encoded (10 Kategorien) |
| `Objektive Messungen.OAE...` |  Nein | Nicht im Modell |
| `Objektive Messungen.LL...` |  Ja | One-hot encoded (3 Kategorien) |
| `Objektive Messungen.4000 Hz...` |  Ja | One-hot encoded (3 Kategorien) |
| `Diagnose.Höranamnese.Hörminderung operiertes Ohr...` |  Ja | Ordinal |
| `Diagnose.Höranamnese.Versorgung operiertes Ohr...` |  Ja | One-hot encoded |
| `Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...` |  Ja | Ordinal |
| `Diagnose.Höranamnese.Erwerbsart...` |  Ja | One-hot encoded |
| `Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...` |  Ja | Ordinal |
| `Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)...` |  Ja | Ordinal |
| `Diagnose.Höranamnese.Ursache....Ursache...` |  Ja | One-hot encoded (9 Kategorien) |
| `Diagnose.Höranamnese.Art der Hörstörung...` |  Ja | One-hot encoded |
| `Diagnose.Höranamnese.Hörminderung Gegenohr...` |  Ja | Ordinal |
| `Diagnose.Höranamnese.Versorgung Gegenohr...` |  Ja | One-hot encoded |
| `Behandlung/OP.CI Implantation` |  Ja | One-hot encoded (11 Kategorien) |
| `outcome_measurments.post24.measure.` |  **Zielvariable** | Post-24-Monate Messung (Target) |
| `outcome_measurments.post12.measure.` |  **Zielvariable** | Post-12-Monate Messung (Target) |
| `outcome_measurments.pre.measure.` |  Ja | Prä-operative Messung (Feature) |
| `abstand` |  Ja | Tage zwischen Messungen |

## Modell-Features (68 Features)

Das Modell erwartet nach One-Hot-Encoding genau **68 Features**:

- 15 numerische/ordinale Features
- 2 Geschlecht-Features (one-hot)
- 10 Bildgebung-Features (one-hot)
- 3 LL-Messungen (one-hot)
- 3 4000Hz-Messungen (one-hot)
- 9 Ursache-Features (one-hot)
- 3 Versorgung Gegenohr (one-hot)
- 11 CI-Implantat-Typen (one-hot)
- 4 Versorgung operiertes Ohr (one-hot)
- 3 Erwerbsart (one-hot)
- 4 Art der Hörstörung (one-hot)

## Preprocessing

Der `preprocessor.py` transformiert Patientendaten in das 68-Feature-Format:

```python
from app.core.preprocessor import preprocess_patient_data

# Rohe Patientendaten (z.B. aus CSV oder API)
raw_data = {
    "Alter [J]": 55,
    "Geschlecht": "w",
    "Seiten": "L",
    # ... weitere Felder
}

# Transformiert zu 68-Feature DataFrame
X = preprocess_patient_data(raw_data)
```

## Zielvariable

Die Zielvariable für das Modell ist die **Erfolgswahrscheinlichkeit** eines Cochlea-Implantats.
Diese wird aus den Post-Messungen (`post12` oder `post24`) abgeleitet und ist NICHT Teil der Eingabe-Features.
