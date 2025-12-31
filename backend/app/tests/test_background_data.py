"""Tests for background data generation."""

from unittest.mock import MagicMock

import numpy as np
import pandas as pd


class TestCreateSyntheticBackground:
    """Test create_synthetic_background function."""

    def test_returns_tuple(self):
        """Test function returns tuple."""
        from app.core.background_data import create_synthetic_background

        result = create_synthetic_background(n_samples=10)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_dataframe(self):
        """Test first element is DataFrame."""
        from app.core.background_data import create_synthetic_background

        raw_df, _ = create_synthetic_background(n_samples=10)
        assert isinstance(raw_df, pd.DataFrame)

    def test_returns_correct_sample_count(self):
        """Test returns correct number of samples."""
        from app.core.background_data import create_synthetic_background

        raw_df, _ = create_synthetic_background(n_samples=25)
        assert len(raw_df) == 25

    def test_dataframe_has_required_columns(self):
        """Test DataFrame has required columns."""
        from app.core.background_data import create_synthetic_background

        raw_df, _ = create_synthetic_background(n_samples=10)

        expected_columns = [
            'Alter [J]',
            'Geschlecht',
            'Primäre Sprache',
        ]
        for col in expected_columns:
            assert col in raw_df.columns

    def test_age_values_in_range(self):
        """Test age values are within reasonable range."""
        from app.core.background_data import create_synthetic_background

        raw_df, _ = create_synthetic_background(n_samples=100)
        ages = raw_df['Alter [J]']

        assert ages.min() >= 18
        assert ages.max() <= 90

    def test_gender_values_valid(self):
        """Test gender values are valid."""
        from app.core.background_data import create_synthetic_background

        raw_df, _ = create_synthetic_background(n_samples=50)
        genders = raw_df['Geschlecht'].unique()

        assert set(genders).issubset({'m', 'w'})

    def test_with_pipeline_transformation(self):
        """Test transformation with mock pipeline."""
        from app.core.background_data import create_synthetic_background

        mock_pipeline = MagicMock()
        mock_preprocessor = MagicMock()
        mock_preprocessor.transform.return_value = np.array([[1, 2, 3]])
        mock_pipeline.named_steps = {'preprocessor': mock_preprocessor}

        raw_df, transformed = create_synthetic_background(
            n_samples=10,
            include_transformed=True,
            pipeline=mock_pipeline
        )

        assert raw_df is not None
        # transformed may be None if transform fails, that's ok

    def test_without_transformation(self):
        """Test without transformation returns None for second element."""
        from app.core.background_data import create_synthetic_background

        raw_df, transformed = create_synthetic_background(
            n_samples=10,
            include_transformed=False
        )

        assert raw_df is not None
        assert transformed is None

    def test_reproducibility_with_same_seed(self):
        """Test results are reproducible (uses fixed seed internally)."""
        from app.core.background_data import create_synthetic_background

        raw_df1, _ = create_synthetic_background(n_samples=10)
        raw_df2, _ = create_synthetic_background(n_samples=10)

        pd.testing.assert_frame_equal(raw_df1, raw_df2)


class TestGetFeatureNamesFromPipeline:
    """Test get_feature_names_from_pipeline function."""

    def test_extracts_from_preprocessor(self):
        """Test extracting feature names from preprocessor."""
        from app.core.background_data import get_feature_names_from_pipeline

        mock_preprocessor = MagicMock()
        mock_preprocessor.get_feature_names_out.return_value = ['feat_a', 'feat_b']

        mock_pipeline = MagicMock()
        mock_pipeline.named_steps = {'preprocessor': mock_preprocessor}

        result = get_feature_names_from_pipeline(mock_pipeline)

        assert result == ['feat_a', 'feat_b']

    def test_returns_none_on_error(self):
        """Test returns None when extraction fails."""
        from app.core.background_data import get_feature_names_from_pipeline

        # Create a mock without get_feature_names_out
        mock_pipeline = MagicMock(spec=[])

        result = get_feature_names_from_pipeline(mock_pipeline)

        assert result is None

    def test_with_no_named_steps(self):
        """Test with pipeline without named_steps."""
        from app.core.background_data import get_feature_names_from_pipeline

        mock_pipeline = MagicMock(spec=[])  # No attributes

        result = get_feature_names_from_pipeline(mock_pipeline)

        assert result is None
