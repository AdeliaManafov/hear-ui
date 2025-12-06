# frontend/src/client

Generated OpenAPI client for accessing the backend API.

Overview
- This folder contains the TypeScript/JavaScript client code that is generated from the project's OpenAPI schema. The generated client is used by the frontend to interact with the backend API in a type-safe way.

When to regenerate
- Regenerate the client whenever the backend OpenAPI schema (openapi.json) changes.
- From the project root run: `./scripts/generate-client.sh`.
- From the `frontend` directory you can run: `npm run generate-client` (if configured in `package.json`).

Important guidelines
- Do not edit generated files directly. Generated code will be overwritten the next time the client is generated.
- If you need custom behavior, wrap the generated client in a small hand-written adapter in another folder (for example, `src/client-adapter/`) and keep changes outside the generated source.
- Document any manual edits clearly and consider improving the generation template instead.

Usage
- Import the generated client modules from this folder in your frontend code. Typical usage looks like:
	- `import { SomeApi } from 'src/client'` (adjust the import path to match your project aliases).
- The client includes models, request/response types, and API methods derived from the OpenAPI spec.

Troubleshooting
- If generation fails, check that you have a valid OpenAPI JSON file and the generator tooling installed (see `frontend/README.md` and project scripts).
- Ensure Node and package manager (npm/pnpm) versions match the frontend requirements.

Notes
- The generator configuration and script are in the repository root; consult `./scripts/generate-client.sh` for exact behavior and any custom arguments.

