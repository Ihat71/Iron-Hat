from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.crud.workout_log_exercises import (
    create_workout_log_exercise, delete_workout_log_exercise, get_workout_log_exercise,
    get_user_workout_log_exercises_by_program, get_all_user_workout_log_exercises, 
    get_user_workout_log_exercises_by_workout_value, get_workout_log_exercise_by_id

)
from backend.crud.exercise_history import create_exercise_history, get_exercise_history, delete_exercise_history
from backend.crud.program_templates import get_program
from backend.models.user import User
from backend.models.workout_log_exercises import WorkoutLogExercise
from backend.models.exercise_history import ExerciseHistory
from backend.schemas.workout_log_exercises import WorkoutLogExerciseCreate, WorkoutLogExerciseUpdate
from backend.schemas.exercise_history import ExerciseHistoryCreate
from typing import Any

def is_valid(db: Session, user_id, workout_id):
    workout = get_workout_log_exercise(db, workout_id)
    program = get_program(db, workout.program_id)

    if program.user_id != user_id:
        return False
   
    return True

def add_workout_log_exercise_service(db: Session, log_data: WorkoutLogExerciseCreate, exercise_data: ExerciseHistoryCreate, program_id: int, user: User):
    program = get_program(db, program_id)

    if program.user_id != user.id:
        raise ValueError("cannot access that")
    
    workout_exercise_log_data = WorkoutLogExercise(
        workout_log_id = log_data.workout_log_id,
        exercise_id = log_data.exercise_id
    )
    workout_log_exercise = create_workout_log_exercise(db, workout_exercise_log_data)

    exercise_history_data = ExerciseHistory(
        user_id=user.id,
        workout_log_exercise_id=workout_log_exercise.id,
        exercise_type= exercise_data.exercise_type,
        sets = exercise_data.sets,
        top_weight=exercise_data.top_weight,
        max_reps=exercise_data.max_reps,
        total_volume=exercise_data.total_volume,
        detailed_sets=exercise_data.detailed_sets,
        max_rpe=exercise_data.max_rpe,
        notes=exercise_data.notes
    )

    exercise_history = create_exercise_history(db, exercise_history_data)

    return workout_log_exercise


def get_workout_log_exercises_by_value_service(db: Session, type: str, value: Any, program_id: int, user: User):
    return get_user_workout_log_exercises_by_workout_value(db, type, value, program_id, user.id)

def get_all_workout_log_exercises_service(db: Session, user: User):
    return get_all_user_workout_log_exercises(db, user.id)

def get_workout_log_exercises_service(db: Session, program_id: int, user: User):
    return get_user_workout_log_exercises_by_program(db, user.id, program_id)

def get_workout_log_exercise_by_id_service(db: Session, workout_id: int, user: User):
    exercise_history = get_exercise_history(db, workout_id)
    if exercise_history.user_id != user.id:
        raise ValueError("cant access that")
    
    return get_workout_log_exercise_by_id(db, workout_id), exercise_history
    



# def update_workout_log_exercise_service(db: Session, data: WorkoutLogExerciseUpdate, workout_id: int, user: User):
#     if not is_valid(db, user.id, workout_id):
#         raise ValueError("cant access that")
    
#     return update_workout_log_exercise(db, workout_id, data)

def delete_workout_log_exercise_service(db: Session, user: User, workout_id: int):
    if not is_valid(db, user.id, workout_id):
        raise ValueError("cant access that")
    
    delete_exercise_history(db, workout_id)

    return delete_workout_log_exercise(db, workout_id)