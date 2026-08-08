from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.workout_template_exercises_service import (
    add_workout_template_exercise_service,
    get_all_workout_template_exercises_service, get_workout_template_exercises_by_program_service, get_workout_template_exercises_by_workout_service, 
    delete_workout_template_exercise_service
)
from backend.models.user import User
from backend.schemas.workout_template_exercises import WorkoutTemplateExerciseCreate, WorkoutTemplateExerciseRead, WorkoutTemplateExerciseUpdate
from backend.schemas.token import Token
from typing import Any


router = APIRouter(
    prefix="/workout-template",
    tags=["WorkoutTemplate"]
)

@router.post("/add/{program_id}", response_model=WorkoutTemplateExerciseRead, status_code=status.HTTP_200_OK)
def create_workout_template_exercise(data: WorkoutTemplateExerciseCreate, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_workout_template_exercise_service(db, data, program_id, current_user)

@router.get("/search/all", response_model=WorkoutTemplateExerciseRead, status_code=status.HTTP_200_OK)
def search_all_workout_template_exercise(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_workout_template_exercises_service(db, current_user)

@router.get("/search/{program_id}", response_model=WorkoutTemplateExerciseRead, status_code=status.HTTP_200_OK)
def search_workout_template_exercise(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_template_exercises_by_program_service(db, program_id, current_user)

@router.get("/search/{program_id}/{value}/{value_data}", response_model=WorkoutTemplateExerciseRead, status_code=status.HTTP_200_OK)
def search_workout_template_exercise_by_value(value: str, value_data: Any, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_template_exercises_by_workout_service(db, value_data, value, program_id, current_user)

# @router.get("/update/{workout_template_id}", response_model=WorkoutTemplateExerciseRead, status_code=status.HTTP_200_OK)
# def update_workout_template_exercise(template_id: int, data: WorkoutTemplateExerciseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     return update_workout_template_service(db, data, template_id, current_user)

@router.delete("/delete/{workout_template_id}", response_model=WorkoutTemplateExerciseRead, status_code=status.HTTP_200_OK)
def delete_workout_template_exercise(template_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout_template_exercise_service(db, template_id, current_user)