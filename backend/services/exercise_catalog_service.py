from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from backend.crud.exercises import (
    get_exercise,get_all_exercises,parameter_search

)
from backend.models.user import User
from backend.models.exercises import Exercises
from backend.schemas.exercises import ExerciseSearch

async def get_exercise_service(exercise_id: int, db: AsyncSession, current_user: User):
    return await get_exercise(exercise_id, db)

async def get_all_exercises_service(page: int, page_size: int, db: AsyncSession, current_user: User):
    return await get_all_exercises(page, page_size, db)

async def parameter_search_exercises_service(
        search: ExerciseSearch,
        db: AsyncSession,
        current_user: User
    ):


    return await parameter_search(search, db)
