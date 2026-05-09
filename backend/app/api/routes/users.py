"""User routes"""
from fastapi import APIRouter, Depends
from app.api.deps import get_current_active_user
from app.crud.user import update_user
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role={"title": current_user.role_title, "description": current_user.role_description},
        context=current_user.context,
        created_at=current_user.created_at
    )


@router.put("/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    updated = await update_user(current_user, user_update)
    return UserResponse(
        id=str(updated.id),
        email=updated.email,
        name=updated.name,
        role={"title": updated.role_title, "description": updated.role_description},
        context=updated.context,
        created_at=updated.created_at
    )
