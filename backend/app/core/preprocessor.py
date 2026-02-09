"""Preprocessing module for HEAR CI prediction model.

This module handles the transformation of patient data from the API format
to the 68-feature format expected by the LogisticRegression model.

CSV Data Compatibility Note:
============================
The CSV file (Dummy Data_Cochlear Implant.csv) contains 34 columns.
Not all columns are used by the ML model. The following columns are
EXCLUDED from the model because they were not part of the training data:

UNUSED CSV COLUMNS (not in model):
- ID                              -> Only used as identifier, not a feature
- Primäre Sprache                 -> Language info not in model training
- Weitere Sprachen                -> Language info not in model training
- Deutsch Sprachbarriere          -> Language barrier not in model training
- non-verbal                      -> Not in model training data
- Eltern m. Schwerhörigkeit       -> Family history not in model training
- Geschwister m. SH               -> Family history not in model training
- Bildgebung, präoperativ.Typ...  -> Only .Befunde... (findings) is used
- Objektive Messungen.OAE...      -> Only LL... and 4000 Hz... are used
- outcome_measurments.post24...   -> This is TARGET variable (not a feature)
- outcome_measurments.post12...   -> This is TARGET variable (not a feature)

USED CSV COLUMNS -> MODEL FEATURES:
- Geschlecht                      -> Geschlecht_m, Geschlecht_w (one-hot)
- Alter [J]                       -> Alter [J] (numeric)
- Seiten                          -> Seiten (L=1, R=2)
- Symptome präoperativ.*          -> Binary features (0/1)
- Bildgebung, präoperativ.Befunde -> One-hot encoded categories
- Objektive Messungen.LL...       -> One-hot encoded categories
- Objektive Messungen.4000 Hz...  -> One-hot encoded categories
- Diagnose.Höranamnese.*          -> Various numeric/one-hot features
- Behandlung/OP.CI Implantation   -> One-hot encoded implant types
- outcome_measurments.pre.measure -> Pre-operative measure (feature)
- abstand                         -> Days between measurements (feature)

The model expects exactly 68 features after one-hot encoding.
"""

from typing import Any

import numpy as np
import pandas as pd


def _safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float with fallback to default."""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


# Complete list of 68 features expected by the model (in order)
EXPECTED_FEATURES = [
    "PID",
    "Alter [J]",
    "Seiten",
    "Symptome präoperativ.Geschmack...",
    "Symptome präoperativ.Tinnitus...",
    "Symptome präoperativ.Schwindel...",
    "Symptome präoperativ.Otorrhoe...",
    "Symptome präoperativ.Kopfschmerzen...",
    "Diagnose.Höranamnese.Hörminderung operiertes Ohr...",
    "Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...",
    "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...",
    "Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)...",
    "Diagnose.Höranamnese.Hörminderung Gegenohr...",
    "outcome_measurments.pre.measure.",
    "abstand",
    "Geschlecht_m",
    "Geschlecht_w",
    "Bildgebung, präoperativ.Befunde..._Anomalie der Bogengänge, Sonstige",
    "Bildgebung, präoperativ.Befunde..._Cochleäre Fehlbildung (Sennaroglu), Anomalie der Bogengänge",
    "Bildgebung, präoperativ.Befunde..._Cochleäre Ossifikation",
    "Bildgebung, präoperativ.Befunde..._Gehirnpathologie",
    "Bildgebung, präoperativ.Befunde..._Normalbefund",
    "Bildgebung, präoperativ.Befunde..._Normalbefund, Sonstige",
    "Bildgebung, präoperativ.Befunde..._Otosklerose",
    "Bildgebung, präoperativ.Befunde..._Sonstige",
    "Bildgebung, präoperativ.Befunde..._Sonstige, Cochleäre Ossifikation",
    "Bildgebung, präoperativ.Befunde..._Sonstige, Otosklerose",
    "Bildgebung, präoperativ.Befunde..._nan",
    "Objektive Messungen.LL..._Keine Reizantwort",
    "Objektive Messungen.LL..._Nicht erhoben",
    "Objektive Messungen.LL..._Schwelle",
    "Objektive Messungen.4000 Hz..._Keine Reizantwort",
    "Objektive Messungen.4000 Hz..._Nicht erhoben",
    "Objektive Messungen.4000 Hz..._Schwelle",
    "Diagnose.Höranamnese.Ursache....Ursache..._Andere",
    "Diagnose.Höranamnese.Ursache....Ursache..._Hörsturz",
    "Diagnose.Höranamnese.Ursache....Ursache..._Hörsturz, M. Menière",
    "Diagnose.Höranamnese.Ursache....Ursache..._Infektiös",
    "Diagnose.Höranamnese.Ursache....Ursache..._M. Menière",
    "Diagnose.Höranamnese.Ursache....Ursache..._Other",
    "Diagnose.Höranamnese.Ursache....Ursache..._Syndromal",
    "Diagnose.Höranamnese.Ursache....Ursache..._unknown",
    "Diagnose.Höranamnese.Ursache....Ursache..._nan",
    "Diagnose.Höranamnese.Versorgung Gegenohr..._CI",
    "Diagnose.Höranamnese.Versorgung Gegenohr..._Hörgerät",
    "Diagnose.Höranamnese.Versorgung Gegenohr..._Keine Versorgung",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Advanced Bionics... HiRes Ultra (HiFocus SlimJ)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Advanced Bionics... HiRes Ultra 3D (HiFocus Mid-Scala)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Advanced Bionics... HiRes Ultra 3D (HiFocus SlimJ)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile CI512 (Contour Advance)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile CI522 (Slim Straight)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile CI532 (Slim Modiolar)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile Plus CI612 (Contour Advance)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile Plus CI622 (Slim Straight)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile Plus CI632 (Slim Modiolar)",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.MED-EL... Implantattyp, Elektrodentyp",
    "Behandlung/OP.CI Implantation_Behandlung/OP.CI Implantation.Oticon Medical... Neuro Zti EVO",
    "Diagnose.Höranamnese.Versorgung operiertes Ohr..._Hörgerät",
    "Diagnose.Höranamnese.Versorgung operiertes Ohr..._Keine Versorgung",
    "Diagnose.Höranamnese.Versorgung operiertes Ohr..._Nicht erhoben",
    "Diagnose.Höranamnese.Versorgung operiertes Ohr..._Sonstige",
    "Diagnose.Höranamnese.Erwerbsart..._Plötzlich",
    "Diagnose.Höranamnese.Erwerbsart..._Progredient",
    "Diagnose.Höranamnese.Erwerbsart..._unknown",
    "Diagnose.Höranamnese.Art der Hörstörung..._Cochleär",
    "Diagnose.Höranamnese.Art der Hörstörung..._Nicht erhoben",
    "Diagnose.Höranamnese.Art der Hörstörung..._Schallleitung",
    "Diagnose.Höranamnese.Art der Hörstörung..._Sonstige",
]


def preprocess_patient_data(raw: dict) -> np.ndarray:
    """Convert raw patient dict into 68-feature array for the model.

    This function handles the transformation from user-friendly input
    to the exact feature format expected by random_forest_final.pkl.

    Args:
        raw: Dictionary with patient data (can use German or simplified keys)

    Returns:
        numpy array of shape (1, 68) with all features
    """
    # Initialize all features with zeros (default for one-hot encoded)
    features = dict.fromkeys(EXPECTED_FEATURES, 0.0)

    # --- Numeric features ---
    features["PID"] = _safe_float(raw.get("PID", raw.get("pid", 0)), 0.0)
    features["Alter [J]"] = _safe_float(
        raw.get("Alter [J]", raw.get("alter", raw.get("age", 50))), 50.0
    )

    # Seiten: L=1, R=2
    seiten_val = raw.get("Seiten", raw.get("seite", raw.get("implant_side", 1)))
    if isinstance(seiten_val, str):
        seiten_val = 1.0 if seiten_val.lower() in ["l", "links", "left"] else 2.0
    features["Seiten"] = _safe_float(seiten_val, 1.0)

    features["abstand"] = _safe_float(
        raw.get("abstand", raw.get("days_between", raw.get("time_since_surgery", 365))),
        365.0,
    )
    features["outcome_measurments.pre.measure."] = _safe_float(
        raw.get("outcome_measurments.pre.measure.", raw.get("pre_measure", 0)), 0.0
    )

    # --- Binary symptom features (0 or 1) ---
    symptom_fields = {
        "Symptome präoperativ.Geschmack...": ["geschmack", "taste"],
        "Symptome präoperativ.Tinnitus...": ["tinnitus"],
        "Symptome präoperativ.Schwindel...": ["schwindel", "vertigo", "dizziness"],
        "Symptome präoperativ.Otorrhoe...": ["otorrhoe", "ear_discharge"],
        "Symptome präoperativ.Kopfschmerzen...": ["kopfschmerzen", "headache"],
    }

    for feature_name, aliases in symptom_fields.items():
        value = raw.get(feature_name, None)
        if value is None:
            for alias in aliases:
                if alias in raw:
                    value = raw[alias]
                    break
        if value is not None:
            # Handle pandas Series by extracting scalar value
            if hasattr(value, "iloc"):
                value = value.iloc[0] if len(value) > 0 else None
            if value is None:
                continue
            if isinstance(value, str):
                # Recognize German symptom values: "Vorhanden" = present, "Kein/Keine" = absent
                positive_values = ["ja", "yes", "1", "true", "vorhanden"]
                features[feature_name] = (
                    1.0 if value.lower().strip() in positive_values else 0.0
                )
            else:
                features[feature_name] = 1.0 if bool(value) else 0.0

    # --- Diagnosis features that are actually categorical/ordinal ---
    # These need special handling as they can be text values
    diagnosis_ordinal = {
        "Diagnose.Höranamnese.Hörminderung operiertes Ohr...": [
            "hearing_loss_operated",
            "hoerminderung_op",
        ],
        "Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...": [
            "time_of_loss",
            "zeitpunkt",
        ],
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": [
            "onset",
            "beginn",
            "hearing_loss_onset",
        ],
        "Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)...": [
            "severe_loss",
            "hochgradig",
        ],
        "Diagnose.Höranamnese.Hörminderung Gegenohr...": [
            "hearing_loss_other",
            "hoerminderung_gegen",
        ],
    }

    # Map ordinal string values to numeric
    ORDINAL_MAPPINGS = {
        # Beginn der Hörminderung
        "praelingual": 1.0,
        "prälingual": 1.0,
        "prelingual": 1.0,
        "< 1 y": 1.0,
        "perilingual": 2.0,
        "1-2 y": 2.0,
        "1-5 y": 2.0,
        "postlingual": 3.0,
        "> 20 y": 3.0,
        "10-20 y": 3.0,
        "5-10 y": 3.0,
        # Zeitpunkt
        "erworben – prälingual": 1.0,
        "erworben - prälingual": 1.0,
        "erworben - perilingual": 2.0,
        "erworben - postlingual": 3.0,
        "erworben – postlingual": 3.0,
        "angeboren": 0.0,
        "kongenital": 0.0,
        # Hearing loss severity
        "hochgradiger hv": 2.0,
        "hochgradig": 2.0,
        "taubheit (profound hl)": 3.0,
        "taubheit": 3.0,
        "profound": 3.0,
        "mittelgradig": 1.0,
        "leichtgradig": 0.5,
        "unbekannt": 0.0,
        "unbekannt/ka": 0.0,
    }

    for feature_name, aliases in diagnosis_ordinal.items():
        value = raw.get(feature_name, None)
        if value is None:
            for alias in aliases:
                if alias in raw:
                    value = raw[alias]
                    break
        if value is not None:
            # Handle pandas Series by extracting scalar value
            if hasattr(value, "iloc"):
                value = value.iloc[0] if len(value) > 0 else None
            if value is None:
                continue
            if isinstance(value, str):
                # Try to map string to numeric
                mapped = ORDINAL_MAPPINGS.get(value.lower().strip(), None)
                if mapped is not None:
                    features[feature_name] = mapped
                else:
                    # Try to parse as number, else default to 0
                    try:
                        features[feature_name] = float(value)
                    except (ValueError, TypeError):
                        features[feature_name] = 0.0
            else:
                try:
                    features[feature_name] = float(value)
                except (ValueError, TypeError):
                    features[feature_name] = 0.0

    # --- Gender (one-hot encoded) ---
    gender = str(
        raw.get("Geschlecht", raw.get("geschlecht", raw.get("gender", "w")))
    ).lower()
    if gender in ["m", "male", "männlich"]:
        features["Geschlecht_m"] = 1.0
        features["Geschlecht_w"] = 0.0
    else:
        features["Geschlecht_m"] = 0.0
        features["Geschlecht_w"] = 1.0

    # --- Imaging findings (one-hot encoded) ---
    imaging = raw.get(
        "Bildgebung, präoperativ.Befunde...",
        raw.get("bildgebung", raw.get("imaging", "Normalbefund")),
    )
    imaging_features = [
        f
        for f in EXPECTED_FEATURES
        if f.startswith("Bildgebung, präoperativ.Befunde..._")
    ]
    _set_one_hot_feature(features, imaging_features, imaging, default="Normalbefund")

    # --- Objective measurements (one-hot encoded) ---
    # NOTE: Default changed from "Nicht erhoben" to None to avoid inflating predictions
    # "Nicht erhoben" has a high positive coefficient (+4.3) which artificially raises predictions
    ll_measurement = raw.get(
        "Objektive Messungen.LL...", raw.get("ll_measurement", None)
    )
    ll_features = [
        f for f in EXPECTED_FEATURES if f.startswith("Objektive Messungen.LL..._")
    ]
    _set_one_hot_feature(features, ll_features, ll_measurement, default=None)

    # NOTE: Default changed from "Nicht erhoben" to None to avoid inflating predictions
    hz4000_measurement = raw.get(
        "Objektive Messungen.4000 Hz...", raw.get("hz4000_measurement", None)
    )
    hz4000_features = [
        f for f in EXPECTED_FEATURES if f.startswith("Objektive Messungen.4000 Hz..._")
    ]
    _set_one_hot_feature(features, hz4000_features, hz4000_measurement, default=None)

    # --- Cause/Ursache (one-hot encoded) ---
    # NOTE: Default changed from "unknown" to None to avoid negative bias
    cause = raw.get(
        "Diagnose.Höranamnese.Ursache....Ursache...",
        raw.get("ursache", raw.get("cause", None)),
    )
    cause_features = [
        f
        for f in EXPECTED_FEATURES
        if f.startswith("Diagnose.Höranamnese.Ursache....Ursache..._")
    ]
    _set_one_hot_feature(features, cause_features, cause, default=None)

    # --- Contralateral ear supply (one-hot encoded) ---
    contra = raw.get(
        "Diagnose.Höranamnese.Versorgung Gegenohr...",
        raw.get("versorgung_gegen", raw.get("contra_supply", "Keine Versorgung")),
    )
    contra_features = [
        f
        for f in EXPECTED_FEATURES
        if f.startswith("Diagnose.Höranamnese.Versorgung Gegenohr..._")
    ]
    _set_one_hot_feature(features, contra_features, contra, default="Keine Versorgung")

    # --- CI Implant type (one-hot encoded) ---
    implant = raw.get(
        "Behandlung/OP.CI Implantation", raw.get("implant_type", raw.get("ci_type", ""))
    )
    implant_features = [
        f for f in EXPECTED_FEATURES if f.startswith("Behandlung/OP.CI Implantation_")
    ]
    _set_one_hot_feature(features, implant_features, implant, default=None)

    # --- Operated ear supply (one-hot encoded) ---
    # NOTE: Default changed from "Nicht erhoben" to None to avoid bias
    op_supply = raw.get(
        "Diagnose.Höranamnese.Versorgung operiertes Ohr...",
        raw.get("versorgung_op", None),
    )
    op_supply_features = [
        f
        for f in EXPECTED_FEATURES
        if f.startswith("Diagnose.Höranamnese.Versorgung operiertes Ohr..._")
    ]
    _set_one_hot_feature(features, op_supply_features, op_supply, default=None)

    # --- Acquisition type (one-hot encoded) ---
    # NOTE: Default changed from "unknown" to None to avoid negative bias
    acquisition = raw.get(
        "Diagnose.Höranamnese.Erwerbsart...",
        raw.get("erwerbsart", raw.get("acquisition", None)),
    )
    acq_features = [
        f
        for f in EXPECTED_FEATURES
        if f.startswith("Diagnose.Höranamnese.Erwerbsart..._")
    ]
    _set_one_hot_feature(features, acq_features, acquisition, default=None)

    # --- Hearing disorder type (one-hot encoded) ---
    # NOTE: Default changed from "Cochleär" to None to avoid bias
    disorder = raw.get(
        "Diagnose.Höranamnese.Art der Hörstörung...",
        raw.get("hoerstoerung", raw.get("disorder_type", None)),
    )
    disorder_features = [
        f
        for f in EXPECTED_FEATURES
        if f.startswith("Diagnose.Höranamnese.Art der Hörstörung..._")
    ]
    _set_one_hot_feature(features, disorder_features, disorder, default=None)

    # Convert to pandas DataFrame with correct column names (required by the model)
    df = pd.DataFrame([features], columns=EXPECTED_FEATURES)
    return df


def _set_one_hot_feature(
    features: dict, feature_list: list[str], value: Any, default: str | None = None
) -> None:
    """Set the appropriate one-hot encoded feature to 1.0.

    Args:
        features: Dictionary of all features
        feature_list: List of one-hot encoded feature names for this category
        value: The value to match
        default: Default feature suffix to set if no match found
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        value = default

    if value is None:
        return

    value_str = str(value).lower().strip()

    # Try exact match first
    for feat in feature_list:
        # Extract the suffix after the underscore
        if "_" in feat:
            suffix = feat.split("_", 1)[1].lower()
            if value_str == suffix or value_str in suffix or suffix in value_str:
                features[feat] = 1.0
                return

    # If no match, try partial matching
    for feat in feature_list:
        if "_" in feat:
            suffix = feat.split("_", 1)[1].lower()
            # Check for key words
            value_words = value_str.split()
            suffix_words = suffix.split()
            if any(w in suffix_words for w in value_words):
                features[feat] = 1.0
                return

    # If still no match and default is specified, set the default
    if default:
        for feat in feature_list:
            if "_" in feat and default.lower() in feat.lower():
                features[feat] = 1.0
                return


def get_feature_names() -> list[str]:
    """Return the list of expected feature names."""
    return EXPECTED_FEATURES.copy()
