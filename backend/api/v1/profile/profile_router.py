from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.profile_services import update_username_service, update_email_service, update_full_name_service
from backend.models.user import User
from backend.schemas.user import UserCreate, UserRead, UserUpdate, UserNameUpdate, UserEmailUpdate, UserFullNameUpdate
from backend.schemas.token import Token

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_me(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = UserRead(
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        gender=current_user.gender,
        created_at=current_user.created_at,
        last_updated_username=current_user.last_updated_username
    )

    return user_info

@router.patch("/username", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_my_username(data: UserNameUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    #can only update username every few days
    return await update_username_service(db, current_user, data)

@router.patch("/email", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_my_email(data: UserEmailUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    return await update_email_service(db, current_user, data.email)

@router.patch("/name", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_my_name(data: UserFullNameUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await update_full_name_service(db, current_user, data.full_name)
