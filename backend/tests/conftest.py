"""
Pytest configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    Provide a test client for API testing.
    
    Yields:
        TestClient: FastAPI test client
    """
    return TestClient(app)


@pytest.fixture
def app_instance():
    """
    Provide the FastAPI application instance.
    
    Yields:
        FastAPI: Application instance
    """
    return app
