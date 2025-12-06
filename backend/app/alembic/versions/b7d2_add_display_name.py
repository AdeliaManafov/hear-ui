"""Ensure patient table exists and add display_name column

Revision ID: b7d2adddisplayname
Revises: 4152189463d6
Create Date: 2025-12-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'b7d2adddisplayname'
down_revision = '4152189463d6'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
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
    inspector = inspect(op.get_bind())
    indexes = {idx["name"] for idx in inspector.get_indexes("patient")}
    if "ix_patient_display_name" in indexes:
        op.drop_index(op.f("ix_patient_display_name"), table_name="patient")

    columns = {c["name"] for c in inspector.get_columns("patient")}
    if "display_name" in columns:
        op.drop_column("patient", "display_name")
