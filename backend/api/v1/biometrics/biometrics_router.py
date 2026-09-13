from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.biometrics_service import (
    add_bio_service, get_bio_history_service, get_recent_bio_history_service,
    get_last_5_bio_history_service, update_recent_bio_service,
    delete_bio_service
)
from backend.models.user import User
from backend.schemas.user_biometrics import BiometricRead, BiometricCreate, BiometricUpdate


router = APIRouter(
    prefix="/biometrics",
    tags=["Biometrics"]
)

@router.post("", response_model=BiometricRead, status_code=status.HTTP_201_CREATED)
async def create_biometrics(data: BiometricCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await add_bio_service(data, db, current_user)

@router.get("/history", response_model=list[BiometricRead], status_code=status.HTTP_200_OK)
async def get_bio_history(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_bio_history_service(db, current_user)

@router.get("/recent", response_model=BiometricRead, status_code=status.HTTP_200_OK)
async def get_recent_bio(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_recent_bio_history_service(db, current_user)

@router.get("/recent/last-5", response_model=list[BiometricRead], status_code=status.HTTP_200_OK)
async def get_last_5_bio(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_last_5_bio_history_service(db, current_user)

@router.patch("/{bio_id}", response_model=BiometricRead, status_code=status.HTTP_200_OK)
async def update_recent_bio(bio_id: int, update_data: BiometricUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await update_recent_bio_service(bio_id, update_data, db, current_user)

@router.delete("/{bio_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_recent_bio(bio_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await delete_bio_service(bio_id, db, current_user)
