from sqlmodel import SQLModel
from app.models.user import User
from app.models.item import Item
# Ensure these models are imported so Alembic's target_metadata
# includes them for autogeneration and migrations.
from app.models.feedback import Feedback
from app.models.prediction import Prediction
