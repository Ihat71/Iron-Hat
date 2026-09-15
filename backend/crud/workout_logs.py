from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, UTC

from backend.models.user import User
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_logs import WorkoutLog
from backend.models.workout_log_exercises import WorkoutLogExercise
from backend.schemas.workout_logs import WorkoutLogCreate, WorkoutLogUpdate, SearchLogs
from typing import Any

VALID_COLUMNS = [
    "day_number",
    "workout_type",
]


async def create_workout_log(db: AsyncSession, log_data: WorkoutLog) -> WorkoutLog:

    db.add(log_data)
    await db.commit()
    await db.refresh(log_data)

    return log_data


async def get_workout_log(program_id: int, workout_id: int, db: AsyncSession, user: User) -> WorkoutLog | None:
    stmt = select(WorkoutLog).options(
        selectinload(WorkoutLog.template),
        selectinload(WorkoutLog.exercises),
    ).where(WorkoutLog.program_id == program_id, WorkoutLog.id == workout_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_workout_logs(db: AsyncSession) -> list[WorkoutLog] :
    result = await db.execute(select(WorkoutLog))

    return result.scalars().all()

async def get_user_workout_logs(db: AsyncSession, user_id: int) -> list[WorkoutLog]:
    stmt = select(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_all_user_workout_logs(db: AsyncSession, program_id: int):
    stmt = select(WorkoutLog).options(selectinload(WorkoutLog.exercises)).where(WorkoutLog.program_id == program_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_logs_by_program(db: AsyncSession, user_id: int, program_id):
    stmt = select(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_logs_by_value(db: AsyncSession, value_type: str, value: Any, program_id: int, user_id: int):

    if value_type not in VALID_COLUMNS:
        raise ValueError("wrong value type selection")

    column = getattr(WorkoutLog, value_type)

    stmt = (
        select(WorkoutLog)
        .join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user_id,
            column == value,
            ProgramTemplates.id == program_id
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_workouts_done(days_ago: int, db: AsyncSession, user: User):
    days = datetime.now(UTC) - timedelta(days=days_ago)
    stmt = select(WorkoutLog).join(ProgramTemplates).where(
        ProgramTemplates.user_id == user.id,
        WorkoutLog.inserted_at >= days
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_workout_logs_in_range(program_id: int, start: datetime, end: datetime, db: AsyncSession, user: User) -> list[WorkoutLog]:
    stmt = (
        select(WorkoutLog)
        .join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user.id,
            ProgramTemplates.id == program_id,
            WorkoutLog.inserted_at >= start,
            WorkoutLog.inserted_at < end,
        )
        .order_by(WorkoutLog.inserted_at)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_all_workout_log_dates(program_id: int, db: AsyncSession, user: User) -> list[datetime]:
    """All-time workout dates for a program, oldest first. Used to compute streaks."""
    stmt = (
        select(WorkoutLog.inserted_at)
        .join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user.id,
            ProgramTemplates.id == program_id,
        )
        .order_by(WorkoutLog.inserted_at)
    )

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_workout_logs_count(program_id: int, days_ago: int, db: AsyncSession, user: User) -> int | None:
    cutoff = datetime.now(UTC) - timedelta(days=days_ago)

    stmt = (
        select(func.count(WorkoutLog.id))
        .join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user.id,
            WorkoutLog.inserted_at >= cutoff,
            ProgramTemplates.id == program_id
        )
    )

    return await db.scalar(stmt)


# def update_workout_log(db: Session, log_id: int, log_data: WorkoutLogUpdate) -> WorkoutLog | None:
#     workout = db.get(WorkoutLog, log_id)

#     if workout is None:
#         return None



#     update_data = log_data.model_dump(
#         exclude_unset=True,
#         exclude={"exercises"},
#     )

#     for field, value in update_data.items():
#         setattr(workout, field, value)

#     if log_data.exercises is not None:
#         for exercise in log_data.exercises:
#             workout_log_exercise = next(
#                 (x for x in workout.exercises if x.id == exercise.id),
#                 None,
#             )
#             if workout_log_exercise is None:
#                 raise ValueError("This workout exercise log is not part of this workout")

#             exercise_data = exercise.model_dump(exclude_unset=True, exclude={"id","exercise_history"})

#             for field, value in exercise_data.items():
#                 setattr(workout_log_exercise, field, value)

#             exercise_history = workout_log_exercise.exercise_history
#             if exercise.exercise_history is not None:
#                 if exercise_history is None:
#                     raise ValueError("Exercise history does not exist")
#                 history_data = exercise.exercise_history.model_dump(exclude_unset=True, exclude={"id"})
#                 for field, value in history_data.items():
#                     setattr(exercise_history, field, value)



#     db.commit()
#     db.refresh(workout)

#     return workout


async def delete_workout_log(db: AsyncSession, log_id: int) -> bool:
    workout = await db.get(WorkoutLog, log_id)

    if workout is None:
        return False

    await db.delete(workout)
    await db.commit()

    return True
