Scripts and how to use init-dev.sh

Project scripts are organized in two places:

- Repository-level helpers: `./scripts/` (e.g. `build.sh`, `deploy.sh`, `init-dev.sh`). These are generic helpers for the whole project.
- Backend-specific helpers: `./backend/scripts/` (format, lint, test, prestart). These are intended to be run from the `backend/` directory or inside the backend container.

init-dev.sh

- A safe helper to bootstrap a local `.env` from `.env.example`. It will not overwrite an existing `.env`.
- Usage (from repository root):

```bash
chmod +x scripts/init-dev.sh
./scripts/init-dev.sh
```

If you prefer to run the backend locally without installing Python dependencies on your machine, use the Docker Compose setup described in the repository root `development.md` — it runs the backend in a container with all dependencies available.
