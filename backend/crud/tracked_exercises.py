from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.tracked_exercises import TrackedExercise


async def create_tracked_exercise(db: AsyncSession, program_id: int, exercise_id: int) -> TrackedExercise:
    tracked = TrackedExercise(program_id=program_id, exercise_id=exercise_id)

    db.add(tracked)
    await db.commit()
    await db.refresh(tracked, attribute_names=["exercise"])

    return tracked


async def get_tracked_exercise(db: AsyncSession, program_id: int, tracked_id: int) -> TrackedExercise | None:
    stmt = select(TrackedExercise).where(
        TrackedExercise.id == tracked_id,
        TrackedExercise.program_id == program_id,
    )
    return await db.scalar(stmt)


async def get_tracked_exercises_by_program(db: AsyncSession, program_id: int) -> list[TrackedExercise]:
    stmt = select(TrackedExercise).options(selectinload(TrackedExercise.exercise)).where(
        TrackedExercise.program_id == program_id
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def delete_tracked_exercise(db: AsyncSession, tracked: TrackedExercise) -> bool:
    await db.delete(tracked)
    await db.commit()

    return True
