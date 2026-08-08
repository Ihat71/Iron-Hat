from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, UTC

from backend.models.user import User
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_logs import WorkoutLog
from backend.models.workout_logs import WorkoutLog
from backend.schemas.workout_logs import WorkoutLogCreate, WorkoutLogUpdate
from typing import Any

VALID_COLUMNS = [
    "day_number",
    "workout_type",
]


def create_workout_log(db: Session, log_data: WorkoutLogCreate) -> WorkoutLog:
    exercise = WorkoutLog(**log_data.model_dump())

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

def get_workout_log(db: Session, log_id: int) -> WorkoutLog:
    return db.get(WorkoutLog, log_id)

def get_all_workout_logs(db: Session) -> list[WorkoutLog] :
    results = db.execute(select(WorkoutLog)).scalars().all()

    return results

def get_user_workout_logs(db: Session, user_id: int) -> list[WorkoutLog]:
    stmt = select(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_all_user_workout_logs(db: Session, user_id: int):
    stmt = select(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_logs_by_program(db: Session, user_id: int, program_id):
    stmt = select(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_logs_by_value(db: Session, value_type: str, value: Any, program_id: int, user_id: int):

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

    return db.execute(stmt).scalars().all()

def get_workouts_done(days_ago: int, db: Session, user: User):
    days = datetime.now(UTC) - timedelta(days=days_ago)
    stmt = select(WorkoutLog).join(ProgramTemplates).where(
        ProgramTemplates.user_id == user.id,
        WorkoutLog.inserted_at >= days
    )

    return db.execute(stmt).scalars().all()

def get_workout_logs_count(program_id: int, days_ago: int, db: Session, user: User) -> int:
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

    return db.scalar(stmt)


def update_workout_log(db: Session, log_id: int, log_data: WorkoutLogUpdate) -> WorkoutLog | None:
    workout = db.get(WorkoutLog, log_id)

    if workout is None:
        return None

    update_data = log_data.model_dump(exclude_unset=True, exclude={"id"})

    for field, value in update_data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout


def delete_workout_log(db: Session, log_id: int) -> bool:
    exercise = db.get(WorkoutLog, log_id)

    if exercise is None:
        return False

    db.delete(exercise)
    db.commit()

    return True