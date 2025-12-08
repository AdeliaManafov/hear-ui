-- Fix the alembic_version table to use the shortened revision ID
-- Run this SQL if your database already has the old long revision ID

-- Update any records that have the old long revision ID to the new short one
UPDATE alembic_version 
SET version_num = 'd9e8_trgm_unaccent' 
WHERE version_num = 'd9e8_add_trgm_unaccent_display_name';

-- Verify the change
SELECT version_num FROM alembic_version;
