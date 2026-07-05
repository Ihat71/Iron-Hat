from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.personal_records import PersonalRecords
from backend.schemas.personal_records import PersonalRecordCreate, PersonalRecordUpdate


def create_personal_records(db: Session, workout_data: PersonalRecordCreate) -> PersonalRecords:
    workout = PersonalRecords(**workout_data.model_dump())

    db.add(workout)
    db.commit()
    db.refresh(workout)

    return workout

def get_user_personal_records(db: Session, user_id: int) -> list[PersonalRecords]:
    stmt = select(PersonalRecords).where(PersonalRecords.user_id == user_id)
    return db.execute(stmt).scalars().all()


def get_user_personal_records_by_type(db: Session, user_id: int, workout_type: str) -> list[PersonalRecords]:

    stmt = select(PersonalRecords).where(PersonalRecords.user_id == user_id, PersonalRecords.workout_type == workout_type)
    return db.execute(stmt).scalars().all()


def update_personal_records(db: Session, workout_id: int, pr_data: PersonalRecordUpdate) -> PersonalRecords | None:
    workout = db.get(PersonalRecords, workout_id)

    if workout is None:
        return None

    update_data = pr_data.model_dump(exclude_unset=True, exclude={"id"})

    for field, value in update_data.items():
        setattr(workout, field, value)

    db.commit()
    db.refresh(workout)

    return workout


def delete_personal_records(db: Session, workout_id: int) -> bool:
    workout = db.get(PersonalRecords, workout_id)

    if workout is None:
        return False

    db.delete(workout)
    db.commit()

    return True