"""add display_name to patient

Revision ID: b7d2_add_display_name
Revises: 4152189463d6
Create Date: 2025-12-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b7d2_add_display_name'
down_revision = '4152189463d6'
branch_labels = None
depends_on = None


def upgrade():
    # add nullable display_name column
    op.add_column('patient', sa.Column('display_name', sa.String(), nullable=True))
    # create a simple index for faster prefix/substring searches
    op.create_index(op.f('ix_patient_display_name'), 'patient', ['display_name'], unique=False)
    # Optionally create pg_trgm index for fuzzy search; leave commented for safety
    # op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    # op.execute("CREATE INDEX IF NOT EXISTS idx_patient_display_name_trgm ON patient USING gin (display_name gin_trgm_ops);")


def downgrade():
    op.drop_index(op.f('ix_patient_display_name'), table_name='patient')
    op.drop_column('patient', 'display_name')
