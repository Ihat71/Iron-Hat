from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.exercise_history import ExerciseHistory
from backend.models.workouts import Workouts
from backend.models.program_templates import ProgramTemplates
from backend.schemas.exercise_history import ExerciseHistoryCreate, ExerciseHistoryUpdate



def create_exercise_history(db: Session,history_data: ExerciseHistoryCreate) -> ExerciseHistory:
    history = ExerciseHistory(**history_data.model_dump())

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def get_exercise_history(db: Session, history_id: int) -> ExerciseHistory | None:
    return db.get(ExerciseHistory, history_id)


def get_user_exercise_history(db: Session, user_id: int) -> list[ExerciseHistory]:

    stmt = select(ExerciseHistory).join(Workouts).join(ProgramTemplates).where(ProgramTemplates.user_id == user_id)
    return db.execute(stmt).scalars().all()


def update_exercise_history(db: Session, history_id: int, history_data: ExerciseHistoryUpdate) -> ExerciseHistory | None:
    history = get_exercise_history(db, history_id)

    if history is None:
        return None

    update_data = history_data.model_dump(exclude_unset=True, exclude={"id"})

    for field, value in update_data.items():
        setattr(history, field, value)

    db.commit()
    db.refresh(history)

    return history


def delete_exercise_history(db: Session, history_id: int) -> bool:
    history = get_exercise_history(db, history_id)

    if history is None:
        return False

    db.delete(history)
    db.commit()

    return True