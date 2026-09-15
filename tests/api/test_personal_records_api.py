"""
End-to-end tests for /personal-records.

Personal records need an exercise to point at, so these seed one directly
through the ORM (via `db_session`) before hitting the API -- a common
pattern once a resource has foreign keys: set up state with the ORM,
exercise behavior through HTTP.

Note: most of this router's success paths currently 500 instead of
returning real data, because `PersonalRecordRead` in
backend/schemas/personal_records.py declares `exercise_history_id`, `reps`
and `notes` as required (`int` / `str`) even though the matching model
columns are nullable -- so any record created without those fields fails
FastAPI's response validation. The two `xfail`s below are regression tests
for that; see tests/crud/test_personal_records_crud.py for coverage of the
actual create/search/filter logic that doesn't depend on this route
working end-to-end.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import persist_exercise

_SCHEMA_BUG_REASON = (
    "backend/schemas/personal_records.py:PersonalRecordRead declares "
    "exercise_history_id/reps/notes as required even though the "
    "PersonalRecords model allows them to be NULL, so FastAPI's response "
    "validation 500s on any record created without those fields. Make the "
    "three fields Optional in the schema to fix."
)


async def test_create_pr_requires_authentication(client: AsyncClient, db_session: AsyncSession):
    exercise = await persist_exercise(db_session)

    response = await client.post(
        "/personal-records",
        json={"exercise_id": exercise.id, "pr_type": "1rm", "top_weight": 100},
    )

    assert response.status_code == 401


@pytest.mark.xfail(reason=_SCHEMA_BUG_REASON, strict=False)
async def test_create_pr_returns_201_for_a_first_time_record(
    auth_client: AsyncClient, db_session: AsyncSession
):
    exercise = await persist_exercise(db_session)

    response = await auth_client.post(
        "/personal-records",
        json={"exercise_id": exercise.id, "pr_type": "1rm", "top_weight": 100},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["top_weight"] == 100
    assert body["pr_type"] == "1rm"


@pytest.mark.xfail(reason=_SCHEMA_BUG_REASON, strict=False)
async def test_search_with_no_filters_returns_every_pr_for_the_current_user(
    auth_client: AsyncClient, db_session: AsyncSession
):
    exercise = await persist_exercise(db_session)
    await auth_client.post(
        "/personal-records",
        json={"exercise_id": exercise.id, "pr_type": "1rm", "top_weight": 100},
    )

    response = await auth_client.request("GET", "/personal-records", json={})

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.xfail(
    reason=(
        "backend/services/personal_records_service.py:get_pr_service is missing "
        "a `return`, so it always sends back `None`, which fails response_model "
        "validation and yields a 500 instead of the PR. Fix the service, then "
        "this test should start passing -- flip it to a plain assertion at that point."
    ),
    strict=False,
)
async def test_get_single_pr_returns_the_record(
    auth_client: AsyncClient, db_session: AsyncSession
):
    exercise = await persist_exercise(db_session)
    created = await auth_client.post(
        "/personal-records",
        json={"exercise_id": exercise.id, "pr_type": "1rm", "top_weight": 100},
    )
    record_id = created.json()["id"]

    response = await auth_client.get(f"/personal-records/{record_id}")

    assert response.status_code == 200
    assert response.json()["id"] == record_id
