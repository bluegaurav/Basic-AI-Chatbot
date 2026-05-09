"""Conversation CRUD operations"""
from typing import Optional, List
from datetime import datetime
from beanie import PydanticObjectId
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationUpdate


async def get_conversation(conversation_id: str, user_id: str) -> Optional[Conversation]:
    return await Conversation.find_one(
        Conversation.id == PydanticObjectId(conversation_id),
        Conversation.user_id == user_id
    )


async def get_user_conversations(user_id: str, skip: int = 0, limit: int = 100) -> List[Conversation]:
    return await Conversation.find(
        Conversation.user_id == user_id
    ).sort(-Conversation.updated_at).skip(skip).limit(limit).to_list()


async def count_user_conversations(user_id: str) -> int:
    return await Conversation.find(Conversation.user_id == user_id).count()


async def create_conversation(user_id: str, conversation_in: ConversationCreate) -> Conversation:
    conversation = Conversation(
        user_id=user_id,
        title=conversation_in.title or "New Conversation"
    )
    await conversation.insert()
    return conversation


async def update_conversation(conversation: Conversation, update: ConversationUpdate) -> Conversation:
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(conversation, field, value)
    conversation.updated_at = datetime.utcnow()
    await conversation.save()
    return conversation


async def update_message_count(conversation: Conversation) -> Conversation:
    count = await Message.find(Message.conversation_id == str(conversation.id)).count()
    conversation.message_count = count
    conversation.updated_at = datetime.utcnow()
    await conversation.save()
    return conversation


async def delete_conversation(conversation_id: str, user_id: str) -> bool:
    conversation = await get_conversation(conversation_id, user_id)
    if not conversation:
        return False
    await Message.find(Message.conversation_id == conversation_id).delete()
    await conversation.delete()
    return True


async def clear_messages(conversation_id: str, user_id: str) -> bool:
    conversation = await get_conversation(conversation_id, user_id)
    if not conversation:
        return False
    await Message.find(Message.conversation_id == conversation_id).delete()
    conversation.message_count = 0
    conversation.updated_at = datetime.utcnow()
    await conversation.save()
    return True
