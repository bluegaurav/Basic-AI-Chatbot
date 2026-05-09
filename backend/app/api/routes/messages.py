"""Message routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_current_active_user
from app.crud.conversation import get_conversation, update_message_count
from app.crud.message import *
from app.models.user import User
from app.schemas.message import *
from app.services.openrouter import openrouter_service

router = APIRouter()


@router.get("/{conversation_id}/messages", response_model=MessageList)
async def list_messages(
    conversation_id: str,
    skip: int = 0,
    limit: int = 1000,
    current_user: User = Depends(get_current_active_user)
):
    if not await get_conversation(conversation_id, str(current_user.id)):
        raise HTTPException(status_code=404, detail="Not found")
    
    msgs = await get_messages(conversation_id, skip, limit)
    total = await count_messages(conversation_id)
    
    return MessageList(
        messages=[
            MessageResponse(
                id=str(m.id),
                content=m.content,
                role=m.role.value,
                timestamp=m.created_at
            )
            for m in msgs
        ],
        total=total
    )


@router.post("/{conversation_id}/chat", response_model=ChatResponse)
async def chat(
    conversation_id: str,
    chat_req: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    conv = await get_conversation(conversation_id, str(current_user.id))
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    
    try:
        # Create user message
        user_msg = await create_user_message(conversation_id, chat_req.message)
        
        # Get history
        history = await get_messages(conversation_id)
        history_data = [
            {"role": m.role.value, "content": m.content}
            for m in history[:-1]
        ]
        
        # Generate AI response
        ai_response = await openrouter_service.generate_response(
            user_message=chat_req.message,
            conversation_history=history_data,
            role_title=current_user.role_title,
            role_description=current_user.role_description,
            context=current_user.context
        )
        
        # Create assistant message
        ai_msg = await create_assistant_message(conversation_id, ai_response)
        
        # Update count
        await update_message_count(conv)
        
        # Auto-title
        if conv.message_count == 2:
            await auto_title(conv, chat_req.message)
        
        return ChatResponse(
            user_message=MessageResponse(
                id=str(user_msg.id),
                content=user_msg.content,
                role=user_msg.role.value,
                timestamp=user_msg.created_at
            ),
            assistant_message=MessageResponse(
                id=str(ai_msg.id),
                content=ai_msg.content,
                role=ai_msg.role.value,
                timestamp=ai_msg.created_at
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
