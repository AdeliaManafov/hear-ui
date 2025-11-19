#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/backend_pre_start.py

# Run migrations. If upgrade fails (e.g. because the DB already contains
# tables from a previous run), fall back to stamping the current revision
# heads so the DB is considered up-to-date.
alembic upgrade heads || alembic stamp heads

# Create initial data in DB
python app/initial_data.py
