#! /usr/bin/env bash

set -e
set -x

# Purpose:
#  - Generate the frontend API client from the backend OpenAPI specification.
#  - This script runs the backend app to produce `openapi.json`, moves it
#    into the frontend folder and runs the frontend client generator.
#
# Requirements:
#  - A working Python environment (backend) so the backend app can produce
#    its OpenAPI spec (the script imports `app.main` to get `openapi()`).
#  - Node/npm in `frontend/` to run the client generator.
#
# When to use:
#  - Use this when the backend API changes and you need to regenerate the
#    Typescript/JS client used by the frontend. Not required for normal
#    runtime operation of the app (only for development/update workflows).

cd backend
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
cd ..
mv openapi.json frontend/
cd frontend
npm run generate-client
npx biome format --write ./src/client
