from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from api.dependencies import get_current_user
from services.workout_log_exercises_service import (
    add_workout_log_exercise_service,
    get_all_workout_log_exercises_service, get_workout_log_exercises_service, get_workout_log_exercises_by_value_service,
    delete_workout_log_exercise_service, get_workout_log_exercise_by_id_service
)
from models.user import User
from schemas.workout_log_exercises import WorkoutLogExerciseCreate, WorkoutLogExerciseRead, WorkoutLogExerciseUpdate
from schemas.exercise_history import ExerciseHistoryCreate
from schemas.token import Token
from typing import Any


router = APIRouter(
    prefix="/workout-template",
    tags=["WorkoutLogExercises"]
)

@router.post("/add/{program_id}", response_model=WorkoutLogExerciseRead, status_code=status.HTTP_200_OK)
def create_workout_log_exercises(data: WorkoutLogExerciseCreate, exercise_data: ExerciseHistoryCreate, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_workout_log_exercise_service(db, data, exercise_data, program_id, current_user)

@router.get("/search/all", response_model=WorkoutLogExerciseRead, status_code=status.HTTP_200_OK)
def search_all_workout_log_exercises(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_workout_log_exercises_service(db, current_user)

@router.get("/search/{program_id}", response_model=WorkoutLogExerciseRead, status_code=status.HTTP_200_OK)
def search_workout_log_exercises(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_log_exercises_service(db, program_id, current_user)

@router.get("/search/{program_id}/{value}/{value_data}", response_model=WorkoutLogExerciseRead, status_code=status.HTTP_200_OK)
def search_workout_log_exercises_by_value(value: str, value_data: Any, program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_log_exercises_by_value_service(db, value_data, value, program_id, current_user)

@router.get("/{workout_id}", response_model=WorkoutLogExerciseRead, status_code=status.HTTP_200_OK)
def search_workout_log_exercises_by_id(workout_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_log_exercise_by_id_service(db, workout_id, current_user)

@router.delete("/delete/{workout_log_exercise_id}", response_model=WorkoutLogExerciseRead, status_code=status.HTTP_200_OK)
def delete_workout_log_exercises(template_id, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout_log_exercise_service(db, template_id, current_user)