from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from backend.models.user import User
from backend.models.personal_records import PersonalRecords
from backend.schemas.personal_records import PersonalRecordCreate, PersonalRecordUpdate, SearchPR
from typing import Any
from backend.core.enums import PRType


async def create_personal_records(db: AsyncSession, record_data: PersonalRecordCreate, user: User) -> PersonalRecords:
    record = PersonalRecords(user_id=user.id, **record_data.model_dump())

    db.add(record)
    await db.commit()
    await db.refresh(record)

    return record

async def get_pr(record_id: int, db: AsyncSession, user: User):
    stmt = select(PersonalRecords).where(
    PersonalRecords.user_id==user.id,
    PersonalRecords.id == record_id
    )

    return await db.scalar(stmt)

async def get_max_pr(exercise_id: int, pr_type: PRType, db: AsyncSession, user: User):
    stmt = select(PersonalRecords).where(
        PersonalRecords.user_id == user.id,
        PersonalRecords.exercise_id == exercise_id,
        PersonalRecords.pr_type == pr_type
    ).order_by(desc(PersonalRecords.top_weight)).limit(1)


    return await db.scalar(stmt)

async def search_prs(search_data: dict[str, Any], db: AsyncSession, user: User):
    stmt = select(PersonalRecords).where(PersonalRecords.user_id == user.id)

    for key, value in search_data.items():
        column = getattr(PersonalRecords, key)
        stmt = stmt.where(column == value)

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_prs_by_params(params: dict[str, Any], db: AsyncSession, user: User):
    stmt = select(PersonalRecords).where(PersonalRecords.user_id == user.id)

    if params['exercise_id'] is not None:
        stmt.where(PersonalRecords.exercise_id == params['exercise_id'])

    if params['pr_type'] is not None:
        stmt.where(PersonalRecords.pr_type == params['pr_type'])

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_pr_history(exercises: list[int], db: AsyncSession, current_user: User):
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

    result = await db.execute(stmt)
    return result.scalars().all()

async def get_pr_count(days_ago: int, db: AsyncSession, user: User):
    cutoff = datetime.now() - timedelta(days=days_ago)
    stmt = select(func.count(PersonalRecords.id)).where(
        PersonalRecords.user_id == user.id,
        PersonalRecords.date >= cutoff
    )

    return await db.scalar(stmt)


async def delete_personal_record(db: AsyncSession, record_id: int) -> bool:
    record = await db.get(PersonalRecords, record_id)

    if record is None:
        return False

    await db.delete(record)
    await db.commit()

    return True
