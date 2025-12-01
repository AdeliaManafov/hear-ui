# backend/app/tests

Tests for the backend.

Recommended structure:
- `conftest.py` for shared test fixtures
- `test_*.py` files for unit and integration tests

Running tests:
- Locally: `bash ./scripts/test.sh` from the `backend/` directory
- In CI: Pytest workflow is configured (see GitHub Actions in project root)

Current status:
- 164 tests passing ✅
- 2 tests skipped (matplotlib not available, batch endpoint format update)
- 82% code coverage

Tip: For integration tests requiring DB or external services, use the Docker Compose test environment.
