 # Project Documentation (Index)

This directory contains project-level documentation for the HEAR project. Its
purpose is to provide a clear entry point that groups the most important
documents and points to archived/obsolete files.

Important active documents

- `development.md` — Instructions for local development (Docker Compose, local
	servers, logs, `.env`, pre-commit hooks).
- `deployment.md` — Production deployment guidance: Traefik, DNS, remote
	servers and CI/CD notes.
- `ci-cd.md` — Suggested CI/CD setup and example GitHub Actions workflows
	(lint, tests, build & push).
- `SECURITY.md` — Security policy and vulnerability reporting instructions.
- `assignment-status.md` — Project assignment, current status, TODO list and
	recommended next steps (maintained continuously).

Area-specific READMEs

- `../backend/README.md` — Backend-specific guidance (migrations, tests,
	development workflows).
- `../backend/README-DEPS.md` — Dependency management guidance for the
	Python backend.
- `../backend/SCRIPTS.md` — Short descriptions of backend helper scripts.
- `../frontend/README.md` — Frontend development instructions (Vite, npm,
	Playwright, generating API client).

Archive (duplicated or long templates)

Files that are older, highly detailed, or template-oriented are kept in
`docs/archived/` for reference but are not actively maintained. Examples:

- `sprint_plan_and_tech.md` — earlier sprint plans and technical notes.
- `TODO.md` — historical TODO (merged into `assignment-status.md`).
- `release-notes.md` — detailed changelog templates.

Update procedure

- When you edit a document, briefly update this index to reflect the change.
	For major updates, add a short summary to `assignment-status.md` describing
	the change and rationale.
- If you are unsure whether a document is still active, move it to
	`docs/archived/` rather than deleting it — this preserves history and makes
	it easy to restore if needed.

---

Wenn du möchtest, kann ich jetzt bei Bedarf die archivierten Dateien per Pull‑Request oder Commit löschen bzw. weitere Dateien konsolidieren (z. B. TODO → assignment‑status zusammenführen). Sag kurz, ob das Vorgehen so passt.
