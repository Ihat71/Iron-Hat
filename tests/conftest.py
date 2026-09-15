"""
Shared pytest fixtures for the whole suite.

Read this file first if you're new here -- everything else in tests/
builds on top of what's defined here. The big ideas:

1. Tests run against a REAL disposable Postgres database (not sqlite),
   because a couple of models use Postgres-only column types (JSONB).
   The database is created once per test session and dropped afterwards.

2. Every individual test gets its own SQLAlchemy transaction that is
   rolled back at the end of the test, even though the application code
   under test calls `db.commit()` internally. This is the standard
   "nested savepoint" pattern -- see `db_session` below. It means tests
   never leak data into each other and never need manual cleanup.

3. `client` gives you an httpx AsyncClient wired up to the FastAPI app
   with its `get_db` dependency swapped out for the same transactional
   session `db_session` uses, so what you set up via the ORM is visible
   to the API call, and vice versa.

4. `register_user` / `auth_client` give you a ready-made authenticated
   user so most endpoint tests don't need to re-implement register+login.
"""

from collections.abc import AsyncIterator
from urllib.parse import urlsplit, urlunsplit

import psycopg
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Importing backend.models (not just backend.core.database) ensures every
# model class is registered on Base.metadata before we call create_all().
import backend.models  # noqa: F401
from backend.core.config import config
from backend.core.database import Base, get_db
from backend.core.hashing import hash_password
from backend.main import app
from backend.models.user import User

# ---------------------------------------------------------------------------
# Test database bootstrap: derive `<original_db>_test` from the configured
# DATABASE_URL and manage its lifecycle for the whole test session.
# ---------------------------------------------------------------------------


def _with_db_name(url: str, db_name: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, f"/{db_name}", parts.query, parts.fragment))


_source_db_name = urlsplit(config.database_url).path.lstrip("/")
TEST_DB_NAME = f"{_source_db_name}_test"
TEST_DATABASE_URL = _with_db_name(config.database_url, TEST_DB_NAME)

# psycopg's synchronous driver understands the plain "postgresql://" scheme;
# SQLAlchemy's "+psycopg" suffix is only meaningful to SQLAlchemy itself.
_MAINTENANCE_URL = _with_db_name(config.database_url, "postgres").replace(
    "postgresql+psycopg://", "postgresql://"
)


@pytest.fixture(scope="session", autouse=True)
def _test_database() -> None:
    """Create a scratch database for this test run and drop it afterwards.

    Runs against the "postgres" maintenance database with autocommit,
    since CREATE/DROP DATABASE can't run inside a transaction block.
    """
    with psycopg.connect(_MAINTENANCE_URL, autocommit=True) as conn:
        conn.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}" WITH (FORCE)')
        conn.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')

    yield

    with psycopg.connect(_MAINTENANCE_URL, autocommit=True) as conn:
        conn.execute(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}" WITH (FORCE)')


@pytest_asyncio.fixture(scope="session")
async def _engine():
    engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(_engine) -> AsyncIterator[AsyncSession]:
    """A session bound to one connection + outer transaction per test.

    App code is free to call `await db.commit()` -- because the session is
    configured with join_transaction_mode="create_savepoint", a commit
    inside the test only releases a SAVEPOINT, not the outer transaction.
    We roll that outer transaction back when the test ends, so nothing
    written during the test persists to the next one.
    """
    connection = await _engine.connect()
    outer_transaction = await connection.begin()

    session_factory = async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        autoflush=False,
        join_transaction_mode="create_savepoint",
    )
    session = session_factory()

    try:
        yield session
    finally:
        await session.close()
        await outer_transaction.rollback()
        await connection.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    """An httpx AsyncClient that talks to the FastAPI app in-process."""

    async def _override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.pop(get_db, None)


# ---------------------------------------------------------------------------
# User / auth helpers
# ---------------------------------------------------------------------------

DEFAULT_PASSWORD = "correct-horse-battery-staple"


def make_user_payload(**overrides) -> dict:
    """A valid /auth/register payload. Pass overrides to tweak specific fields."""
    payload = {
        "full_name": "Test Lifter",
        "username": "test_lifter",
        "email": "test.lifter@example.com",
        "gender": "male",
        "password": DEFAULT_PASSWORD,
    }
    payload.update(overrides)
    return payload


@pytest_asyncio.fixture
async def db_user(db_session: AsyncSession) -> User:
    """A persisted User row, created directly through the ORM (no HTTP)."""
    user = User(
        full_name="Direct DB User",
        username="direct_db_user",
        email="direct.db.user@example.com",
        hashed_password=hash_password(DEFAULT_PASSWORD),
        gender="female",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    """A client that has already registered a user and carries a bearer token.

    Exposes the registered user's payload (plus its db `id`, since UserRead
    doesn't expose one) as `client.registered_user` in case a test needs it.
    """
    from backend.crud.user import get_user_by_username

    payload = make_user_payload()

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201, register_response.text

    login_response = await client.post(
        "/auth/token",
        data={"username": payload["username"], "password": payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"

    user = await get_user_by_username(db_session, payload["username"])
    client.registered_user = {**payload, "id": user.id}

    yield client
