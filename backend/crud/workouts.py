from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.workouts import Workouts
from backend.models.program_templates import ProgramTemplates
from backend.schemas.workouts import WorkoutCreate, WorkoutUpdate


def create_workout(db: Session, workout_data: WorkoutCreate) -> Workouts:
    workout = Workouts(**workout_data.model_dump())

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout


def get_workout(db: Session, workout_id: int) -> Workouts | None:
    return db.get(Workouts, workout_id)

def get_all_workouts(db: Session) -> list[Workouts] | None:
    results = db.execute(select(Workouts)).scalars().all()
    if results is None:
        return None
    return results

def get_user_workouts(db: Session, user_id: int) -> list[Workouts]:
    stmt = select(Workouts).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()


def get_user_workouts_by_type(db: Session, user_id: int, workout_type: str) -> list[Workouts]:
    stmt = (
        select(Workouts).join(ProgramTemplates)
        .where(
            ProgramTemplates.user_id == user_id,
            Workouts.workout_type == workout_type,
        )
    )

    return db.execute(stmt).scalars().all()


def update_workout(db: Session, workout_id: int, workout_data: WorkoutUpdate) -> Workouts | None:
    workout = db.get(Workouts, workout_id)

    if workout is None:
        return None

    update_data = workout_data.model_dump(exclude_unset=True, exclude={"id"})

    for field, value in update_data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout


def delete_workout(db: Session, workout_id: int) -> bool:
    workout = db.get(Workouts, workout_id)

    if workout is None:
        return False

    db.delete(workout)
    db.commit()

    return True