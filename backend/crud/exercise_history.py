from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.models.exercise_history import ExerciseHistory
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_log_exercises import WorkoutLogExercise
from backend.schemas.exercise_history import ExerciseHistoryCreate, ExerciseHistorySearch
from backend.models.user import User



def create_exercise_history(db: Session,history_data: ExerciseHistoryCreate, user: User) -> ExerciseHistory:
    history = ExerciseHistory(user_id = user.id, **history_data.model_dump())

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def get_exercise_history(history_id: int, db: Session, user: User):
    stmt = select(ExerciseHistory).options(selectinload(ExerciseHistory.exercise)).where(
        ExerciseHistory.id==history_id,
        ExerciseHistory.user_id == user.id
        )
    return db.execute(stmt).scalars().one_or_none()

def parameter_search_exercise_history(data: ExerciseHistorySearch, db: Session, user: User):
    search_data = data.model_dump()
    stmt = select(ExerciseHistory).where(ExerciseHistory.user_id == user.id)
    for key, val in search_data.items():
        column = getattr(ExerciseHistory, key)
        stmt = stmt.where(column==val)

    return db.execute(stmt).scalars().all()

def get_all_exercise_history(offset: int, limit: int, db: Session, user: User):
    stmt = select(ExerciseHistory).offset(offset).limit(limit)
    return db.execute(stmt).scalars().all()

def delete_exercise_history(history_id, db: Session, user: User) -> bool:
    history = get_exercise_history(history_id, db, user)

    if history is None:
        raise ValueError("Cant delete that")

    db.delete(history)
    db.commit()

    return True