"""
Tests for backend/crud/user_biometrics.py.

These demonstrate the pattern for testing "belongs to a user" data: build a
user with the `db_user` fixture from conftest.py, then create rows scoped
to it and check the CRUD functions only ever see/touch that user's data.
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.user_biometrics import (
    add_bio,
    delete_bio,
    get_bio,
    get_bio_history,
    get_recent_bio_history,
    update_bio,
)
from backend.models.user import User
from backend.schemas.user_biometrics import BiometricCreate, BiometricUpdate


async def test_add_bio_associates_the_entry_with_the_given_user(
    db_session: AsyncSession, db_user: User
):
    bio = await add_bio(BiometricCreate(weight=82.5), db_session, db_user)

    assert bio.id is not None
    assert bio.user_id == db_user.id
    assert bio.weight == 82.5


async def test_get_bio_history_only_returns_rows_for_that_user(
    db_session: AsyncSession, db_user: User
):
    other_user = User(
        full_name="Other User",
        username="other_user",
        email="other.user@example.com",
        hashed_password=db_user.hashed_password,
        gender="male",
    )
    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)

    await add_bio(BiometricCreate(weight=80), db_session, db_user)
    await add_bio(BiometricCreate(weight=70), db_session, other_user)

    history = await get_bio_history(db_session, db_user)

    assert len(history) == 1
    assert history[0].user_id == db_user.id


async def test_get_recent_bio_history_returns_the_most_recently_recorded_entry(
    db_session: AsyncSession, db_user: User
):
    now = datetime.now(timezone.utc)

    await add_bio(
        BiometricCreate(weight=80, recorded_at=now - timedelta(days=7)),
        db_session,
        db_user,
    )
    latest = await add_bio(
        BiometricCreate(weight=79, recorded_at=now),
        db_session,
        db_user,
    )

    recent = await get_recent_bio_history(db_session, db_user)

    assert recent.id == latest.id
    assert recent.weight == 79


async def test_update_bio_only_changes_fields_that_were_provided(
    db_session: AsyncSession, db_user: User
):
    bio = await add_bio(BiometricCreate(weight=80, notes="baseline"), db_session, db_user)

    updated = await update_bio(bio, BiometricUpdate(weight=78.5), db_session)

    assert updated.weight == 78.5
    assert updated.notes == "baseline"  # untouched


async def test_delete_bio_removes_the_row(db_session: AsyncSession, db_user: User):
    bio = await add_bio(BiometricCreate(weight=80), db_session, db_user)

    result = await delete_bio(bio, db_session)

    assert result is True
    assert await get_bio(bio.id, db_session) is None
