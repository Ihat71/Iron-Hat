from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.exercises import Exercises
from backend.schemas.exercises import ExerciseCreate, ExerciseUpdate

def create_exercise(db: Session, exercise_data: ExerciseCreate) -> Exercises:

    exercise = Exercises(**exercise_data.model_dump())

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

def get_exercise(db: Session, exercise_id: int) -> Exercises | None:
    return db.get(Exercises, exercise_id)

def update_exercise(db: Session, exercise_data: ExerciseUpdate) -> Exercises | None:
    
    exercise = get_exercise(db, exercise_data.id)

    if not exercise:
        return None
    
    update_data = exercise_data.model_dump(exclude_unset=True, exclude={"id"})
    
    for key, value in update_data.items():
        setattr(exercise, key, value)
    
    db.commit()

    db.refresh(exercise)

    return exercise

def delete_exercise(db: Session, exercise_id: int) -> bool:
    exercise = get_exercise(db, exercise_id)

    if exercise is None:
        return False
    
    db.delete(exercise)
    db.commit()

    return True