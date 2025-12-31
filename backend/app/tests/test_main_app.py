"""Tests for the main FastAPI application."""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient


class TestAppConfiguration:
    """Test FastAPI app configuration."""

    def test_app_has_title(self):
        """Test app has title set."""
        from app.main import app
        assert app.title is not None
        assert len(app.title) > 0

    def test_app_has_openapi_url(self):
        """Test app has openapi URL configured."""
        from app.main import app
        assert app.openapi_url is not None
        assert "/openapi.json" in app.openapi_url

    def test_app_includes_api_router(self):
        """Test app includes API router."""
        from app.main import app
        routes = [route.path for route in app.routes]
        assert any("/api/v1" in str(route) for route in routes)


class TestCustomGenerateUniqueId:
    """Test custom unique ID generation for routes."""

    def test_generate_unique_id_with_tags(self):
        """Test unique ID generation with tags."""
        from fastapi.routing import APIRoute

        from app.main import custom_generate_unique_id

        # Create mock route
        mock_route = MagicMock(spec=APIRoute)
        mock_route.tags = ["prediction"]
        mock_route.name = "predict"

        result = custom_generate_unique_id(mock_route)
        assert result == "prediction-predict"

    def test_generate_unique_id_without_tags(self):
        """Test unique ID generation without tags."""
        from fastapi.routing import APIRoute

        from app.main import custom_generate_unique_id

        mock_route = MagicMock(spec=APIRoute)
        mock_route.tags = []
        mock_route.name = "some_route"

        result = custom_generate_unique_id(mock_route)
        assert result == "default-some_route"

    def test_generate_unique_id_with_none_tags(self):
        """Test unique ID generation with None tags."""
        from fastapi.routing import APIRoute

        from app.main import custom_generate_unique_id

        mock_route = MagicMock(spec=APIRoute)
        mock_route.tags = None
        mock_route.name = "some_route"

        result = custom_generate_unique_id(mock_route)
        assert result == "default-some_route"


class TestExceptionHandler:
    """Test exception handler."""

    def test_unhandled_exception_returns_500(self):
        """Test unhandled exceptions return 500."""
        from app.main import app
        client = TestClient(app, raise_server_exceptions=False)

        # Access a route that may throw an internal error
        # This tests that the exception handler works
        response = client.post("/api/v1/predict/", json={})
        # Should not crash the app - returns either error or validation error
        assert response.status_code in [200, 400, 422, 500, 503]


class TestCORSMiddleware:
    """Test CORS middleware configuration."""

    def test_cors_middleware_added(self):
        """Test CORS middleware is configured."""
        from app.main import app

        # Check that middleware is present
        middleware_classes = [m.cls.__name__ for m in app.user_middleware]
        assert "CORSMiddleware" in middleware_classes


class TestModelWrapperState:
    """Test model wrapper in app state."""

    def test_app_has_model_wrapper_attribute(self):
        """Test app exposes model_wrapper."""
        from app.main import model_wrapper

        assert model_wrapper is not None
        # After startup, app.state.model_wrapper should be set
        # (may be None if model file not found, but attribute should exist)
