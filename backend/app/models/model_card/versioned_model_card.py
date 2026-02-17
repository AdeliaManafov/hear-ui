"""
Model Card Version Management System

Manages multiple versioned model cards with deployment tracking.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ModelCardManager:
    """Manages multiple versioned model cards with deployment history."""

    CARD_DIR = Path(__file__).parent.parent.parent / "config" / "model_cards"
    ACTIVE_VERSION_FILE = CARD_DIR / "active_version.txt"

    @classmethod
    def get_active_version(cls) -> str:
        """
        Read active version identifier from file.

        Returns:
            Version identifier (e.g., "v3_randomforest_2026-02-17")
        """
        if cls.ACTIVE_VERSION_FILE.exists():
            version = cls.ACTIVE_VERSION_FILE.read_text().strip()
            logger.info(f"Active model version: {version}")
            return version

        # Fallback: find most recent card
        cards = sorted(cls.CARD_DIR.glob("v*.json"), reverse=True)
        if cards:
            version = cards[0].stem  # filename without extension
            logger.warning(
                f"active_version.txt not found, using most recent: {version}"
            )
            return version

        raise FileNotFoundError(
            f"No model cards found in {cls.CARD_DIR} "
            "and active_version.txt does not exist"
        )

    @classmethod
    def set_active_version(cls, version: str) -> None:
        """
        Update the active model version.

        Args:
            version: Version identifier (e.g., "v3_randomforest_2026-02-17")

        Raises:
            FileNotFoundError: If the version file doesn't exist
        """
        card_path = cls.CARD_DIR / f"{version}.json"
        if not card_path.exists():
            raise FileNotFoundError(f"Cannot activate non-existent version: {version}")

        cls.CARD_DIR.mkdir(parents=True, exist_ok=True)
        cls.ACTIVE_VERSION_FILE.write_text(version)
        logger.info(f"✅ Active model version set to: {version}")

    @classmethod
    def load_card(cls, version: str | None = None) -> dict[str, Any]:
        """
        Load a specific model card version or the active one.

        Args:
            version: Version identifier. If None, loads active version.

        Returns:
            Model card data as dictionary

        Raises:
            FileNotFoundError: If the requested version doesn't exist
        """
        if version is None:
            version = cls.get_active_version()

        card_path = cls.CARD_DIR / f"{version}.json"

        if not card_path.exists():
            raise FileNotFoundError(f"Model card not found: {card_path}")

        with card_path.open("r", encoding="utf-8") as f:
            card = json.load(f)
            logger.info(
                f"Loaded model card: {card.get('version', 'unknown')} "
                f"({card.get('model_type', 'unknown')})"
            )
            return card

    @classmethod
    def list_all_versions(cls) -> list[dict[str, Any]]:
        """
        List all available model cards with metadata.

        Returns:
            List of version metadata dicts, sorted by deployment date (newest first)
        """
        if not cls.CARD_DIR.exists():
            logger.warning(f"Model card directory does not exist: {cls.CARD_DIR}")
            return []

        versions = []
        for card_file in cls.CARD_DIR.glob("v*.json"):
            try:
                with card_file.open("r", encoding="utf-8") as f:
                    card = json.load(f)
                    versions.append(
                        {
                            "version": card["version"],
                            "file": card_file.stem,
                            "deployment_date": card["deployment_date"],
                            "retired_date": card.get("retired_date"),
                            "status": card["status"],
                            "model_type": card["model_type"],
                            "accuracy": card.get("metrics", {})
                            .get("test_set", {})
                            .get("accuracy"),
                        }
                    )
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error loading {card_file}: {e}")
                continue

        # Sort by deployment date (newest first)
        versions.sort(key=lambda v: v["deployment_date"], reverse=True)
        logger.info(f"Found {len(versions)} model card versions")
        return versions

    @classmethod
    def retire_version(cls, version: str, reason: str = "") -> None:
        """
        Mark a model version as retired.

        Args:
            version: Version identifier to retire
            reason: Optional reason for retirement (logged in changelog)
        """
        card = cls.load_card(version)
        card["status"] = "retired"
        card["retired_date"] = datetime.now().strftime("%Y-%m-%d")

        if reason:
            original_changelog = card.get("changelog", "")
            card["changelog"] = (
                f"{original_changelog}\n\n**Retired {card['retired_date']}:** {reason}"
            )

        card_path = cls.CARD_DIR / f"{version}.json"
        with card_path.open("w", encoding="utf-8") as f:
            json.dump(card, f, indent=2, ensure_ascii=False)

        logger.info(f"🔒 Model version {version} retired. Reason: {reason or 'N/A'}")

    @classmethod
    def create_new_version(
        cls,
        version_id: str,
        model_type: str,
        metrics: dict[str, float],
        changelog: str,
        **kwargs: Any,
    ) -> str:
        """
        Create a new model card version.

        Args:
            version_id: Version identifier (e.g., "v4_randomforest_2026-03-01")
            model_type: Type of ML model (e.g., "RandomForestClassifier")
            metrics: Performance metrics dict (accuracy, f1, etc.)
            changelog: Description of what changed
            **kwargs: Additional fields (training details, limitations, etc.)

        Returns:
            Path to created JSON file
        """
        card_path = cls.CARD_DIR / f"{version_id}.json"

        if card_path.exists():
            raise FileExistsError(
                f"Version {version_id} already exists. "
                "Use a different version identifier."
            )

        card = {
            "name": "HEAR CI Prediction Model",
            "version": kwargs.get("version", version_id.split("_")[0]),
            "model_type": model_type,
            "deployment_date": datetime.now().strftime("%Y-%m-%d"),
            "retired_date": None,
            "status": "testing",  # Start as testing, not active
            "training": kwargs.get("training", {}),
            "metrics": {"test_set": metrics},
            "intended_use": kwargs.get("intended_use", []),
            "not_intended_for": kwargs.get("not_intended_for", []),
            "limitations": kwargs.get("limitations", []),
            "recommendations": kwargs.get("recommendations", []),
            "changelog": changelog,
        }

        cls.CARD_DIR.mkdir(parents=True, exist_ok=True)
        with card_path.open("w", encoding="utf-8") as f:
            json.dump(card, f, indent=2, ensure_ascii=False)

        logger.info(f"Created new model card: {version_id}")
        return str(card_path)
