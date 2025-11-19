from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.models import Message
from app.utils import send_email

router = APIRouter(prefix="/utils", tags=["utils"])


# The test-email endpoint has been removed for the MVP. Keep health_check only.


@router.get("/health-check/")
async def health_check():
    """Return a small JSON status object for health checks."""
    return {"status": "ok"}
