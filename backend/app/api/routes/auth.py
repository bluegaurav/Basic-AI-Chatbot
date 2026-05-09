"""Authentication routes"""
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user import create_user, authenticate_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate):
    if await get_user_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = await create_user(user_in)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role={"title": user.role_title, "description": user.role_description},
            context=user.context,
            created_at=user.created_at
        ),
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role={"title": user.role_title, "description": user.role_description},
            context=user.context,
            created_at=user.created_at
        ),
        "access_token": access_token,
        "token_type": "bearer"
    }
