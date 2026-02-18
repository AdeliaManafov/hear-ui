from fastapi import APIRouter
from app.models.model_card.model_card import load_model_card
import logging

router = APIRouter(prefix="/model-card", tags=["Model Card"])
logger = logging.getLogger(__name__)


def fmt(x):
    return x if x is not None else "N/A"


@router.get("/markdown")
def get_model_card_markdown():
    try:
        card = load_model_card()
    except Exception as e:
        logger.error("Error loading model card: %s", e)
        return {"markdown": "<p>Error loading model card.</p>"}

    # Gruppiere Features
    feature_groups = {
        "Basic Patient Data": [
            f for f in card.features
            if any(keyword in f.name.lower() for keyword in ["pid", "alter", "seiten", "geschlecht"])
        ],
        "Pre-operative Symptoms": [
            f for f in card.features
            if "symptome präoperativ" in f.name.lower()
        ],
        "Diagnostic Features": [
            f for f in card.features
            if "diagnose.höranamnese" in f.name.lower() and "versorgung" not in f.name.lower()
        ],
        "Measurements": [
            f for f in card.features
            if any(keyword in f.name.lower() for keyword in ["measure", "abstand", "messungen"])
        ],
        "Imaging Findings": [
            f for f in card.features
            if "bildgebung" in f.name.lower()
        ],
        "Treatment and Implants": [
            f for f in card.features
            if "behandlung/op.ci implantation" in f.name.lower()
        ],
        "Device Care": [
            f for f in card.features
            if "versorgung" in f.name.lower()
        ]
    }

    # Features Markdown
    features_md = ""
    for group_name, features in feature_groups.items():
        if features:
            features_md += f"\n### {group_name}\n"
            features_md += "\n".join(f"- {f.name}" for f in features) + "\n"

    # ⭐ Metrics Markdown (JETZT RICHTIG EINGERÜCKT)
    metrics_md = ""
    if card.metrics:
        metrics_lines = []

        if card.metrics.accuracy is not None:
            metrics_lines.append(f"- Accuracy: {card.metrics.accuracy}")

        if card.metrics.f1_score is not None:
            metrics_lines.append(f"- F1 Score: {card.metrics.f1_score}")

        if card.metrics.precision is not None:
            metrics_lines.append(f"- Precision: {card.metrics.precision}")

        if card.metrics.recall is not None:
            metrics_lines.append(f"- Recall: {card.metrics.recall}")

        if card.metrics.roc_auc is not None:
            metrics_lines.append(f"- ROC AUC: {card.metrics.roc_auc}")

        if metrics_lines:
            metrics_md += "## Model Metrics\n" + "\n".join(metrics_lines)

    # Markdown Gesamt
    md = f"""
# {card.name}

**Version:** {card.version}
**Model type:** {card.model_type}
**Last updated:** {card.last_updated}

---

## Intended use
{chr(10).join(f"- {x}" for x in card.intended_use)}

## Not intended for
{chr(10).join(f"- {x}" for x in card.not_intended_for)}

## Limitations
{chr(10).join(f"- {x}" for x in card.limitations)}

## Recommendations
{chr(10).join(f"- {x}" for x in card.recommendations)}

{metrics_md}

## Features
{features_md}
"""

    return {"markdown": md}
