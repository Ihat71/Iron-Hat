from sqlalchemy import select
from sqlalchemy.orm import Session

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


def create_workout_log_exercise(db: Session, log_data: WorkoutLogExerciseCreate) -> WorkoutLogExercise:
    exercise = WorkoutLogExercise(**log_data.model_dump())

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

def get_workout_log_exercise(db: Session, log_id: int) -> WorkoutLogExercise:
    return db.get(WorkoutLogExercise, log_id)

def get_all_workout_log_exercises(db: Session) -> list[WorkoutLogExercise] :

    results = db.execute(select(WorkoutLogExercise)).scalars().all()

    return results

def get_all_user_workout_log_exercises(db: Session, user_id: int) -> list[WorkoutLogExercise]:
    stmt = select(WorkoutLogExercise).join(WorkoutLogExercise).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_workout_log_exercise_by_id(db: Session, workout_id: int):
    return db.execute(WorkoutLogExercise, workout_id)

def get_user_workout_log_exercises_by_program(db: Session, user_id: int, program_id: int):
    stmt = select(WorkoutLogExercise).join(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_log_exercise_by_workout(db: Session, user_id: int, workout_id: int):
    stmt = select(WorkoutLogExercise).join(WorkoutLog).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, WorkoutLog.id == workout_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_log_exercises_by_workout_value(db: Session, value_type: str, value: Any, user_id: int, program_id: int):
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

    return db.execute(stmt).scalars().all()

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


def delete_workout_log_exercise(db: Session, log_id: int) -> bool:
    exercise = db.get(WorkoutLogExercise, log_id)

    if exercise is None:
        return False

    db.delete(exercise)
    db.commit()

    return True