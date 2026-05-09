"""Message model"""
from datetime import datetime
from enum import Enum
from beanie import Document, Indexed
from pydantic import Field


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(Document):
    conversation_id: Indexed(str)  # type: ignore
    content: str
    role: MessageRole
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "messages"
