"""Message CRUD operations"""
from typing import List
from datetime import datetime
from app.models.message import Message, MessageRole
from app.models.conversation import Conversation


async def get_messages(conversation_id: str, skip: int = 0, limit: int = 1000) -> List[Message]:
    return await Message.find(
        Message.conversation_id == conversation_id
    ).sort(Message.created_at).skip(skip).limit(limit).to_list()


async def count_messages(conversation_id: str) -> int:
    return await Message.find(Message.conversation_id == conversation_id).count()


async def create_message(conversation_id: str, content: str, role: MessageRole) -> Message:
    message = Message(
        conversation_id=conversation_id,
        content=content,
        role=role
    )
    await message.insert()
    return message


async def create_user_message(conversation_id: str, content: str) -> Message:
    return await create_message(conversation_id, content, MessageRole.USER)


async def create_assistant_message(conversation_id: str, content: str) -> Message:
    return await create_message(conversation_id, content, MessageRole.ASSISTANT)


async def auto_title(conversation: Conversation, first_message: str) -> None:
    if conversation.message_count <= 1:
        title = first_message[:50] + ("..." if len(first_message) > 50 else "")
        conversation.title = title
        conversation.updated_at = datetime.utcnow()
        await conversation.save()
