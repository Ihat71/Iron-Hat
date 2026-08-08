from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.crud.personal_records import (
    create_personal_records,

)
from backend.crud.personal_records import *
from backend.models.user import User
from backend.models.personal_records import PersonalRecords
from backend.models.exercise_history import ExerciseHistory
from backend.schemas.personal_records import PersonalRecordCreate, PersonalRecordUpdate
from typing import Any

def add_pr_service(data: PersonalRecordCreate, db: Session, user: User):
    params = {"exercise_id": data.exercise_id,'pr_type': data.pr_type}

    max_record = get_max_pr(params, db, user)


    if data.top_weight >= max_record:
        return create_personal_records(db, data)
    else:
        raise ValueError("you have stronger lifts than this")


def get_pr_history_service(db: Session, user: User):
    params = {}

    return get_prs_by_params(params, db, user)

def get_pr_history_by_exercise_and_pr_type_service(exercise_id: int, pr_type: str, db: Session, user: User):
    params = {'exercise_id': exercise_id, 'pr_type': pr_type}

    return get_prs_by_params(params, db, user)

def get_pr_history_by_exercise_service(exercise_id: int, db: Session, user: User):
    params = {'exercise_id': exercise_id}

    return get_prs_by_params(params, db, user)

def get_pr_history_by_pr_type_service(pr_type: str, db: Session, user: User):
    params = {'pr_type': pr_type}

    return get_prs_by_params(params, db, user)

#so pr history gets all prs from the past and present while normal get_prs
#get the max prs of the present. Both are based on parameters
def get_prs_by_exercise_service(exercise_id: int, db: Session, user: User):
    params = {'exercise_id': exercise_id}

    return get_max_pr(params, db, user)

def get_pr_by_exercise_and_type_service(exercise_id: int, pr_type: str, db: Session, user: User):
    params = {'exercise_id': exercise_id, 'pr_type': pr_type}

    return get_max_pr(params, db, user)


def delete_pr_service(record_id: int, db: Session, user: User):
    record = get_pr(record_id, db)
    if record.user_id != user.id:
        raise ValueError("cant delete that, authorization issue")
    return delete_personal_record(db, record_id)