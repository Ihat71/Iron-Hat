from backend.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from backend.crud.exercise_history import (create_exercise_history, get_exercise_history,
    get_all_exercise_history, delete_exercise_history
    )
from backend.schemas.exercise_history import ExerciseHistoryCreate, ExerciseHistorySearch

async def create_exercise_history_service(data: ExerciseHistoryCreate, db: AsyncSession, user: User):
    return await create_exercise_history(db, data, user)

async def get_exercise_history_service(history_id: int, db: AsyncSession, user: User):
    await get_exercise_history(history_id, db, user)

async def get_all_exercise_history_service(page: int, page_size: int, db: AsyncSession, user: User):
    offset = (page - 1) * page_size
    await get_all_exercise_history(offset, page_size, db, user)

async def parameter_search_exercise_history_service(search: ExerciseHistorySearch, db: AsyncSession, user: User):
    pass

async def delete_exercise_history_service(history_id: int, db: AsyncSession, user: User):
    return await delete_exercise_history(history_id, db, user)
