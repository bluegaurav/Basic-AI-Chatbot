"""
Tests for user endpoints
"""
import pytest
from httpx import AsyncClient


async def get_auth_headers(client: AsyncClient, test_user_data):
    """Helper to get authentication headers"""
    response = await client.post("/api/auth/signup", json=test_user_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user_data):
    """Test getting current user information"""
    headers = await get_auth_headers(client, test_user_data)
    
    response = await client.get("/api/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]
    assert data["role"]["title"] == "General"


@pytest.mark.asyncio
async def test_update_user_settings(client: AsyncClient, test_user_data):
    """Test updating user settings"""
    headers = await get_auth_headers(client, test_user_data)
    
    # Update user
    response = await client.put(
        "/api/users/me",
        json={
            "name": "Updated Name",
            "role_title": "Developer",
            "role_description": "Programming and technical help",
            "context": "Working on a Python FastAPI project"
        },
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["role"]["title"] == "Developer"
    assert data["context"] == "Working on a Python FastAPI project"


@pytest.mark.asyncio
async def test_update_user_partial(client: AsyncClient, test_user_data):
    """Test partial update of user settings"""
    headers = await get_auth_headers(client, test_user_data)
    
    # Update only role
    response = await client.put(
        "/api/users/me",
        json={
            "role_title": "Student",
            "role_description": "Learning and educational assistance"
        },
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user_data["name"]  # Unchanged
    assert data["role"]["title"] == "Student"  # Changed
