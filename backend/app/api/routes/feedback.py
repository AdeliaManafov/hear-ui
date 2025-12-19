import logging

from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.deps import SessionDep
from app.models import Feedback, FeedbackCreate

router = APIRouter(prefix="/feedback", tags=["feedback"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[Feedback])
def list_feedbacks(session: SessionDep, limit: int = 100, offset: int = 0):
    """List all feedbacks with pagination."""
    return crud.list_feedback(session=session, limit=limit, offset=offset)


@router.post("/", response_model=Feedback, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback_in: FeedbackCreate, session: SessionDep):
    """Create feedback entry in the database. Authentication is disabled in demo mode,
    but current_user is provided for compatibility and auditing later.
    """
    try:
        db_obj = crud.create_feedback(session=session, feedback_in=feedback_in)
        return db_obj
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Failed to create feedback")
        # Keep returning a 500 to the client, but log the full traceback server-side
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


@router.get("/{feedback_id}", response_model=Feedback)
def read_feedback(feedback_id: str, session: SessionDep):
    fb = crud.get_feedback(session=session, feedback_id=feedback_id)
    if not fb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Feedback not found")
    return fb
