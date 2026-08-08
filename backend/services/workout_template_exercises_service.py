from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.crud.workout_template_exercises import (
    create_workout_template_exercise, delete_workout_template_exercise, get_workout_template_exercise,
    get_user_workout_template_exercises_by_program, get_all_user_workout_template_exercises, get_user_workout_template_exercises_by_workout_value
)
from backend.crud.program_templates import get_program
from backend.models.user import User
from backend.models.workout_template_exercises import WorkoutTemplateExercise
from backend.schemas.workout_template_exercises import WorkoutTemplateExerciseCreate, WorkoutTemplateExerciseUpdate
from typing import Any

def is_valid(db: Session, user_id, workout_id):
    workout = get_workout_template_exercise(db, workout_id)
    program = get_program(db, workout.program_id)

    if program.user_id != user_id:
        return False
   
    return True

def add_workout_template_exercise_service(db: Session, data: WorkoutTemplateExerciseCreate, program_id: int, user: User):
    program = get_program(db, program_id)

    if program.user_id != user.id:
        raise ValueError("cannot access that")
    
    data = WorkoutTemplateExercise(
        workout_template_id = data.workout_template_id,
        exercise_id = data.exercise_id
    )
    return create_workout_template_exercise(db, data)

def get_workout_template_exercises_by_workout_service(db: Session, type: str, value: Any, workout_id: int, user: User):
    return get_user_workout_template_exercises_by_workout_value(db, user.id, workout_id)

def get_all_workout_template_exercises_service(db: Session, user: User):
    return get_all_user_workout_template_exercises(db, user.id)

def get_workout_template_exercises_by_program_service(db: Session, program_id: int, user: User):
    return get_user_workout_template_exercises_by_program(db, user.id, program_id)


# def update_workout_template_exercise_service(db: Session, data: WorkoutTemplateExerciseUpdate, workout_id: int, user: User):
#     if not is_valid(db, user.id, workout_id):
#         raise ValueError("cant access that")
    
#     return update_workout_template_exercise(db, workout_id, data)

def delete_workout_template_exercise_service(db: Session, user: User, workout_id: int):
    if not is_valid(db, user.id, workout_id):
        raise ValueError("cant access that")
    
    return delete_workout_template_exercise(db, workout_id)