from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.exercise_history import ExerciseHistory
from backend.models.program_templates import ProgramTemplates
from backend.models.workout_log_exercises import WorkoutLogExercise
from backend.schemas.exercise_history import ExerciseHistoryCreate, ExerciseHistoryUpdate
from backend.models.user import User



def create_exercise_history(db: Session,history_data: ExerciseHistoryCreate) -> ExerciseHistory:
    history = ExerciseHistory(**history_data.model_dump())

    db.add(history)
    db.commit()
    db.refresh(history)

    return history


def get_exercise_history(db: Session, workout_exercise_id: int):
    stmt = select(ExerciseHistory).where(ExerciseHistory.workout_log_exercise_id==workout_exercise_id)
    return db.execute(stmt).scalars().one_or_none()

def get_exercise_history_by_exercise(exercise_id: int, db: Session, current_user: User):
    stmt = select(ExerciseHistory).join(WorkoutLogExercise).where(
        ExerciseHistory.user_id == current_user.id, 
        WorkoutLogExercise.exercise_id == exercise_id
    )

    return db.execute(stmt).scalars().all()

def delete_exercise_history(db: Session, workout_exercise_id: int) -> bool:
    history = get_exercise_history(db, workout_exercise_id)

    if history is None:
        return False

    db.delete(history)
    db.commit()

    return True