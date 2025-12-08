#!/bin/bash
# Delete old migration file and stage everything

cd /Users/adeliamanafov/hearUI_project/hear-ui

# Remove the old migration file
git rm backend/app/alembic/versions/d9e8_add_trgm_unaccent_display_name.py

# Add all other changes
git add -A

# Show status
git status
