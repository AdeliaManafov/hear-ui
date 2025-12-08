#!/usr/bin/env python3
"""Quick check if database exists and needs migration fix"""
import sys
try:
    import psycopg2
    from app.core.config import settings
    
    # Extract connection params from settings
    db_url = str(settings.SQLALCHEMY_DATABASE_URI)
    if 'postgresql' in db_url:
        # Try to connect
        try:
            conn = psycopg2.connect(
                host=settings.POSTGRES_SERVER,
                port=settings.POSTGRES_PORT,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                database=settings.POSTGRES_DB
            )
            cursor = conn.cursor()
            
            # Check if alembic_version table exists and has the old version
            cursor.execute("""
                SELECT version_num FROM alembic_version 
                WHERE version_num = 'd9e8_add_trgm_unaccent_display_name'
            """)
            result = cursor.fetchone()
            
            if result:
                print("NEEDS_FIX")
                print(f"Found old version: {result[0]}")
            else:
                print("NO_FIX_NEEDED")
                
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"DB_NOT_READY: {e}")
    else:
        print("NO_DB_CONFIGURED")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(0)
