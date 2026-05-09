"""
Tests for conversation endpoints
"""
import pytest
from httpx import AsyncClient


async def get_auth_headers(client: AsyncClient, test_user_data):
    """Helper to get authentication headers"""
    response = await client.post("/api/auth/signup", json=test_user_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient, test_user_data):
    """Test creating a conversation"""
    headers = await get_auth_headers(client, test_user_data)
    
    response = await client.post(
        "/api/conversations/",
        json={"title": "Test Conversation"},
        headers=headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Conversation"
    assert "id" in data
    assert data["message_count"] == 0


@pytest.mark.asyncio
async def test_list_conversations(client: AsyncClient, test_user_data):
    """Test listing conversations"""
    headers = await get_auth_headers(client, test_user_data)
    
    # Create conversations
    await client.post(
        "/api/conversations/",
        json={"title": "Conversation 1"},
        headers=headers
    )
    await client.post(
        "/api/conversations/",
        json={"title": "Conversation 2"},
        headers=headers
    )
    
    # List conversations
    response = await client.get("/api/conversations/", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["conversations"]) == 2


@pytest.mark.asyncio
async def test_get_conversation(client: AsyncClient, test_user_data):
    """Test getting a specific conversation"""
    headers = await get_auth_headers(client, test_user_data)
    
    # Create conversation
    create_response = await client.post(
        "/api/conversations/",
        json={"title": "Test Conversation"},
        headers=headers
    )
    conversation_id = create_response.json()["id"]
    
    # Get conversation
    response = await client.get(
        f"/api/conversations/{conversation_id}",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conversation_id
    assert data["title"] == "Test Conversation"


@pytest.mark.asyncio
async def test_update_conversation(client: AsyncClient, test_user_data):
    """Test updating conversation title"""
    headers = await get_auth_headers(client, test_user_data)
    
    # Create conversation
    create_response = await client.post(
        "/api/conversations/",
        json={"title": "Old Title"},
        headers=headers
    )
    conversation_id = create_response.json()["id"]
    
    # Update conversation
    response = await client.put(
        f"/api/conversations/{conversation_id}",
        json={"title": "New Title"},
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_conversation(client: AsyncClient, test_user_data):
    """Test deleting a conversation"""
    headers = await get_auth_headers(client, test_user_data)
    
    # Create conversation
    create_response = await client.post(
        "/api/conversations/",
        json={"title": "To Delete"},
        headers=headers
    )
    conversation_id = create_response.json()["id"]
    
    # Delete conversation
    response = await client.delete(
        f"/api/conversations/{conversation_id}",
        headers=headers
    )
    
    assert response.status_code == 204
    
    # Verify deletion
    get_response = await client.get(
        f"/api/conversations/{conversation_id}",
        headers=headers
    )
    assert get_response.status_code == 404
