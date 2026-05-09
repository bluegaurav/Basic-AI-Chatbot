"""MongoDB connection"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message


async def connect_db():
    """Connect to MongoDB"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=[User, Conversation, Message]
    )
    print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")


async def close_db():
    """Close MongoDB connection"""
    print("✅ Closed MongoDB connection")
