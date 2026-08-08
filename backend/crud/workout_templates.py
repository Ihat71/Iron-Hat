from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.workout_templates import WorkoutTemplate
from backend.models.program_templates import ProgramTemplates
from backend.schemas.workout_templates import WorkoutTemplateCreate, WorkoutTemplateUpdate
from typing import Any

VALID_COLUMNS = [
    "day_number",
    "workout_type",
]

def create_workout_template(db: Session, workout_data: WorkoutTemplateCreate) -> WorkoutTemplate:
    workout = WorkoutTemplate(**workout_data.model_dump())

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout


def get_workout_template(db: Session, workout_id: int) -> WorkoutTemplate:
    return db.get(WorkoutTemplate, workout_id)

def get_all_workout_templates(db: Session) -> list[WorkoutTemplate] :

    results = db.execute(select(WorkoutTemplate)).scalars().all()

    return results

def get_all_user_workout_templates(db: Session, user_id: int):
    stmt = select(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_user_workout_templates(db: Session, user_id: int, program_id: int) -> list[WorkoutTemplate]:
    stmt = select(WorkoutTemplate).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id, ProgramTemplates.id == program_id)
    return db.execute(stmt).scalars().all()


def get_user_workout_template_by_value(db: Session, value_type: str, value: Any, program_id: int, user_id: int) -> list[WorkoutTemplate]:
    if value_type not in VALID_COLUMNS:
        raise ValueError("wrong value type selection")

    column = getattr(WorkoutTemplate, value_type)

    stmt = (
        select(WorkoutTemplate)
        .join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user_id,
            column == value,
            ProgramTemplates.id == program_id
        )
    )

    return db.execute(stmt).scalars().all()

def get_workout_template_target_consistency_per_week(program_id: int, db: Session, current_user: User):
    stmt = select(func.count(WorkoutTemplate.id)).join(ProgramTemplates).where(ProgramTemplates.user_id == current_user.id, WorkoutTemplate.program_id == program_id)
    return db.scalar(stmt)


def update_workout_template(db: Session, workout_id: int, workout_data: WorkoutTemplateUpdate) -> WorkoutTemplate | None:
    workout = db.get(WorkoutTemplate, workout_id)

    if workout is None:
        return None

    update_data = workout_data.model_dump(exclude_unset=True, exclude={"id"})

    for field, value in update_data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout


def delete_workout_template(db: Session, workout_id: int) -> bool:
    workout = db.get(WorkoutTemplate, workout_id)

    if workout is None:
        return False

    db.delete(workout)
    db.commit()

    return True