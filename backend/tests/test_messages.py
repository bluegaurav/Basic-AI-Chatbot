"""
Tests for message and chat endpoints
"""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


async def get_auth_headers(client: AsyncClient, test_user_data):
    """Helper to get authentication headers"""
    response = await client.post("/api/auth/signup", json=test_user_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def create_conversation(client: AsyncClient, headers):
    """Helper to create a conversation"""
    response = await client.post(
        "/api/conversations/",
        json={"title": "Test Conversation"},
        headers=headers
    )
    return response.json()["id"]


@pytest.mark.asyncio
async def test_send_chat_message(client: AsyncClient, test_user_data):
    """Test sending a chat message"""
    headers = await get_auth_headers(client, test_user_data)
    conversation_id = await create_conversation(client, headers)
    
    # Mock OpenRouter response
    with patch('app.services.openrouter.openrouter_service.generate_response') as mock_ai:
        mock_ai.return_value = "This is a test AI response"
        
        response = await client.post(
            f"/api/conversations/{conversation_id}/chat",
            json={"message": "Hello, AI!"},
            headers=headers
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "user_message" in data
    assert "assistant_message" in data
    assert data["user_message"]["content"] == "Hello, AI!"
    assert data["assistant_message"]["content"] == "This is a test AI response"


@pytest.mark.asyncio
async def test_get_messages(client: AsyncClient, test_user_data):
    """Test getting conversation messages"""
    headers = await get_auth_headers(client, test_user_data)
    conversation_id = await create_conversation(client, headers)
    
    # Send a message
    with patch('app.services.openrouter.openrouter_service.generate_response') as mock_ai:
        mock_ai.return_value = "AI response"
        
        await client.post(
            f"/api/conversations/{conversation_id}/chat",
            json={"message": "Test message"},
            headers=headers
        )
    
    # Get messages
    response = await client.get(
        f"/api/conversations/{conversation_id}/messages",
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # User + Assistant messages
    assert len(data["messages"]) == 2


@pytest.mark.asyncio
async def test_conversation_title_auto_generation(client: AsyncClient, test_user_data):
    """Test that conversation title is auto-generated from first message"""
    headers = await get_auth_headers(client, test_user_data)
    conversation_id = await create_conversation(client, headers)
    
    # Send first message
    with patch('app.services.openrouter.openrouter_service.generate_response') as mock_ai:
        mock_ai.return_value = "AI response"
        
        await client.post(
            f"/api/conversations/{conversation_id}/chat",
            json={"message": "This is my first question about Python"},
            headers=headers
        )
    
    # Get conversation and check title
    response = await client.get(
        f"/api/conversations/{conversation_id}",
        headers=headers
    )
    
    data = response.json()
    assert "This is my first question about Python" in data["title"]


@pytest.mark.asyncio
async def test_clear_conversation_messages(client: AsyncClient, test_user_data):
    """Test clearing all messages from a conversation"""
    headers = await get_auth_headers(client, test_user_data)
    conversation_id = await create_conversation(client, headers)
    
    # Send messages
    with patch('app.services.openrouter.openrouter_service.generate_response') as mock_ai:
        mock_ai.return_value = "AI response"
        
        await client.post(
            f"/api/conversations/{conversation_id}/chat",
            json={"message": "Message 1"},
            headers=headers
        )
        await client.post(
            f"/api/conversations/{conversation_id}/chat",
            json={"message": "Message 2"},
            headers=headers
        )
    
    # Clear messages
    response = await client.delete(
        f"/api/conversations/{conversation_id}/messages",
        headers=headers
    )
    
    assert response.status_code == 204
    
    # Verify messages are cleared
    get_response = await client.get(
        f"/api/conversations/{conversation_id}/messages",
        headers=headers
    )
    assert get_response.json()["total"] == 0
