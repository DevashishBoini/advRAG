"""
Tests for API endpoints.
"""

import pytest


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_api_status(client):
    """Test the API status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"
