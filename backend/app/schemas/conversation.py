"""
Pydantic schemas for Conversation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ConversationBase(BaseModel):
    """Base conversation schema"""
    title: Optional[str] = "New Conversation"


class ConversationCreate(ConversationBase):
    """Schema for creating a conversation"""
    pass


class ConversationUpdate(BaseModel):
    """Schema for updating a conversation"""
    title: Optional[str] = None


class ConversationInDB(ConversationBase):
    """Conversation schema with all database fields"""
    id: str
    user_id: str
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Conversation response schema"""
    id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    """List of conversations"""
    conversations: list[ConversationResponse]
    total: int
