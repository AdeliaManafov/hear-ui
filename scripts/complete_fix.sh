#!/bin/bash
set -e

cd /Users/adeliamanafov/hearUI_project/hear-ui

echo "Deleting old migration file..."
rm -f backend/app/alembic/versions/d9e8_add_trgm_unaccent_display_name.py

echo "Staging deletion..."
git add backend/app/alembic/versions/d9e8_add_trgm_unaccent_display_name.py

echo "Committing deletion..."
git commit -m "chore: remove old migration file with long version name"

echo "Checking if database needs migration fix..."
cd backend

# Check if database exists and has the old version
if docker ps | grep -q hear-ui-db; then
    echo "Database container is running, checking if fix is needed..."
    
    NEEDS_FIX=$(docker exec hear-ui-db-1 psql -U postgres -d hear_db -t -c "SELECT COUNT(*) FROM alembic_version WHERE version_num = 'd9e8_add_trgm_unaccent_display_name';" 2>/dev/null || echo "0")
    
    if [ "$NEEDS_FIX" -gt 0 ]; then
        echo "Database needs fix, applying SQL script..."
        docker exec -i hear-ui-db-1 psql -U postgres -d hear_db < scripts/fix_alembic_version.sql
        echo "✅ Database fixed!"
    else
        echo "✅ Database doesn't need fix (no old version found)"
    fi
else
    echo "⚠️  Database container not running. If you have data, run:"
    echo "   docker compose up -d db"
    echo "   docker exec -i hear-ui-db-1 psql -U postgres -d hear_db < backend/scripts/fix_alembic_version.sql"
fi

cd ..

echo "Pushing changes..."
git push

echo ""
echo "✅ All done! Check CI at: https://github.com/AdeliaManafov/hear-ui/actions"
