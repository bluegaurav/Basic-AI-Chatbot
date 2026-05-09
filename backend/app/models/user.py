"""User model"""
from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    email: Indexed(EmailStr, unique=True)  # type: ignore
    name: str
    hashed_password: str
    role_title: str = "General"
    role_description: str = "General purpose assistance"
    context: Optional[str] = ""
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
