from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.exercises import Exercises
from backend.schemas.exercises import ExerciseSearch



def get_exercise(exercise_id: int, db: Session) -> Exercises | None:
    stmt = select(Exercises).where(Exercises.id == exercise_id)
    return db.execute(stmt).scalar_one_or_none()


def get_all_exercises(page, page_size, db: Session):
    offset = (page - 1) * page_size
    stmt = select(Exercises).offset(offset).limit(page_size)
    return db.execute(stmt).scalars().all()

def parameter_search(params: ExerciseSearch, db: Session):
    stmt = select(Exercises)

    if params.name:
        stmt = stmt.where(Exercises.name.ilike(f"%{params.name}%"))
    if params.force_type:
        stmt = stmt.where(Exercises.force_type == params.force_type)
    if params.main_muscle:
        stmt = stmt.where(Exercises.main_muscle == params.main_muscle)
    if params.difficulty:
        stmt = stmt.where(Exercises.difficulty == params.difficulty)

    return db.execute(stmt).scalars().all()