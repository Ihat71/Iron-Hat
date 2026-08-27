from backend.models.user import User
from sqlalchemy.orm import Session
from backend.crud.exercise_history import (create_exercise_history, get_exercise_history, 
    get_all_exercise_history, delete_exercise_history
    )
from backend.schemas.exercise_history import ExerciseHistoryCreate, ExerciseHistorySearch

def create_exercise_history_service(data: ExerciseHistoryCreate, db: Session, user: User):
    return create_exercise_history(db, data, user)

def get_exercise_history_service(history_id: int, db: Session, user: User):
    get_exercise_history(history_id, db, user)

def get_all_exercise_history_service(page: int, page_size: int, db: Session, user: User):
    offset = (page - 1) * page_size
    get_all_exercise_history(offset, page_size, db, user)

def parameter_search_exercise_history_service(search: ExerciseHistorySearch, db: Session, user: User):
    pass

def delete_exercise_history_service(history_id: int, db: Session, user: User):
    return delete_exercise_history(history_id, db, user)