# backend/app/api

This folder contains API-specific modules and routers for the application.

Contents & Notes:
- Individual endpoint groups are typically in separate files or subpackages
- Use existing dependencies and `deps.py` modules to inject common dependencies (DB, Auth)

Tip: Changes to API schemas may require updating the OpenAPI schema used by the frontend client.

See `backend/README.md` for local development and testing instructions.
