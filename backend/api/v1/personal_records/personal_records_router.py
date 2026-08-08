from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.personal_records_service import (add_pr_service, get_pr_history_service, 
        get_pr_history_by_exercise_service, get_prs_by_exercise_service, 
        get_pr_by_exercise_and_type_service, get_pr_history_by_pr_type_service, 
        delete_pr_service, get_pr_history_by_exercise_and_pr_type_service
)
from backend.models.user import User
from backend.schemas.personal_records import PersonalRecordRead, PersonalRecordCreate, PersonalRecordUpdate


router = APIRouter(
    prefix="/personal-records",
    tags=["PR"]
)

@router.get("/create", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def create_pr(data: PersonalRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_pr_service(data, db, current_user)

@router.get("/history", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_history_service(db, current_user)

@router.get("/history/{exercise_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr_history_by_exercise(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_history_by_exercise_service(exercise_id, db, current_user)

@router.get("/history/{exercise_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr_history_by_exercise_and_type(exercise_id: int, pr_type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_history_by_exercise_and_pr_type_service(exercise_id, pr_type, db, current_user)

@router.get("/history/{exercise_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr_history_by_type(pr_type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_history_by_pr_type_service(pr_type, db, current_user)

@router.get("/{exercise_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_prs_by_exercise(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_prs_by_exercise_service(exercise_id, db, current_user)

@router.get("/{exercise_id}/{pr_type}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_pr_by_exercise_and_type(exercise_id: int, pr_type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_by_exercise_and_type_service(exercise_id, pr_type, db, current_user)

@router.get("/{pr_type}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def get_prs_by_pr_type(pr_type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pr_history_by_pr_type_service(pr_type, db, current_user)

@router.delete("/delete/{record_id}", response_model=PersonalRecordRead, status_code=status.HTTP_200_OK)
def delete_pr(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_pr_service(record_id, db, current_user)

