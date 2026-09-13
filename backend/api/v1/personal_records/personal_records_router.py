from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.personal_records_service import (add_pr_service, get_pr_history_service,
        search_prs_service, get_pr_service, delete_pr_service
)
from backend.models.user import User
from backend.schemas.personal_records import PersonalRecordRead, PersonalRecordCreate, PersonalRecordUpdate, SearchPR


router = APIRouter(
    prefix="/personal-records",
    tags=["PR"]
)

@router.post("", response_model=PersonalRecordRead, status_code=status.HTTP_201_CREATED)
async def create_pr(data: PersonalRecordCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await add_pr_service(data, db, current_user)

#let it be able to seach for dates as well
@router.get("", response_model=list[PersonalRecordRead], status_code=status.HTTP_200_OK)
async def search_prs(search_data: SearchPR, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await search_prs_service(search_data, db, current_user)

@router.get("/{record_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
async def get_pr(record_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_pr_service(record_id, db, current_user)

@router.get("/history", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
async def get_pr_history(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_pr_history_service(db, current_user)

@router.delete("/{record_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
async def delete_pr(record_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await delete_pr_service(record_id, db, current_user)
