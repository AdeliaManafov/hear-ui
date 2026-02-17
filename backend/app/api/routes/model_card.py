from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.models.model_card.model_card import load_model_card

router = APIRouter(prefix="/model-card", tags=["Model Card"])


def _render_model_card_markdown() -> str:
    """Build a Markdown string from the loaded ModelCard."""
    card = load_model_card()

    return f"""\
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


@router.get("", response_class=PlainTextResponse)
def get_model_card():
    """Return the model card as plain Markdown (consumed by the frontend)."""
    return _render_model_card_markdown()


@router.get("/markdown")
def get_model_card_markdown():
    """Return the model card wrapped in a JSON object (legacy)."""
    return {"markdown": _render_model_card_markdown()}
