from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.crud.personal_records import (
    create_personal_records,

)
from backend.crud.personal_records import get_pr, get_max_pr, delete_personal_record, get_prs_by_params, search_prs
from backend.models.user import User
from backend.models.personal_records import PersonalRecords
from backend.models.exercise_history import ExerciseHistory
from backend.schemas.personal_records import PersonalRecordCreate, PersonalRecordUpdate, SearchPR
from typing import Any

def add_pr_service(data: PersonalRecordCreate, db: Session, user: User):
    params = {"exercise_id": data.exercise_id,'pr_type': data.pr_type}

    max_record = get_max_pr(params, db, user)


    if not max_record or data.top_weight >= max_record.top_weight:
        return create_personal_records(db, data, user)
    else:
        raise ValueError("you have stronger lifts than this")

def get_pr_service(record_id: int, db: Session, user: User):
    get_pr(record_id, db, user)

def search_prs_service(data: SearchPR, db: Session, user: User):
    search_data = data.model_dump(exclude_unset=True)

    return search_prs(search_data, db, user)

def get_pr_history_service(db: Session, user: User):
    params = {}

    return get_prs_by_params(params, db, user)


#so pr history gets all prs from the past and present while normal get_prs
#get the max prs of the present. Both are based on parameters


def delete_pr_service(record_id: int, db: Session, user: User):
    record = get_pr(record_id, db, user)
    if not record:
        raise ValueError("Could not find that record")
    if record.user_id != user.id:
        raise ValueError("cant delete that, authorization issue")
    return delete_personal_record(db, record_id)