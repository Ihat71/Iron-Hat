from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from services.auth_service import register_user, login_user
from api.dependencies import get_current_user
from models.user import User
from schemas.user import UserCreate, UserRead, UserLogin
from schemas.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED,)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(db, user_data)
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    
@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        token = login_user(db, user_data.username, user_data.password)
        return token
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user