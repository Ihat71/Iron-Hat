from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.crud.workout_templates import create_workout_template, update_workout_template, delete_workout_template, get_workout_template, get_user_workout_templates, get_user_workout_template_by_value, get_all_user_workout_templates
from backend.crud.program_templates import get_program
from backend.models.user import User
from backend.models.workout_templates import WorkoutTemplate
from backend.schemas.workout_templates import WorkoutTemplateCreate, WorkoutTemplateUpdate
from typing import Any

def is_valid(db: Session, user_id, workout_id):
    workout = get_workout_template(db, workout_id)
    program = get_program(db, workout.program_id)

    if program.user_id != user_id:
        return False
   
    return True

def add_workout_template_service(db: Session, data: WorkoutTemplateCreate, program_id: int, user: User):
    program = get_program(db, program_id)

    if program.user_id != user.id:
        raise ValueError("cannot access that")
    
    data = WorkoutTemplate(
        program_id = program_id,
        day_number = data.day_number,
        workout_type = data.workout_type
    )
    return create_workout_template(db, data)

# def get_workout_templates_by_program_service(db: Session, user: User, program_id: int):
#     return get_user_workout_template_by_value(db, user.id, "program_id", program_id)

# def get_workout_templates_by_day_service(db: Session, user: User, day: int):
#     return get_user_workout_template_by_value(db, user.id, "day_number", day)

# def get_workout_templates_by_type_service(db: Session, user: User, type: str):
#     return get_user_workout_template_by_value(db, user.id, "workout_type", type)

def get_workout_template_by_value_service(db: Session, type: str, value: Any, program_id: int, user: User):
    return get_user_workout_template_by_value(db, type, value, program_id, user.id)

def get_all_workout_templates_service(db: Session, user: User):
    return get_all_user_workout_templates(db, user.id)

def get_workout_templates_service(db: Session, program_id: int, user: User):
    return get_user_workout_templates(db, user.id, program_id)

def update_workout_template_service(db: Session, data: WorkoutTemplateUpdate, workout_id: int, user: User):
    if not is_valid(db, user.id, workout_id):
        raise ValueError("cant access that")
    
    return update_workout_template(db, workout_id, data)

def delete_workout_template_service(db: Session, user: User, workout_id: int):
    if not is_valid(db, user.id, workout_id):
        raise ValueError("cant access that")
    
    return delete_workout_template(db, workout_id)