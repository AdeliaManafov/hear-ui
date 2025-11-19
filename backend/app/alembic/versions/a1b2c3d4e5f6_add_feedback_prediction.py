"""add feedback and prediction tables

Revision ID: a1b2c3d4e5f6
Revises: 4152189463d6
Create Date: 2025-11-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '4152189463d6'
branch_labels = None
depends_on = None


def upgrade():
    # Feedback table
    op.create_table(
        'feedback',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('input_features', sa.JSON(), nullable=True),
        sa.Column('prediction', sa.Float(), nullable=True),
        sa.Column('explanation', sa.JSON(), nullable=True),
        sa.Column('accepted', sa.Boolean(), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('user_email', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Prediction table
    op.create_table(
        'prediction',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('input_features', sa.JSON(), nullable=True),
        sa.Column('prediction', sa.Float(), nullable=True),
        sa.Column('explanation', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('prediction')
    op.drop_table('feedback')
