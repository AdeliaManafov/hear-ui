"""add pg_trgm + unaccent and trigram index for patient.display_name

Revision ID: d9e8_trgm_unaccent
Revises: b7d2adddisplayname
Create Date: 2025-12-01 00:55:00.000000
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd9e8_trgm_unaccent'
down_revision = 'b7d2adddisplayname'
branch_labels = None
depends_on = None


def upgrade():
    # Create pg_trgm and unaccent extensions if not present and a GIN trigram index
    # Note: creating extensions requires superuser privileges on the Postgres server.
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    op.execute('CREATE EXTENSION IF NOT EXISTS unaccent;')
    op.execute("CREATE INDEX IF NOT EXISTS idx_patient_display_name_trgm ON patient USING gin (display_name gin_trgm_ops);")


def downgrade():
    op.execute('DROP INDEX IF EXISTS idx_patient_display_name_trgm;')
    # Do not drop extensions automatically (other DB objects may rely on them)
