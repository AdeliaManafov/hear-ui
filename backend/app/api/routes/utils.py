from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["utils"])


# The test-email endpoint has been removed for the MVP. Keep health_check only.


@router.get("/health-check/")
async def health_check():
    """Return a small JSON status object for health checks."""
    return {"status": "ok"}
