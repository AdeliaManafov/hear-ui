"""Pytest configuration and fixtures for backend tests."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.db import engine as production_engine
from app.core.config import settings


@pytest.fixture(name="session", scope="function")
def session_fixture():
    """Provide a clean database session for each test.
    
    Uses in-memory SQLite for fast, isolated testing.
    """
    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    # Clean up
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="test_db", scope="function")
def test_db_fixture():
    """Initialize test database schema.
    
    This fixture creates all tables before tests and drops them after.
    Use this when you need to test against a real postgres instance.
    """
    # Only create schema if TESTING is set
    if getattr(settings, "TESTING", False):
        SQLModel.metadata.create_all(production_engine)
        yield
        SQLModel.metadata.drop_all(production_engine)
    else:
        # For CI/local testing with real DB
        SQLModel.metadata.create_all(production_engine)
        yield
        # Don't drop in case there's existing data


@pytest.fixture(name="client")
def client_fixture():
    """Provide a test client for API testing."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    with TestClient(app) as client:
        yield client


# Sample patient data fixtures for reuse across tests
@pytest.fixture(name="sample_patient")
def sample_patient_fixture():
    """Provide sample patient data for testing."""
    return {
        "Alter [J]": 50,
        "Geschlecht": "w",
        "Primäre Sprache": "Deutsch",
        "Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...": "postlingual",
        "Diagnose.Höranamnese.Ursache....Ursache...": "Unbekannt",
        "Symptome präoperativ.Tinnitus...": "nein",
        "Behandlung/OP.CI Implantation": "Cochlear",
    }


@pytest.fixture(name="sample_feedback")
def sample_feedback_fixture(sample_patient):
    """Provide sample feedback data for testing."""
    return {
        "input_features": sample_patient,
        "prediction": 0.75,
        "explanation": {
            "age": 0.15,
            "hearing_loss_duration": 0.20,
            "implant_type": 0.25,
        },
        "accepted": True,
        "comment": "Test feedback",
    }


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch):
    """Set up test environment variables for all tests."""
    # Ensure we're in test mode
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("TESTING", "true")
    
    # Use test database or in-memory
    if not settings.SQLALCHEMY_DATABASE_URI:
        monkeypatch.setenv("POSTGRES_SERVER", "localhost")
        monkeypatch.setenv("POSTGRES_USER", "postgres")
        monkeypatch.setenv("POSTGRES_PASSWORD", "postgres")
        monkeypatch.setenv("POSTGRES_DB", "test_db")
    
    # Disable external services in tests
    monkeypatch.setenv("SENTRY_DSN", "")
    
    yield


# Mock for SHAP-heavy tests
@pytest.fixture(name="mock_shap")
def mock_shap_fixture():
    """Mock SHAP library to avoid slow computations in tests."""
    from unittest.mock import MagicMock, patch
    
    with patch("app.core.shap_explainer.shap") as mock_shap:
        # Create a mock explainer
        mock_explainer = MagicMock()
        mock_explainer.shap_values.return_value = [[0.1, 0.2, 0.3]]
        mock_explainer.expected_value = 0.5
        
        # Mock SHAP module functions
        mock_shap.Explainer.return_value = mock_explainer
        mock_shap.LinearExplainer.return_value = mock_explainer
        mock_shap.TreeExplainer.return_value = mock_explainer
        mock_shap.KernelExplainer.return_value = mock_explainer
        
        yield mock_shap


# Performance testing helpers
@pytest.fixture
def benchmark_prediction(client):
    """Fixture to benchmark prediction endpoint performance."""
    import time
    
    def _benchmark(payload, n_iterations=10):
        times = []
        for _ in range(n_iterations):
            start = time.time()
            client.post("/api/v1/predict/", json=payload)
            times.append(time.time() - start)
        
        return {
            "avg": sum(times) / len(times),
            "min": min(times),
            "max": max(times),
            "iterations": n_iterations,
        }
    
    return _benchmark
