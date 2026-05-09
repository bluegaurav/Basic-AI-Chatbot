"""Conversation model"""
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field


class Conversation(Document):
    user_id: Indexed(str)  # type: ignore
    title: str = "New Conversation"
    message_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "conversations"
