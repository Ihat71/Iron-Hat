"""
Tests for backend/crud/user.py, talking to the ORM directly through the
`db_session` fixture -- no HTTP layer involved. This is the layer to test
when you want to check exact query behavior (filters, uniqueness, etc.)
without also depending on routers/services/schemas being wired up right.

Compare with tests/api/test_auth_api.py, which tests the same user-creation
flow but through the actual HTTP endpoints.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.hashing import hash_password
from backend.crud.user import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    get_users,
    update_user,
)
from backend.models.user import User
from backend.schemas.user import UserUpdate


def _build_user(**overrides) -> User:
    defaults = dict(
        full_name="Ada Lovelace",
        username="ada",
        email="ada@example.com",
        hashed_password=hash_password("password123"),
        gender="female",
    )
    defaults.update(overrides)
    return User(**defaults)


async def test_create_user_persists_and_returns_it_with_an_id(db_session: AsyncSession):
    user = await create_user(db_session, _build_user())

    assert user.id is not None
    assert user.username == "ada"


async def test_get_user_by_id_returns_the_matching_user(db_session: AsyncSession):
    created = await create_user(db_session, _build_user())

    found = await get_user_by_id(db_session, created.id)

    assert found is not None
    assert found.id == created.id


async def test_get_user_by_id_returns_none_for_a_missing_id(db_session: AsyncSession):
    found = await get_user_by_id(db_session, 999_999)

    assert found is None


async def test_get_user_by_email_is_case_exact(db_session: AsyncSession):
    await create_user(db_session, _build_user(email="ada@example.com"))

    assert await get_user_by_email(db_session, "ada@example.com") is not None
    assert await get_user_by_email(db_session, "nobody@example.com") is None


async def test_get_user_by_username_finds_the_right_user(db_session: AsyncSession):
    await create_user(db_session, _build_user(username="ada"))
    await create_user(
        db_session, _build_user(username="grace", email="grace@example.com")
    )

    found = await get_user_by_username(db_session, "grace")

    assert found is not None
    assert found.username == "grace"


async def test_get_users_returns_every_user(db_session: AsyncSession):
    await create_user(db_session, _build_user(username="ada"))
    await create_user(
        db_session, _build_user(username="grace", email="grace@example.com")
    )

    users = await get_users(db_session)

    assert {u.username for u in users} == {"ada", "grace"}


async def test_update_user_applies_only_the_fields_that_were_set(db_session: AsyncSession):
    created = await create_user(db_session, _build_user())

    updated = await update_user(db_session, created.id, UserUpdate(full_name="Ada, Countess of Lovelace"))

    assert updated.full_name == "Ada, Countess of Lovelace"
    # untouched fields should survive the partial update
    assert updated.username == "ada"
    assert updated.email == "ada@example.com"


async def test_update_user_returns_none_for_a_missing_id(db_session: AsyncSession):
    result = await update_user(db_session, 999_999, UserUpdate(full_name="Nobody"))

    assert result is None


async def test_delete_user_removes_the_row_and_returns_true(db_session: AsyncSession):
    created = await create_user(db_session, _build_user())

    deleted = await delete_user(db_session, created.id)

    assert deleted is True
    assert await get_user_by_id(db_session, created.id) is None


async def test_delete_user_returns_false_for_a_missing_id(db_session: AsyncSession):
    deleted = await delete_user(db_session, 999_999)

    assert deleted is False


async def test_duplicate_username_is_rejected_at_the_database_level(db_session: AsyncSession):
    # The `username` column is declared unique=True in the model -- this
    # confirms the database actually enforces it (application-level checks
    # like in auth_service are a second line of defense, tested separately
    # in tests/api/test_auth_api.py).
    await create_user(db_session, _build_user(username="ada"))

    with pytest.raises(Exception):
        await create_user(
            db_session, _build_user(username="ada", email="different@example.com")
        )
