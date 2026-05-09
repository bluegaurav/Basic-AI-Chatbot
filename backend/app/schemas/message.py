"""
Pydantic schemas for Message
"""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """Base message schema"""
    content: str = Field(..., min_length=1)
    role: Literal["user", "assistant"]


class MessageCreate(BaseModel):
    """Schema for creating a message (user sends)"""
    content: str = Field(..., min_length=1)


class MessageInDB(MessageBase):
    """Message schema with all database fields"""
    id: str
    conversation_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Message response schema"""
    id: str
    content: str
    role: str
    timestamp: datetime
    
    @classmethod
    def from_db_message(cls, message: MessageInDB) -> "MessageResponse":
        """Convert MessageInDB to MessageResponse"""
        return cls(
            id=str(message.id),
            content=message.content,
            role=message.role,
            timestamp=message.created_at
        )
    
    class Config:
        from_attributes = True


class MessageList(BaseModel):
    """List of messages"""
    messages: list[MessageResponse]
    total: int


class ChatRequest(BaseModel):
    """Request to send a chat message"""
    message: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    user_message: MessageResponse
    assistant_message: MessageResponse
