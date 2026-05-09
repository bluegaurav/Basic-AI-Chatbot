"""API router"""
from fastapi import APIRouter
from app.api.routes import auth, users, conversations, messages

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(messages.router, prefix="/conversations", tags=["Messages"])
