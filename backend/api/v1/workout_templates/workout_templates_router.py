from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from api.dependencies import get_current_user

from services.workout_templates_service import (get_workout_templates_by_program_service, 
            get_workout_templates_by_day_service, get_workout_templates_by_type_service, 
            get_all_workout_templates_service, add_workout_template_service, update_workout_template_service, 
            delete_workout_template_service)

from models.user import User
from models.workout_templates import WorkoutTemplate
from schemas.workout_templates import WorkoutTemplateCreate, WorkoutTemplateRead, WorkoutTemplateUpdate

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)

@router.post("/add/{program_id}", response_model=WorkoutTemplateRead, status_code=status.HTTP_201_CREATED)
def add_workout(program_id: int, data: WorkoutTemplateCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data.program_id = program_id
    return add_workout_template_service(db, current_user, program_id, data)

@router.get("/search/program/{program_id}", response_model=list[WorkoutTemplateRead], status_code=status.HTTP_200_OK)
def search_workouts_by_program(program_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_templates_by_program_service(db, current_user, program_id)

@router.get("/search/day/{day_number}", response_model=list[WorkoutTemplateRead], status_code=status.HTTP_200_OK)
def search_workouts_by_day(day_number: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_templates_by_day_service(db, current_user, day_number)

@router.get("/search/type/{workout_type}", response_model=list[WorkoutTemplateRead], status_code=status.HTTP_200_OK)
def search_workouts_by_type(workout_type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_workout_templates_by_type_service(db, current_user, workout_type)

@router.get("/search/all", response_model=list[WorkoutTemplateRead], status_code=status.HTTP_200_OK)
def search_all_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_workout_templates_service(db, current_user)

@router.patch("/{workout_id}", response_model=WorkoutTemplateRead, status_code=status.HTTP_200_OK)
def update_workout(workout_id: int, data: WorkoutTemplateUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_workout_template_service(db, current_user, workout_id, data)

@router.delete("/{workout_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout_template_service(db, current_user, workout_id)