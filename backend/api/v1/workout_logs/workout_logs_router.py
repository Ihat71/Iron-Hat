from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.workout_logs_service import (
    add_workout_log_service,
    get_all_workout_logs_service, get_workout_logs_service, get_workout_log_by_value_service, 
    update_workout_log_service, delete_workout_log_service
)
from backend.models.user import User
from backend.schemas.workout_logs import WorkoutLogCreate, WorkoutLogRead, WorkoutLogUpdate
from backend.schemas.token import Token
from typing import Any


router = APIRouter(
    prefix="/workout-template",
    tags=["WorkoutLog"]
)

@router.post("/add/{program_id}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def create_workout_logs(data: WorkoutLogCreate, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_workout_log_service(db, data, program_id, current_user)

@router.get("/search/all", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def search_all_workout_logs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_workout_logs_service(db, current_user)

@router.get("/search/{program_id}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def search_workout_logs(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_logs_service(db, program_id, current_user)

@router.get("/search/{program_id}/{value}/{value_data}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def search_workout_logs_by_value(value: str, value_data: Any, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_log_by_value_service(db, value_data, value, program_id, current_user)

@router.patch("/update/{workout_log_id}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def update_workout_logs(template_id: int, data: WorkoutLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_workout_log_service(db, data, template_id, current_user)

@router.delete("/delete/{workout_log_id}", response_model=WorkoutLogRead, status_code=status.HTTP_200_OK)
def delete_workout_logs(template_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout_log_service(db, template_id, current_user)