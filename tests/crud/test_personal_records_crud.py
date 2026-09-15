"""
Tests for backend/crud/personal_records.py.

Personal records reference an exercise, so these use the
`persist_exercise` factory from tests/factories.py to satisfy the
foreign key instead of hand-rolling an Exercises row in every test.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.enums import PRType
from backend.crud.personal_records import (
    create_personal_records,
    delete_personal_record,
    get_max_pr,
    get_pr,
)
from backend.models.user import User
from backend.schemas.personal_records import PersonalRecordCreate
from tests.factories import persist_exercise


async def test_create_personal_records_associates_user_and_exercise(
    db_session: AsyncSession, db_user: User
):
    exercise = await persist_exercise(db_session)

    record = await create_personal_records(
        db_session,
        PersonalRecordCreate(exercise_id=exercise.id, pr_type=PRType.ONE_RM, top_weight=100),
        db_user,
    )

    assert record.id is not None
    assert record.user_id == db_user.id
    assert record.exercise_id == exercise.id
    assert record.top_weight == 100


async def test_get_pr_only_matches_the_owning_user(db_session: AsyncSession, db_user: User):
    exercise = await persist_exercise(db_session)
    other_user = User(
        full_name="Other Lifter",
        username="other_lifter",
        email="other.lifter@example.com",
        hashed_password=db_user.hashed_password,
        gender="male",
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)

    record = await create_personal_records(
        db_session,
        PersonalRecordCreate(exercise_id=exercise.id, pr_type=PRType.ONE_RM, top_weight=100),
        db_user,
    )

    assert await get_pr(record.id, db_session, db_user) is not None
    assert await get_pr(record.id, db_session, other_user) is None


async def test_get_max_pr_returns_the_heaviest_record_for_that_type(
    db_session: AsyncSession, db_user: User
):
    exercise = await persist_exercise(db_session)

    await create_personal_records(
        db_session,
        PersonalRecordCreate(exercise_id=exercise.id, pr_type=PRType.ONE_RM, top_weight=100),
        db_user,
    )
    heaviest = await create_personal_records(
        db_session,
        PersonalRecordCreate(exercise_id=exercise.id, pr_type=PRType.ONE_RM, top_weight=140),
        db_user,
    )

    max_pr = await get_max_pr(exercise.id, PRType.ONE_RM, db_session, db_user)

    assert max_pr.id == heaviest.id


async def test_get_max_pr_does_not_mix_pr_types(db_session: AsyncSession, db_user: User):
    exercise = await persist_exercise(db_session)

    await create_personal_records(
        db_session,
        PersonalRecordCreate(exercise_id=exercise.id, pr_type=PRType.FIVE_RM, top_weight=200),
        db_user,
    )

    max_pr = await get_max_pr(exercise.id, PRType.ONE_RM, db_session, db_user)

    assert max_pr is None


async def test_delete_personal_record_removes_it(db_session: AsyncSession, db_user: User):
    exercise = await persist_exercise(db_session)
    record = await create_personal_records(
        db_session,
        PersonalRecordCreate(exercise_id=exercise.id, pr_type=PRType.ONE_RM, top_weight=100),
        db_user,
    )

    deleted = await delete_personal_record(db_session, record.id)

    assert deleted is True
    assert await get_pr(record.id, db_session, db_user) is None


async def test_delete_personal_record_returns_false_for_a_missing_id(
    db_session: AsyncSession,
):
    assert await delete_personal_record(db_session, 999_999) is False
