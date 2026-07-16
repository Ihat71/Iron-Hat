from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from api.dependencies import get_current_user
from services.profile_services import update_username, update_email, update_full_name
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from schemas.token import Token

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get(response_model=UserRead, status_code=status.HTTP_200_OK)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = UserRead(
        current_user.full_name,
        current_user.username,
        current_user.email
    )

    return user_info

@router.patch("/username", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_my_username(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    #can only update username every few days
    return update_username(db, current_user, data)

@router.patch("/email", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_my_email(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_email(db, current_user, data.email)

@router.patch("/name", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_my_name(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_full_name(db, current_user, data.full_name)

