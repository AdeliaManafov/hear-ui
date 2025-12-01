-- SQL script: clean_json_keys.sql
-- Purpose: remove leading U+FEFF (BOM) from JSON keys in the `patient.input_features` column
-- Usage (from project root):
--   docker compose exec -T -u postgres db psql -d hear_db -f scripts/clean_json_keys.sql

BEGIN;

-- Update only rows where a key begins with a BOM (U+FEFF)
UPDATE patient
SET input_features = (
  SELECT (jsonb_object_agg(regexp_replace(k, U&'^\FEFF', '', 'g'), v))
  FROM jsonb_each(input_features::jsonb) AS t(k,v)
)
WHERE EXISTS (
  SELECT 1 FROM jsonb_each(input_features::jsonb) AS t(k,v)
  WHERE k LIKE U&'\FEFF%'
);

COMMIT;

-- End of script
