from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from crud.exercises import (
    get_exercise,get_all_exercises,parameter_search

)
from models.user import User
from models.exercises import Exercises
from schemas.exercises import ExerciseSearch

def get_exercise_service(exercise_id: int, db: Session, current_user: User):
    get_exercise(exercise_id, db)

def get_all_exercises_service(page: int, page_size: int, db: Session, current_user: User):
    return get_all_exercises(page, page_size, db)

def parameter_search_exercises_service(
        search: ExerciseSearch,
        db: Session, 
        current_user: User):


    return parameter_search(search, db)