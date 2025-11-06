from __future__ import with_statement
import sys
import asyncio
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# ------------------------------------------------------------
# Pfadkonfiguration – sorgt dafür, dass "app" importiert werden kann
# ------------------------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
from app.db.base import SQLModel  # Enthält alle Models (z. B. User, Item usw.)

# ------------------------------------------------------------
# Alembic Config & Logging
# ------------------------------------------------------------
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

# ------------------------------------------------------------
# 🔧 DB-Verbindungs-URL (direkt festgelegt, damit Alembic funktioniert)
# ------------------------------------------------------------
def get_url():
    return "postgresql+asyncpg://postgres:postgres@localhost/hear_db"

# ------------------------------------------------------------
# Offline-Modus (keine echte Verbindung, z. B. beim Skripterzeugen)
# ------------------------------------------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ------------------------------------------------------------
# Online-Modus (echte DB-Verbindung, async)
# ------------------------------------------------------------
async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(get_url(), poolclass=pool.NullPool)

    async with connectable.begin() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata,
                compare_type=True,
                compare_server_default=True,
            )
        )

        await connection.run_sync(lambda conn: context.run_migrations())

    await connectable.dispose()
        
# ------------------------------------------------------------
# Hauptlogik – entscheidet zwischen offline und online
# ------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

