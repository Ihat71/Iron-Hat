from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.workout_logs_service import (
    add_workout_log_service,
    get_all_workout_logs_service, 
    update_workout_log_service, delete_workout_log_service, get_workout_log_service
)
from backend.models.user import User
from backend.schemas.workout_logs import WorkoutLogCreate, WorkoutLogRead, WorkoutLogUpdate, SearchLogs
from backend.schemas.token import Token
from typing import Any


router = APIRouter(
    prefix="",
    tags=["WorkoutLog"]
)

@router.post("/", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def create_workout_logs(data: WorkoutLogCreate, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_workout_log_service(db, data, program_id, current_user)

@router.get("/", response_model=list[WorkoutLogRead], status_code=status.HTTP_200_OK)
def search_all_workout_logs(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_workout_logs_service(db, program_id, current_user)

@router.get("/{workout_log_id}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def get_workout_log(program_id: int, workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_log_service(program_id, workout_id, db, current_user)

@router.patch("/{workout_log_id}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def update_workout_logs(program_id: int, workout_id: int, data: WorkoutLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_workout_log_service(db, data, workout_id, program_id, current_user)

@router.delete("/{workout_log_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_workout_logs(program_id: int, workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout_log_service(program_id, workout_id, db, current_user)