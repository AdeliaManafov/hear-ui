"""Add updated_at to patient and rating to feedback

Revision ID: e1f2a3b4c5d6
Revises: d9e8_trgm_unaccent
Create Date: 2026-01-23

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "e1f2a3b4c5d6"
down_revision = "d9e8_trgm_unaccent"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add updated_at column to patient table
    op.add_column(
        "patient",
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    # Add rating column to feedback table
    op.add_column(
        "feedback",
        sa.Column("rating", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("feedback", "rating")
    op.drop_column("patient", "updated_at")
