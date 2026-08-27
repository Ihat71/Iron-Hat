from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.crud.workout_logs import (create_workout_log, 
        update_workout_log, delete_workout_log, get_workout_log, 
        get_user_workout_logs, get_user_workout_logs_by_program, 
        get_all_user_workout_logs, get_user_workout_logs_by_value,
        )
from backend.crud.workout_templates import get_workout_template
from backend.crud.program_templates import get_program
from backend.models.user import User
from backend.models.workout_logs import WorkoutLog
from backend.schemas.workout_logs import WorkoutLogCreate, WorkoutLogUpdate, SearchLogs
from backend.models.workout_log_exercises import WorkoutLogExercise
from typing import Any

def is_valid(db: Session, user: User, workout_id: int, program_id: int):
    workout = get_workout_log(program_id, workout_id, db, user)
    if workout:
        program = get_program(db, workout.program_id)
    else:
        return False

    if program.user_id != user.id:
        return False
   
    return True

def add_workout_log_service(db: Session, data: WorkoutLogCreate, program_id: int, user: User):
    template = get_workout_template(db, data.workout_template_id, program_id)
    if not template:
        data.workout_template_id = None
    create_data = WorkoutLog(
        program_id = program_id,
        workout_template_id = data.workout_template_id,
        notes = data.notes
    )
    for exercise in data.exercises:
        exercise_data = WorkoutLogExercise(**exercise.model_dump())
        create_data.exercises.append(exercise_data)
    
    return create_workout_log(db, create_data)


def get_workout_log_service(program_id: int, workout_id: int, db: Session, user: User):
    log = get_workout_log(program_id, workout_id, db, user)
    if not log:
        raise ValueError("There was an error: cant access or doesn't exist")

def get_workout_log_by_value_service(db: Session, type: str, value: Any, program_id: int, user: User):
    return get_user_workout_logs_by_value(db, type, value, program_id, user.id)

def get_all_workout_logs_service(db: Session, program_id: int, user: User):
    return get_all_user_workout_logs(db, program_id)

def get_workout_logs_service(db: Session, program_id: int, user: User):
    return get_user_workout_logs_by_program(db, user.id, program_id)

def update_workout_log_service(db: Session, data: WorkoutLogUpdate, workout_id: int, program_id: int, user: User):
    if not is_valid(db, user, workout_id, program_id):
        raise ValueError("cant access that")
    
    return update_workout_log(db, workout_id, data)

def delete_workout_log_service(program_id: int, workout_id: int, db: Session, user: User):
    if not is_valid(db, user, workout_id, program_id):
        raise ValueError("cant access that")
    
    return delete_workout_log(db, workout_id)