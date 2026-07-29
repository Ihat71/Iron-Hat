from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from api.dependencies import get_current_user
from services.profile_services import update_username_service, update_email_service, update_full_name_service
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate, UserNameUpdate, UserEmailUpdate, UserFullNameUpdate
from schemas.token import Token

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_info = UserRead(
        **current_user.model_dump()
    )

    return user_info

@router.patch("/username", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_my_username(data: UserNameUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    #can only update username every few days
    return update_username_service(db, current_user, data)

@router.patch("/email", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_my_email(data: UserEmailUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    return update_email_service(db, current_user, data.email)

@router.patch("/name", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_my_name(data: UserFullNameUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_full_name_service(db, current_user, data.full_name)

