from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.workout_exercises import WorkoutExercises
from backend.schemas.workout_exercises import WorkoutExerciseCreate, WorkoutExerciseUpdate


def create_workout_exercise(db: Session, exercise_data: WorkoutExerciseCreate) -> WorkoutExercises:

    exercise = WorkoutExercises(**exercise_data.model_dump())

    db.add(exercise)
    db.commit()
    db.refresh(exercise)

    return exercise

def get_workout_exercises(db: Session, workout_id: int) -> list[WorkoutExercises]:
    #gets workout exercises from the workout they are assigned to 
    return db.execute(select(WorkoutExercises).where(WorkoutExercises.workout_id == workout_id)).scalars().all()

def get_workout_exercise(db: Session, exercise_id: int) -> WorkoutExercises:
    return db.get(WorkoutExercises, exercise_id)

def update_workout_exercise(db: Session, exercise_data: WorkoutExerciseUpdate) -> WorkoutExercises | None:
    
    exercise = get_workout_exercise(db, exercise_data.id)

    if not exercise:
        return None
    
    update_data = exercise_data.model_dump(exclude_unset=True, exclude={"id"})
    
    for key, value in update_data.items():
        setattr(exercise, key, value)
    
    db.commit()

    db.refresh(exercise)

    return exercise

def delete_workout_exercise(db: Session, exercise_id: int) -> bool:
    exercise = get_workout_exercise(db, exercise_id)

    if exercise is None:
        return False
    
    db.delete(exercise)
    db.commit()

    return True