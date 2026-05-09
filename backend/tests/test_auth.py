"""
Tests for authentication endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_signup(client: AsyncClient, test_user_data):
    """Test user signup"""
    response = await client.post("/api/auth/signup", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "access_token" in data
    assert data["user"]["email"] == test_user_data["email"]
    assert data["user"]["name"] == test_user_data["name"]
    assert "id" in data["user"]


@pytest.mark.asyncio
async def test_signup_duplicate_email(client: AsyncClient, test_user_data):
    """Test signup with duplicate email"""
    # First signup
    await client.post("/api/auth/signup", json=test_user_data)
    
    # Second signup with same email
    response = await client.post("/api/auth/signup", json=test_user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user_data):
    """Test user login"""
    # First create user
    await client.post("/api/auth/signup", json=test_user_data)
    
    # Then login
    response = await client.post(
        "/api/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "user" in data
    assert data["user"]["email"] == test_user_data["email"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, test_user_data):
    """Test login with invalid credentials"""
    await client.post("/api/auth/signup", json=test_user_data)
    
    response = await client.post(
        "/api/auth/login",
        data={
            "username": test_user_data["email"],
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user_data):
    """Test getting current user info"""
    # Signup
    signup_response = await client.post("/api/auth/signup", json=test_user_data)
    token = signup_response.json()["access_token"]
    
    # Get current user
    response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing protected route without token"""
    response = await client.get("/api/users/me")
    
    assert response.status_code == 401
