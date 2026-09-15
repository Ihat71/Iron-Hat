from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models.exercise_history import ExerciseHistory
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_logs import WorkoutLog
from backend.models.workout_log_exercises import WorkoutLogExercise
from backend.schemas.exercise_history import ExerciseHistoryCreate, ExerciseHistorySearch
from backend.models.user import User



async def create_exercise_history(db: AsyncSession, history_data: ExerciseHistoryCreate, user: User) -> ExerciseHistory:
    history = ExerciseHistory(user_id = user.id, **history_data.model_dump())

    db.add(history)
    await db.commit()
    await db.refresh(history)

    return history


async def get_exercise_history(history_id: int, db: AsyncSession, user: User):
    stmt = select(ExerciseHistory).options(selectinload(ExerciseHistory.exercise)).where(
        ExerciseHistory.id==history_id,
        ExerciseHistory.user_id == user.id
        )
    result = await db.execute(stmt)
    return result.scalars().one_or_none()

async def parameter_search_exercise_history(data: ExerciseHistorySearch, db: AsyncSession, user: User):
    search_data = data.model_dump()
    stmt = select(ExerciseHistory).where(ExerciseHistory.user_id == user.id)
    for key, val in search_data.items():
        column = getattr(ExerciseHistory, key)
        stmt = stmt.where(column==val)

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_exercise_history_for_program_exercise(
    db: AsyncSession,
    user: User,
    program_id: int,
    exercise_id: int,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list[ExerciseHistory]:
    """All exercise history entries for one exercise, logged within one program, oldest first."""
    stmt = (
        select(ExerciseHistory)
        .join(WorkoutLogExercise, ExerciseHistory.workout_log_exercise_id == WorkoutLogExercise.id)
        .join(WorkoutLog, WorkoutLogExercise.workout_log_id == WorkoutLog.id)
        .where(
            ExerciseHistory.user_id == user.id,
            ExerciseHistory.exercise_id == exercise_id,
            WorkoutLog.program_id == program_id,
        )
        .order_by(ExerciseHistory.created_at)
    )

    if start is not None:
        stmt = stmt.where(ExerciseHistory.created_at >= start)
    if end is not None:
        stmt = stmt.where(ExerciseHistory.created_at < end)

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_all_exercise_history(offset: int, limit: int, db: AsyncSession, user: User):
    stmt = select(ExerciseHistory).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def delete_exercise_history(history_id, db: AsyncSession, user: User) -> bool:
    history = await get_exercise_history(history_id, db, user)

    if history is None:
        raise ValueError("Cant delete that")

    await db.delete(history)
    await db.commit()

    return True
