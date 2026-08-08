from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user

from backend.services.workout_templates_service import (get_workout_template_by_value_service,  
            get_all_workout_templates_service, add_workout_template_service, update_workout_template_service, 
            delete_workout_template_service)

from backend.models.user import User
from backend.models.workout_templates import WorkoutTemplate
from backend.schemas.workout_templates import WorkoutTemplateCreate, WorkoutTemplateRead, WorkoutTemplateUpdate
from typing import Any

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)

@router.post("/add/{program_id}", response_model=WorkoutTemplateRead, status_code=status.HTTP_201_CREATED)
def add_workout(program_id: int, data: WorkoutTemplateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data.program_id = program_id
    return add_workout_template_service(db, data, program_id, current_user)

@router.get("/search/{program_id}/{value}", response_model=list[WorkoutTemplateRead], status_code=status.HTTP_200_OK)
def search_workouts_by_value(value: Any, program_id: int, workout_type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_template_by_value_service(db, workout_type, value, program_id, current_user)

@router.get("/search/all", response_model=list[WorkoutTemplateRead], status_code=status.HTTP_200_OK)
def search_all_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_workout_templates_service(db, current_user)

@router.patch("/{workout_id}", response_model=WorkoutTemplateRead, status_code=status.HTTP_200_OK)
def update_workout(workout_id: int, data: WorkoutTemplateUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_workout_template_service(db, data, workout_id, current_user)

@router.delete("/{workout_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout_template_service(db, current_user, workout_id)