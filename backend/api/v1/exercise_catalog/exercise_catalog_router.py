from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.exercise_catalog_service import (
    get_exercise_service, get_all_exercises_service,
    parameter_search_exercises_service
)
from backend.models.user import User
from backend.schemas.exercises import ExerciseRead, ExerciseSearch


router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)

@router.get("/{exercise_id}", response_model=ExerciseRead, status_code=status.HTTP_200_OK)
def get_exercise(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_exercise_service(exercise_id, db, current_user)

@router.get("/search/all", response_model=list[ExerciseRead], status_code=status.HTTP_200_OK)
def search_all_exercises(page: int, page_size: int = 20, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_exercises_service(page, page_size, db, current_user)

@router.get("/exercises")
def search_exercises(search: ExerciseSearch, db: Session, current_user: User = Depends(get_current_user)):
    return parameter_search_exercises_service(search, db, current_user)


