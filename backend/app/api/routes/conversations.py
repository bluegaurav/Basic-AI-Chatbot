"""Conversation routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_active_user
from app.crud.conversation import *
from app.models.user import User
from app.schemas.conversation import *

router = APIRouter()


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create(
    conversation_in: ConversationCreate,
    current_user: User = Depends(get_current_active_user)
):
    conv = await create_conversation(str(current_user.id), conversation_in)
    return ConversationResponse(
        id=str(conv.id),
        title=conv.title,
        message_count=conv.message_count,
        created_at=conv.created_at,
        updated_at=conv.updated_at
    )


@router.get("/", response_model=ConversationList)
async def list_all(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    convs = await get_user_conversations(str(current_user.id), skip, limit)
    total = await count_user_conversations(str(current_user.id))
    return ConversationList(
        conversations=[
            ConversationResponse(
                id=str(c.id),
                title=c.title,
                message_count=c.message_count,
                created_at=c.created_at,
                updated_at=c.updated_at
            )
            for c in convs
        ],
        total=total
    )


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_one(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    conv = await get_conversation(conversation_id, str(current_user.id))
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    return ConversationResponse(
        id=str(conv.id),
        title=conv.title,
        message_count=conv.message_count,
        created_at=conv.created_at,
        updated_at=conv.updated_at
    )


@router.put("/{conversation_id}", response_model=ConversationResponse)
async def update_one(
    conversation_id: str,
    update_data: ConversationUpdate,
    current_user: User = Depends(get_current_active_user)
):
    conv = await get_conversation(conversation_id, str(current_user.id))
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    
    updated = await update_conversation(conv, update_data)
    return ConversationResponse(
        id=str(updated.id),
        title=updated.title,
        message_count=updated.message_count,
        created_at=updated.created_at,
        updated_at=updated.updated_at
    )


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    if not await delete_conversation(conversation_id, str(current_user.id)):
        raise HTTPException(status_code=404, detail="Not found")


@router.delete("/{conversation_id}/messages", status_code=status.HTTP_204_NO_CONTENT)
async def clear(
    conversation_id: str,
    current_user: User = Depends(get_current_active_user)
):
    if not await clear_messages(conversation_id, str(current_user.id)):
        raise HTTPException(status_code=404, detail="Not found")
