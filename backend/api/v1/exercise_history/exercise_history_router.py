from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.api.dependencies import get_current_user
from backend.services.exercise_history_service import (
    create_exercise_history_service, get_exercise_history_service, get_all_exercise_history,
    get_all_exercise_history_service, delete_exercise_history_service, parameter_search_exercise_history_service
)
from backend.models.user import User
from backend.schemas.exercise_history import ExerciseHistoryRead, ExerciseHistoryCreate, ExerciseHistorySearch


router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)

@router.post("/", response_model=ExerciseHistoryRead, status_code=status.HTTP_200_OK)
def create_exercise_history(data: ExerciseHistoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_exercise_history_service(data, db, current_user)

@router.get("/{history_id}", response_model=ExerciseHistoryRead, status_code=status.HTTP_200_OK)
def get_exercise_history(history_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_exercise_history_service(history_id, db, current_user)

@router.get("/search", , response_model=list[ExerciseHistoryRead], status_code=status.HTTP_200_OK)
def search_exercise_history(
    exercise_id: int,
    exercise_type: str,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):
    search = ExerciseHistorySearch(
        exercise_id = exercise_id,
        exercise_type = exercise_type
    )
    return parameter_search_exercise_history_service(search, db, current_user)

@router.get("/search/all", response_model=list[ExerciseHistoryRead], status_code=status.HTTP_200_OK)
def search_all_history(page: int = 1, page_size: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_exercise_history_service(page, page_size, db, current_user)


@router.delete("/{history_id}", response_model=bool, status_code=status.HTTP_200_OK)
def delete_exercise_history(history_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_exercise_history_service(history_id, db, current_user)


