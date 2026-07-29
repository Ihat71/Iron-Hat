from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from api.dependencies import get_current_user
from services.biometrics_service import (
    add_bio_service, get_bio_history_service, get_recent_bio_history_service,
    get_last_5_bio_history_service, update_recent_bio_service, 
    delete_bio_service
)
from models.user import User
from schemas.user_biometrics import BiometricRead, BiometricCreate, BiometricUpdate


router = APIRouter(
    prefix="/biometrics",
    tags=["Biometrics"]
)

@router.post("/create", response_model=BiometricRead, status_code=status.HTTP_201_CREATED)
def create_biometrics(data: BiometricCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_bio_service(data, db, current_user)

@router.get("/history", response_model=BiometricRead, status_code=status.HTTP_200_OK)
def get_bio_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_bio_history_service(db, current_user)

@router.get("/recent", response_model=BiometricRead, status_code=status.HTTP_200_OK)
def get_recent_bio(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_recent_bio_history_service(db, current_user)

@router.get("/recent/last-5", response_model=BiometricRead, status_code=status.HTTP_200_OK)
def get_last_5_bio(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_last_5_bio_history_service(db, current_user)

@router.patch("/update/{bio_id}", response_model=BiometricRead, status_code=status.HTTP_200_OK)
def update_recent_bio(bio_id: int, update_data: BiometricUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_recent_bio_service(bio_id, db, update_data, current_user)

@router.delete("/delete/{bio_id}", response_model=BiometricRead, status_code=status.HTTP_200_OK)
def delete_recent_bio(bio_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_bio_service(bio_id, db, current_user)

