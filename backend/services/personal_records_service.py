from sqlalchemy import select
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
from backend.core.enums import ExType, PRType

reps_map = {
    1: "1rm",
    2: "2rm",
    5: "5rm"
}

def add_pr_service(data: PersonalRecordCreate, db: Session, user: User):

    max_record = get_max_pr(data.exercise_id, data.pr_type, db, user)


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

def check_and_add_pr_service(record: PersonalRecordCreate,exercise_type: str,db: Session,user: User) -> None:

    # Determine which PR types this set can qualify for.
    pr_type_list = []

    if exercise_type != ExType.BODYWEIGHT:
        for reps, pr_type in reps_map.items():
            if record.reps is not None and reps <= record.reps:
                pr_type_list.append(pr_type)
    else:
        pr_type_list.append(PRType.BODYWEIGHT)

    if not pr_type_list:
        return

    for pr_type in pr_type_list:

        # Because PR history is monotonic, the latest PR is
        # also the greatest PR for this user/exercise/type.
        
        latest_pr = get_max_pr(record.exercise_id, pr_type, db, user)

        # No previous PR -> establish the base PR.
        if latest_pr is None:
            should_add = True

        # Existing PR -> only add if strictly better.
        else:
            should_add = record.top_weight > latest_pr.top_weight

        if not should_add:
            continue

        # Do not mutate `record`.
        # The PR type itself describes the rep count for weighted PRs.
        pr_reps = (
            record.reps
            if pr_type == PRType.BODYWEIGHT
            else None
        )

        new_record = PersonalRecords(
            user_id=user.id,
            exercise_id=record.exercise_id,
            exercise_history_id=record.exercise_history_id,
            pr_type=pr_type,
            top_weight=record.top_weight,
            reps=pr_reps,
            notes=record.notes,
            date=record.date,
        )

        db.add(new_record)

        # Make the newly-created PR visible to subsequent queries
        # in this transaction.
        db.flush()

    




def delete_pr_service(record_id: int, db: Session, user: User):
    record = get_pr(record_id, db, user)
    if not record:
        raise ValueError("Could not find that record")

    return delete_personal_record(db, record_id)