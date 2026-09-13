from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.exercises import Exercises
from backend.schemas.exercises import ExerciseSearch



async def get_exercise(exercise_id: int, db: AsyncSession) -> Exercises | None:
    stmt = select(Exercises).where(Exercises.id == exercise_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_exercises(page, page_size, db: AsyncSession):
    offset = (page - 1) * page_size
    stmt = select(Exercises).offset(offset).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()

async def parameter_search(params: ExerciseSearch, db: AsyncSession):
    stmt = select(Exercises)

    if params.name:
        stmt = stmt.where(Exercises.name.ilike(f"%{params.name}%"))
    if params.force_type:
        stmt = stmt.where(Exercises.force_type == params.force_type)
    if params.main_muscle:
        stmt = stmt.where(Exercises.main_muscle == params.main_muscle)
    if params.difficulty:
        stmt = stmt.where(Exercises.difficulty == params.difficulty)

    result = await db.execute(stmt)
    return result.scalars().all()
