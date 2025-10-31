"""
Test suite for chat session API endpoints.
"""

import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.main import app


@pytest.fixture
async def client():
    """Create async test client."""
    from fastapi.testclient import TestClient
    # Note: For proper async testing, install httpx and use:
    # async with AsyncClient(base_url="http://test") as ac:
    #     yield ac
    # For now, using TestClient for basic testing
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "app" in data


@pytest.mark.asyncio
async def test_create_session(client):
    """Test creating a new chat session."""
    payload = {
        "user_id": "test_user_123",
        "title": "Test Session",
        "metadata": {"test": True}
    }
    
    response = await client.post("/api/v1/sessions", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert data["user_id"] == "test_user_123"
    assert data["title"] == "Test Session"
    assert data["status"] == "active"
    assert data["is_active"] is True
    assert data["message_count"] == 0
    assert data["message"] == "hello! upload docs for me to Index"


@pytest.mark.asyncio
async def test_create_session_minimal(client):
    """Test creating session with minimal data."""
    payload = {}
    
    response = await client.post("/api/v1/sessions", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data
    assert data["title"] == "New Chat Session"
    assert data["message"] == "hello! upload docs for me to Index"


@pytest.mark.asyncio
async def test_get_session(client):
    """Test getting a session by ID."""
    # First create a session
    create_payload = {"title": "Get Test Session"}
    create_response = await client.post("/api/v1/sessions", json=create_payload)
    assert create_response.status_code == 201
    session_id = create_response.json()["id"]
    
    # Now get it
    response = await client.get(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == session_id
    assert data["title"] == "Get Test Session"


@pytest.mark.asyncio
async def test_get_nonexistent_session(client):
    """Test getting a session that doesn't exist."""
    fake_id = str(uuid4())
    response = await client.get(f"/api/v1/sessions/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_session(client):
    """Test updating a session."""
    # Create a session
    create_payload = {"title": "Original Title"}
    create_response = await client.post("/api/v1/sessions", json=create_payload)
    session_id = create_response.json()["id"]
    
    # Update it
    update_payload = {"title": "Updated Title", "status": "completed"}
    response = await client.patch(f"/api/v1/sessions/{session_id}", json=update_payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "completed"


@pytest.mark.asyncio
async def test_delete_session(client):
    """Test deleting a session."""
    # Create a session
    create_response = await client.post("/api/v1/sessions", json={})
    session_id = create_response.json()["id"]
    
    # Delete it
    response = await client.delete(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 204
    
    # Verify it's marked as deleted
    get_response = await client.get(f"/api/v1/sessions/{session_id}")
    if get_response.status_code == 200:
        data = get_response.json()
        assert data["is_active"] is False
        assert data["status"] == "archived"


@pytest.mark.asyncio
async def test_api_health_endpoint(client):
    """Test detailed API health endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code in [200, 503]  # 503 if DB not connected
    
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "timestamp" in data
