"""
Pydantic schemas for User
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRole(BaseModel):
    """User role schema"""
    title: str
    description: str


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user"""
    name: Optional[str] = None
    role_title: Optional[str] = None
    role_description: Optional[str] = None
    context: Optional[str] = None


class UserInDB(UserBase):
    """User schema with all database fields"""
    id: str
    role_title: str
    role_description: str
    context: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response schema (without sensitive data)"""
    id: str
    email: str
    name: str
    role: UserRole
    context: Optional[str] = None
    created_at: datetime
    
    @classmethod
    def from_db_user(cls, user: UserInDB) -> "UserResponse":
        """Convert UserInDB to UserResponse"""
        return cls(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=UserRole(
                title=user.role_title,
                description=user.role_description
            ),
            context=user.context,
            created_at=user.created_at
        )
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
