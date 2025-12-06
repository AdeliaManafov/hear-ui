"""Tests for preprocessor module (68-feature HEAR CI model)."""

import numpy as np
import pandas as pd
import pytest
from app.core.preprocessor import preprocess_patient_data, get_feature_names, EXPECTED_FEATURES


class TestPreprocessPatientData:
    """Test patient data preprocessing for the 68-feature LogisticRegression model."""

    def test_basic_preprocessing(self):
        """Test basic patient data preprocessing returns correct shape."""
        raw = {
            "age": 45,
            "geschlecht": "w",
            "tinnitus": "ja"
        }
        result = preprocess_patient_data(raw)
        
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (1, 68)
        
        # Check age is in the correct column
        assert result["Alter [J]"].iloc[0] == 45.0

    def test_returns_correct_columns(self):
        """Test that function returns DataFrame with correct column names."""
        result = preprocess_patient_data({})
        assert list(result.columns) == EXPECTED_FEATURES

    def test_gender_male_encoding(self):
        """Test male gender encoding."""
        raw = {"geschlecht": "m"}
        result = preprocess_patient_data(raw)
        
        assert result["Geschlecht_m"].iloc[0] == 1.0
        assert result["Geschlecht_w"].iloc[0] == 0.0

    def test_gender_female_encoding(self):
        """Test female gender encoding."""
        raw = {"geschlecht": "w"}
        result = preprocess_patient_data(raw)
        
        assert result["Geschlecht_m"].iloc[0] == 0.0
        assert result["Geschlecht_w"].iloc[0] == 1.0

    def test_tinnitus_symptom(self):
        """Test tinnitus symptom encoding."""
        raw = {"tinnitus": "ja"}
        result = preprocess_patient_data(raw)
        
        assert result["Symptome präoperativ.Tinnitus..."].iloc[0] == 1.0

    def test_tinnitus_symptom_no(self):
        """Test tinnitus symptom when no."""
        raw = {"tinnitus": "nein"}
        result = preprocess_patient_data(raw)
        
        assert result["Symptome präoperativ.Tinnitus..."].iloc[0] == 0.0

    def test_implant_type_cochlear(self):
        """Test Cochlear implant type encoding."""
        raw = {"implant_type": "Cochlear CI632"}
        result = preprocess_patient_data(raw)
        
        # Check that one of the Cochlear implant features is set
        implant_cols = [c for c in result.columns if "Cochlear" in c]
        has_cochlear = any(result[c].iloc[0] == 1.0 for c in implant_cols)
        assert has_cochlear

    def test_missing_age_uses_default(self):
        """Test missing age uses default of 50."""
        raw = {"geschlecht": "w"}
        result = preprocess_patient_data(raw)
        assert result["Alter [J]"].iloc[0] == 50.0

    def test_cause_hoersturz(self):
        """Test Hörsturz cause encoding."""
        raw = {"ursache": "Hörsturz"}
        result = preprocess_patient_data(raw)
        
        assert result["Diagnose.Höranamnese.Ursache....Ursache..._Hörsturz"].iloc[0] == 1.0

    def test_empty_dict_uses_defaults(self):
        """Test empty dictionary uses sensible defaults."""
        raw = {}
        result = preprocess_patient_data(raw)
        
        assert result.shape == (1, 68)
        # Default age should be 50
        assert result["Alter [J]"].iloc[0] == 50.0
        # Default gender should be female
        assert result["Geschlecht_w"].iloc[0] == 1.0
        # Default imaging should be Normalbefund
        assert result["Bildgebung, präoperativ.Befunde..._Normalbefund"].iloc[0] == 1.0

    def test_case_insensitive_gender(self):
        """Test gender is case insensitive."""
        raw = {"geschlecht": "M"}
        result = preprocess_patient_data(raw)
        assert result["Geschlecht_m"].iloc[0] == 1.0

    def test_string_numeric_values(self):
        """Test that string numeric values are converted."""
        raw = {"age": "45"}
        result = preprocess_patient_data(raw)
        assert result["Alter [J]"].iloc[0] == 45.0

    def test_float_age(self):
        """Test that float age is handled correctly."""
        raw = {"age": 45.7}
        result = preprocess_patient_data(raw)
        assert result["Alter [J]"].iloc[0] == 45.7


class TestGetFeatureNames:
    """Test get_feature_names function."""

    def test_returns_list(self):
        """Test that get_feature_names returns a list."""
        result = get_feature_names()
        assert isinstance(result, list)

    def test_returns_68_features(self):
        """Test that 68 features are returned."""
        result = get_feature_names()
        assert len(result) == 68

    def test_returns_copy(self):
        """Test that modifications don't affect the original."""
        result = get_feature_names()
        result.append("extra")
        assert len(EXPECTED_FEATURES) == 68


class TestCSVCompatibility:
    """Test preprocessing compatibility with CSV data format from Dummy Data_Cochlear Implant.csv."""

    def test_csv_row_preprocessing(self):
        """Test preprocessing a row similar to CSV format."""
        # Data format matching CSV columns
        csv_row = {
            "ID": 1,
            "Geschlecht": "w",
            "Alter [J]": 30,
            "Primäre Sprache": "Deutsch",  # Ignored - not in model
            "Weitere Sprachen": "",  # Ignored - not in model
            "Seiten": "L",
            "Symptome präoperativ.Geschmack...": "Subjektiv normal",
            "Symptome präoperativ.Tinnitus...": "Vorhanden",
            "Symptome präoperativ.Schwindel...": "Kein",
            "Symptome präoperativ.Otorrhoe...": "Keine",
            "Symptome präoperativ.Kopfschmerzen...": "Keine",
            "Bildgebung, präoperativ.Typ...": "MRT, CT, konventionell",  # Ignored
            "Bildgebung, präoperativ.Befunde...": "Sonstige",
            "Objektive Messungen.OAE (TEOAE/DPOAE)...": "Nicht erhoben",  # Ignored
            "Objektive Messungen.LL...": "Keine Reizantwort",
            "Objektive Messungen.4000 Hz...": "Keine Reizantwort",
            "Diagnose.Höranamnese.Hörminderung operiertes Ohr...": "Hochgradiger HV",
            "Diagnose.Höranamnese.Versorgung operiertes Ohr...": "Keine Versorgung",
            "Diagnose.Höranamnese.Zeitpunkt des Hörverlusts (OP-Ohr)...": "Erworben – prälingual",
            "Diagnose.Höranamnese.Erwerbsart...": "Progredient",
            "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "< 1 y",
            "Diagnose.Höranamnese.Hochgradige Hörminderung oder Taubheit (OP-Ohr)...": "> 20 y",
            "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
            "Diagnose.Höranamnese.Art der Hörstörung...": "Cochleär",
            "Diagnose.Höranamnese.Hörminderung Gegenohr...": "Hochgradiger HV",
            "Diagnose.Höranamnese.Versorgung Gegenohr...": "Hörgerät",
            "Behandlung/OP.CI Implantation": "Behandlung/OP.CI Implantation.Cochlear... Nucleus Profile CI532 (Slim Modiolar)",
            "outcome_measurments.post24.measure.": 40,  # Ignored - target variable
            "outcome_measurments.post12.measure.": 80,  # Ignored - target variable
            "outcome_measurments.pre.measure.": 10,
            "abstand": 828,
        }
        
        result = preprocess_patient_data(csv_row)
        
        # Verify shape
        assert result.shape == (1, 68)
        
        # Verify key values
        assert result["Alter [J]"].iloc[0] == 30.0
        assert result["Geschlecht_w"].iloc[0] == 1.0
        assert result["Symptome präoperativ.Tinnitus..."].iloc[0] == 1.0
        assert result["abstand"].iloc[0] == 828.0
        assert result["outcome_measurments.pre.measure."].iloc[0] == 10.0

    def test_ignored_columns_dont_affect_output(self):
        """Test that columns not in model don't affect preprocessing."""
        base_data = {"age": 45, "gender": "m"}
        
        # Add columns that should be ignored
        with_ignored = base_data.copy()
        with_ignored.update({
            "Primäre Sprache": "Arabisch",
            "Weitere Sprachen": "Deutsch",
            "Deutsch Sprachbarriere": "ja",
            "non-verbal": "mit Gebärden",
            "Eltern m. Schwerhörigkeit": "Vater SH",
            "Geschwister m. SH": "Mit HG",
            "Objektive Messungen.OAE (TEOAE/DPOAE)...": "Nicht erhoben",
            "Bildgebung, präoperativ.Typ...": "MRT",
        })
        
        result_base = preprocess_patient_data(base_data)
        result_with_ignored = preprocess_patient_data(with_ignored)
        
        # Results should be identical since ignored columns don't matter
        pd.testing.assert_frame_equal(result_base, result_with_ignored)

    def test_outcome_measures_not_used_as_features(self):
        """Test that post-operative outcome measures are not used as features."""
        # The post12 and post24 measures are TARGET variables, not features
        data = {
            "age": 50,
            "outcome_measurments.post24.measure.": 100,
            "outcome_measurments.post12.measure.": 90,
        }
        
        result = preprocess_patient_data(data)
        
        # These columns should NOT be in the output
        assert "outcome_measurments.post24.measure." not in result.columns
        assert "outcome_measurments.post12.measure." not in result.columns
        
        # But pre-measure should be there
        assert "outcome_measurments.pre.measure." in result.columns

    def test_german_symptom_values(self):
        """Test German symptom value encoding (Vorhanden/Kein)."""
        data = {
            "Symptome präoperativ.Tinnitus...": "Vorhanden",
            "Symptome präoperativ.Schwindel...": "Kein",
            "Symptome präoperativ.Otorrhoe...": "Keine",
        }
        
        result = preprocess_patient_data(data)
        
        assert result["Symptome präoperativ.Tinnitus..."].iloc[0] == 1.0
        assert result["Symptome präoperativ.Schwindel..."].iloc[0] == 0.0
        assert result["Symptome präoperativ.Otorrhoe..."].iloc[0] == 0.0

    def test_seiten_encoding(self):
        """Test Seiten (L/R) encoding."""
        data_left = {"Seiten": "L"}
        data_right = {"Seiten": "R"}
        
        result_left = preprocess_patient_data(data_left)
        result_right = preprocess_patient_data(data_right)
        
        assert result_left["Seiten"].iloc[0] == 1.0  # L = 1
        assert result_right["Seiten"].iloc[0] == 2.0  # R = 2
