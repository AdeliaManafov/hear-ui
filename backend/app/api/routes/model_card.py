from fastapi import APIRouter
from app.models.model_card.model_card import load_model_card

router = APIRouter(prefix="/model-card", tags=["Model Card"])


@router.get("/markdown")
def get_model_card_markdown():
    card = load_model_card()

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

## Features
{chr(10).join(f"- **{f.name}**" for f in card.features)}

"""

    return {"markdown": md}
