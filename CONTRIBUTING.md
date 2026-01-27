# Contributing to HEAR-UI

Thank you for your interest in contributing to HEAR-UI! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/hear-ui.git
   cd hear-ui
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/hear-ui.git
   ```

## Development Setup

### Prerequisites

- Python 3.14+
- Node.js 20+
- Docker & Docker Compose
- Git

### Quick Start

1. **Copy environment files**:
   ```bash
   cp .env.example .env
   # ⚠️ Edit .env and set secure values for:
   #    - POSTGRES_PASSWORD
   #    - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
   ```

2. **Start development environment**:
   ```bash
   docker compose -f docker/docker-compose.yml \
     -f docker/docker-compose.override.yml \
     --env-file "$PWD/.env" up -d --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Environment Variables

The following Docker image variables must be set in `.env`:

| Variable | Required | Description |
|----------|----------|-------------|
| `DOCKER_IMAGE_BACKEND` | Yes | Backend image name (e.g., `hear-backend`) |
| `DOCKER_IMAGE_FRONTEND` | Yes | Frontend image name (e.g., `hear-frontend`) |
| `POSTGRES_PASSWORD` | Yes | Database password |
| `SECRET_KEY` | Yes | JWT signing key (min 32 chars) |
| `VITE_API_URL` | No | Frontend API URL (default: `http://localhost:8000`) |

See `.env.example` for the complete list of configuration options.

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clear, concise code
   - Add tests for new features
   - Update documentation as needed

3. **Keep your branch updated**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

## Testing

### Run All Tests

**Backend:**
```bash
cd backend
pytest app/tests/ -v
```

**Frontend:**
```bash
cd frontend
npm test                    # Unit tests
npm run test:e2e           # E2E tests with Playwright
```

### Test Coverage

Aim for >80% test coverage for new code:

```bash
# Backend
cd backend
pytest app/tests/ --cov=app --cov-report=html

# Frontend
cd frontend
npm run test:coverage
```

### CI Pipeline

All pull requests must pass:
- ✅ Linting (Ruff for Python, ESLint for TypeScript)
- ✅ Formatting (Ruff, Prettier)
- ✅ Unit tests
- ✅ Integration tests
- ✅ E2E tests

## Submitting Changes

1. **Commit your changes** with clear messages:
   ```bash
   git commit -m "feat: add patient search functionality"
   ```

   Use conventional commit format:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation changes
   - `test:` test additions/changes
   - `refactor:` code refactoring
   - `chore:` maintenance tasks

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**:
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template with:
     - Description of changes
     - Related issues
     - Testing performed
     - Screenshots (if UI changes)

## Code Style

### Python (Backend)

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use `ruff` for linting and formatting:

```bash
cd backend
ruff check app/
ruff format app/
```

### TypeScript (Frontend)

- Follow TypeScript best practices
- Use ESLint and Prettier:

```bash
cd frontend
npm run lint
npm run format
```

### Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add JSDoc/docstrings for new functions
- Update CHANGELOG.md for significant changes

## Project Structure

```
hear-ui/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core logic (ML model, SHAP)
│   │   ├── models/      # Database models
│   │   └── tests/       # Backend tests
│   └── requirements.txt
├── frontend/            # Vue.js frontend
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── routes/      # Route definitions
│   │   └── client/      # API client
│   └── tests/          # Frontend tests
├── docker/             # Docker configuration
└── docs/               # Additional documentation
```

## Questions?

- Open an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Join our discussions for questions and ideas

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
