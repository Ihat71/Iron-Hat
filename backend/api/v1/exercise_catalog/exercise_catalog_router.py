from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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
async def get_exercise(exercise_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_exercise_service(exercise_id, db, current_user)

@router.get("/search", status_code=status.HTTP_200_OK)
async def search_exercises(
    name: str | None=None,
    force_type: str| None=None,
    main_muscle: str| None=None,
    difficulty: int| None=None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    search = ExerciseSearch(
        name=name,
        force_type=force_type,
        main_muscle=main_muscle,
        difficulty=difficulty
    )
    return await parameter_search_exercises_service(search, db, current_user)

@router.get("/search/all", response_model=list[ExerciseRead], status_code=status.HTTP_200_OK)
async def search_all_exercises(page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await get_all_exercises_service(page, page_size, db, current_user)
