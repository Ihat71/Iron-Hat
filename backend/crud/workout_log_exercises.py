from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.user import User
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_logs import WorkoutLog
from backend.models.workout_log_exercises import WorkoutLogExercise
from backend.schemas.workout_log_exercises import WorkoutLogExerciseCreate, WorkoutLogExerciseUpdate
from typing import Any

VALID_COLUMNS = [
    "day_number",
    "workout_type",
]


async def create_workout_log_exercise(db: AsyncSession, log_data: WorkoutLogExerciseCreate) -> WorkoutLogExercise:
    exercise = WorkoutLogExercise(**log_data.model_dump())

    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)

    return exercise

async def get_workout_log_exercise(db: AsyncSession, log_id: int) -> WorkoutLogExercise:
    return await db.get(WorkoutLogExercise, log_id)

async def get_all_workout_log_exercises(db: AsyncSession) -> list[WorkoutLogExercise] :

    result = await db.execute(select(WorkoutLogExercise))

    return result.scalars().all()

async def get_all_user_workout_log_exercises(db: AsyncSession, user_id: int) -> list[WorkoutLogExercise]:
    stmt = select(WorkoutLogExercise).join(WorkoutLogExercise).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_workout_log_exercise_by_id(db: AsyncSession, workout_id: int):
    return await db.execute(WorkoutLogExercise, workout_id)

async def get_user_workout_log_exercises_by_program(db: AsyncSession, user_id: int, program_id: int):
    stmt = select(WorkoutLogExercise).join(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_log_exercise_by_workout(db: AsyncSession, user_id: int, workout_id: int):
    stmt = select(WorkoutLogExercise).join(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, WorkoutLog.id == workout_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_user_workout_log_exercises_by_workout_value(db: AsyncSession, value_type: str, value: Any, user_id: int, program_id: int):
    if value_type not in VALID_COLUMNS:
        raise ValueError("wrong value type selection")

    column = getattr(WorkoutLog, value_type)

    stmt = (
        select(WorkoutLogExercise)
        .join(WorkoutLog)
        .join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user_id,
            column == value,
            ProgramTemplates.id == program_id
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()

# justification: you dont really update a workout log exercise entry you just delete it
# def update_workout_log_exercise(db: Session, log_id: int, log_data: WorkoutLogExerciseUpdate) -> WorkoutLogExercise | None:
#     workout = db.get(WorkoutLogExercise, log_id)

#     if workout is None:
#         return None

#     update_data = log_data.model_dump(exclude_unset=True, exclude={"id"})

#     for field, value in update_data.items():
#         setattr(workout, field, value)

#     db.commit()
#     db.refresh(workout)

#     return workout


async def delete_workout_log_exercise(db: AsyncSession, log_id: int) -> bool:
    exercise = await db.get(WorkoutLogExercise, log_id)

    if exercise is None:
        return False

    await db.delete(exercise)
    await db.commit()

    return True
