from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from crud.workout_logs import create_workout_log, update_workout_log, delete_workout_log, get_workout_log, get_user_workout_logs, get_user_workout_logs_by_program, get_all_user_workout_logs, get_user_workout_logs_by_value
from crud.program_templates import get_program
from models.user import User
from models.workout_logs import WorkoutLog
from schemas.workout_logs import WorkoutLogCreate, WorkoutLogUpdate
from typing import Any

def is_valid(db: Session, user_id, workout_id):
    workout = get_workout_log(db, workout_id)
    program = get_program(db, workout.program_id)

    if program.user_id != user_id:
        return False
   
    return True

def add_workout_log_service(db: Session, data: WorkoutLogCreate, program_id: int, user: User):
    program = get_program(db, program_id)

    if program.user_id != user.id:
        raise ValueError("cannot access that")
    
    data = WorkoutLog(
        program_id = program_id,
        day_number = data.day_number,
        workout_type = data.workout_type
    )
    return create_workout_log(db, data)

def get_workout_log_by_value_service(db: Session, type: str, value: Any, program_id: int, user: User):
    return get_user_workout_logs_by_value(db, type, value, program_id, user.id)

def get_all_workout_logs_service(db: Session, user: User):
    return get_all_user_workout_logs(db, user.id)

def get_workout_logs_service(db: Session, program_id: int, user: User):
    return get_user_workout_logs_by_program(db, user.id, program_id)

def update_workout_log_service(db: Session, data: WorkoutLogUpdate, workout_id: int, user: User):
    if not is_valid(db, user.id, workout_id):
        raise ValueError("cant access that")
    
    return update_workout_log(db, workout_id, data)

def delete_workout_log_service(db: Session, user: User, workout_id: int):
    if not is_valid(db, user.id, workout_id):
        raise ValueError("cant access that")
    
    return delete_workout_log(db, workout_id)