from sqlalchemy import select, desc, func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.models.user import User
from backend.models.personal_records import PersonalRecords
from backend.schemas.personal_records import PersonalRecordCreate, PersonalRecordUpdate


def create_personal_records(db: Session, record_data: PersonalRecordCreate) -> PersonalRecords:
    record = PersonalRecords(**record_data.model_dump())

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

def get_pr(record_id: int, db: Session):
    return db.get(PersonalRecords, record_id)

def get_max_pr(params: dict, db: Session, user: User):
    stmt = select(PersonalRecords).where(
        PersonalRecords.user_id == user.id
    )

    if params['exercise_id'] is not None:
        stmt.where(PersonalRecords.exercise_id == params['exercise_id'])

    if params['pr_type'] is not None:
        stmt.where(PersonalRecords.pr_type == params['pr_type'])

    stmt = stmt.order_by(desc(PersonalRecords.top_weight))

    return db.execute(stmt).scalars().first()

def get_prs_by_params(params: dict, db: Session, user: User):
    stmt = select(PersonalRecords).where(PersonalRecords.user_id == user.id)

    if params['exercise_id'] is not None:
        stmt.where(PersonalRecords.exercise_id == params['exercise_id'])

    if params['pr_type'] is not None:
        stmt.where(PersonalRecords.pr_type == params['pr_type'])

    return db.execute(stmt).scalars().all()

def get_pr_history(exercises: list[int], db: Session, current_user: User):
    stmt = select(
        PersonalRecords.id,
        PersonalRecords.top_weight,
        PersonalRecords.pr_type,
        PersonalRecords.date,
        PersonalRecords.created_at
    ).where(
        PersonalRecords.user_id == current_user.id,
        PersonalRecords.exercise_id.in_(exercises)
    )

    return db.execute(stmt).scalars().all()

def get_pr_count(days_ago: int, db: Session, user: User):
    cutoff = datetime.now() - timedelta(days=days_ago)
    stmt = select(func.count(PersonalRecords.id)).where(
        PersonalRecords.user_id == user.id,
        PersonalRecords.date >= cutoff
    )

    return db.scalar(stmt)


def delete_personal_record(db: Session, record_id: int) -> bool:
    record = db.get(PersonalRecords, record_id)

    if record is None:
        return False

    db.delete(record)
    db.commit()

    return True