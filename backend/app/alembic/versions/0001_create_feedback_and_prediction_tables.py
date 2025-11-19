"""No-op migration to unify alembic heads

This migration previously duplicated the feedback/prediction table
creation that already exists in the `a1b2c3d4e5f6` migration. To avoid
multiple-heads conflicts and duplicate-table errors during CI/dev
startup we convert this file into a no-op and attach it after the
existing `a1b2c3d4e5f6` migration.

Revision ID: 0001
Revises: a1b2c3d4e5f6
Create Date: 2025-11-17 00:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Intentionally empty: schema changes were consolidated in
    # `a1b2c3d4e5f6_add_feedback_prediction.py`.
    pass


def downgrade():
    pass
