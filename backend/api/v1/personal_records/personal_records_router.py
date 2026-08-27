from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

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
def create_pr(data: PersonalRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_pr_service(data, db, current_user)

#let it be able to seach for dates as well
@router.get("", response_model=list[PersonalRecordRead], status_code=status.HTTP_200_OK)
def search_prs(search_data: SearchPR, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return search_prs_service(search_data, db, current_user)

@router.get("/{record_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_service(record_id, db, current_user)

@router.get("/history", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_history_service(db, current_user)

@router.delete("/{record_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def delete_pr(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_pr_service(record_id, db, current_user)

