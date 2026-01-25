#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/backend_pre_start.py

# Run migrations. If upgrade fails (e.g. because the DB already contains
# tables from a previous run), fall back to stamping the current revision
# heads so the DB is considered up-to-date. Use an explicit alembic config
# path so the behavior is deterministic in containers.
alembic -c /app/alembic.ini upgrade heads || alembic -c /app/alembic.ini stamp heads

# Create initial data in DB
if [ -f "/app/app/initial_data.py" ]; then
	python app/initial_data.py
else
	echo "Skipping initial data: /app/app/initial_data.py not found"
fi
