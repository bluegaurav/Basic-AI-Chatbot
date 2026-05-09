"""User CRUD operations"""
from typing import Optional
from beanie import PydanticObjectId
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


async def get_user(user_id: str) -> Optional[User]:
    return await User.get(PydanticObjectId(user_id))


async def get_user_by_email(email: str) -> Optional[User]:
    return await User.find_one(User.email == email)


async def create_user(user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password)
    )
    await user.insert()
    return user


async def update_user(user: User, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    await user.save()
    return user


async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
