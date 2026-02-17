"""Ensure patient table exists and add display_name column

Revision ID: b7d2adddisplayname
Revises: 4152189463d6
Create Date: 2025-12-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from alembic import context

# revision identifiers, used by Alembic.
revision = 'b7d2adddisplayname'
down_revision = '4152189463d6'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    
    # In offline mode (--sql), we can't inspect the database
    # So we just emit the safest SQL: try to add column if not exists
    if context.is_offline_mode():
        # For offline mode, we use batch operations which handle if-not-exists
        with op.batch_alter_table('patient', schema=None) as batch_op:
            batch_op.add_column(sa.Column('display_name', sa.String(), nullable=True))
            batch_op.create_index(batch_op.f('ix_patient_display_name'), ['display_name'], unique=False)
        return
    
    # Online mode: inspect and decide
    inspector = inspect(conn)

    # Create patient table if it does not exist (fresh DBs)
    if "patient" not in inspector.get_table_names():
        op.create_table(
            "patient",
            sa.Column("id", sa.Uuid(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("input_features", sa.JSON(), nullable=True),
            sa.Column("display_name", sa.String(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_patient_display_name"), "patient", ["display_name"], unique=False)
        return

    columns = {c["name"] for c in inspector.get_columns("patient")}
    if "display_name" not in columns:
        op.add_column("patient", sa.Column("display_name", sa.String(), nullable=True))

    indexes = {idx["name"] for idx in inspector.get_indexes("patient")}
    if "ix_patient_display_name" not in indexes:
        op.create_index(op.f("ix_patient_display_name"), "patient", ["display_name"], unique=False)


def downgrade():
    # In offline mode, just emit the drop statements
    if context.is_offline_mode():
        with op.batch_alter_table('patient', schema=None) as batch_op:
            batch_op.drop_index(batch_op.f('ix_patient_display_name'))
            batch_op.drop_column('display_name')
        return
    
    # Online mode: inspect and decide
    inspector = inspect(op.get_bind())
    indexes = {idx["name"] for idx in inspector.get_indexes("patient")}
    if "ix_patient_display_name" in indexes:
        op.drop_index(op.f("ix_patient_display_name"), table_name="patient")

    columns = {c["name"] for c in inspector.get_columns("patient")}
    if "display_name" in columns:
        op.drop_column("patient", "display_name")
