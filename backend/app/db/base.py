# Ensure models are imported so Alembic's target_metadata includes them.
# Ensure these models are imported so Alembic's target_metadata
# includes them for autogeneration and migrations.

from sqlmodel import SQLModel  # noqa: F401

from app.models.feedback import Feedback  # noqa: F401
from app.models.item import Item  # noqa: F401
from app.models.prediction import Prediction  # noqa: F401
from app.models.user import User  # noqa: F401
