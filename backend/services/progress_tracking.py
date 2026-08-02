from sqlalchemy.orm import Session
from models.user import User
from crud.user_biometrics import get_weight_and_bf_history, get_bio_history
from crud.personal_records import get_pr_history
from crud.exercise_history import get_exercise_history_by_exercise


def get_weight_and_bf_history_service(db: Session, current_user: User):
    return get_weight_and_bf_history(db, current_user)

def get_pr_tracking_service(exercises: list[int], db: Session, current_user: User):
    return get_pr_history(exercises, db, current_user)

def get_exercise_history_service(exercise_id: int, db: Session, current_user: User):
    return get_exercise_history_by_exercise(exercise_id, db, current_user)

def get_extra_biometrics_service(db: Session, current_user: User):
    bio_history = get_bio_history(db, current_user)

    return bio_history

def get_workout_history_service(db: Session, current_user: User):
    """this func should return a count of workout logs for this month, how many were done properly according to the template, and how many were done and skipped in general."""
    pass

def get_tracking_summary(db: Session, current_user: User):
    """This func should return data for a simple weekly and monthly summary card that also features how consistent the user was and how much he grew,
    how many PRs he accomplished in various exercises and other stuff.
    """
    pass
