"""
Tests for versioned model card management system.
"""

import pytest

from app.models.model_card.versioned_model_card import ModelCardManager


class TestModelCardManager:
    """Test suite for ModelCardManager."""

    def test_get_active_version(self):
        """Should read active version from file."""
        version = ModelCardManager.get_active_version()
        assert version == "v3_randomforest_2026-02-17"

    def test_load_active_card(self):
        """Should load the currently active model card."""
        card = ModelCardManager.load_card()

        assert card["version"] == "v3.0"
        assert card["status"] == "active"
        assert card["model_type"] == "RandomForestClassifier"
        assert card["deployment_date"] == "2026-02-17"
        assert card["retired_date"] is None

    def test_load_specific_version(self):
        """Should load a specific model card version."""
        card = ModelCardManager.load_card("v2_randomforest_2026-01-20")

        assert card["version"] == "v2.0"
        assert card["status"] == "retired"
        assert card["retired_date"] == "2026-02-17"

    def test_load_old_version(self):
        """Should load oldest (v1) model card."""
        card = ModelCardManager.load_card("v1_logreg_2025-11-15")

        assert card["version"] == "v1.0"
        assert card["model_type"] == "LogisticRegression"
        assert card["status"] == "retired"

    def test_list_all_versions(self):
        """Should list all available versions sorted by date."""
        versions = ModelCardManager.list_all_versions()

        assert len(versions) >= 3

        # Check newest first
        assert versions[0]["version"] == "v3.0"
        assert versions[0]["status"] == "active"

        # Check fields present
        for v in versions:
            assert "version" in v
            assert "file" in v
            assert "deployment_date" in v
            assert "status" in v
            assert "model_type" in v
            assert "accuracy" in v

    def test_metrics_in_loaded_card(self):
        """Should have metrics in loaded cards."""
        card = ModelCardManager.load_card()

        assert "metrics" in card
        assert "test_set" in card["metrics"]

        metrics = card["metrics"]["test_set"]
        assert "accuracy" in metrics
        assert "f1_score" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "roc_auc" in metrics

        # Check v3 accuracy is better than v2
        v3_acc = metrics["accuracy"]
        v2_card = ModelCardManager.load_card("v2_randomforest_2026-01-20")
        v2_acc = v2_card["metrics"]["test_set"]["accuracy"]
        assert v3_acc > v2_acc  # v3 should be better

    def test_changelog_present(self):
        """Should have changelog in all cards."""
        for version_file in [
            "v1_logreg_2025-11-15",
            "v2_randomforest_2026-01-20",
            "v3_randomforest_2026-02-17",
        ]:
            card = ModelCardManager.load_card(version_file)
            assert "changelog" in card
            assert len(card["changelog"]) > 0

    def test_retired_versions_have_retired_date(self):
        """Retired versions should have retired_date set."""
        v1 = ModelCardManager.load_card("v1_logreg_2025-11-15")
        v2 = ModelCardManager.load_card("v2_randomforest_2026-01-20")

        assert v1["retired_date"] == "2026-01-20"
        assert v2["retired_date"] == "2026-02-17"

    def test_nonexistent_version_raises_error(self):
        """Should raise FileNotFoundError for non-existent version."""
        with pytest.raises(FileNotFoundError):
            ModelCardManager.load_card("v999_fake_2099-01-01")

    def test_version_progression(self):
        """Should show clear progression in metrics from v1 → v2 → v3."""
        v1 = ModelCardManager.load_card("v1_logreg_2025-11-15")
        v2 = ModelCardManager.load_card("v2_randomforest_2026-01-20")
        v3 = ModelCardManager.load_card("v3_randomforest_2026-02-17")

        v1_acc = v1["metrics"]["test_set"]["accuracy"]
        v2_acc = v2["metrics"]["test_set"]["accuracy"]
        v3_acc = v3["metrics"]["test_set"]["accuracy"]

        # Each version should improve
        assert v2_acc > v1_acc  # 0.74 > 0.68
        assert v3_acc > v2_acc  # 0.76 > 0.74

    def test_ethical_considerations_present(self):
        """All cards should have ethical considerations."""
        for version in ModelCardManager.list_all_versions():
            card = ModelCardManager.load_card(version["file"])
            assert "ethical_considerations" in card
            assert "fairness" in card["ethical_considerations"]
            assert "privacy" in card["ethical_considerations"]
            assert "transparency" in card["ethical_considerations"]
