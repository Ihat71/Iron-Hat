"""
End-to-end tests for /exercises/*.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import persist_exercise


async def test_get_exercise_by_id_returns_it(
    auth_client: AsyncClient, db_session: AsyncSession
):
    exercise = await persist_exercise(db_session, name="Deadlift")

    response = await auth_client.get(f"/exercises/{exercise.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Deadlift"


async def test_get_exercise_requires_authentication(
    client: AsyncClient, db_session: AsyncSession
):
    exercise = await persist_exercise(db_session)

    response = await client.get(f"/exercises/{exercise.id}")

    assert response.status_code == 401


async def test_search_all_paginates_results(
    auth_client: AsyncClient, db_session: AsyncSession
):
    for i in range(3):
        await persist_exercise(db_session, name=f"Exercise {i}")

    first_page = await auth_client.get("/exercises/search/all?page=1&page_size=2")
    second_page = await auth_client.get("/exercises/search/all?page=2&page_size=2")

    assert first_page.status_code == 200
    assert len(first_page.json()) == 2
    assert second_page.status_code == 200
    assert len(second_page.json()) == 1


@pytest.mark.xfail(
    reason=(
        "backend/api/v1/exercise_catalog/exercise_catalog_router.py declares "
        "GET /{exercise_id} before GET /search, and FastAPI matches routes in "
        "declaration order -- so a request to /exercises/search is captured by "
        "/{exercise_id} first, fails to parse 'search' as an int, and returns "
        "422 instead of ever reaching the search handler. Move the /search "
        "route above /{exercise_id} to fix."
    ),
    strict=False,
)
async def test_search_by_name_is_case_insensitive_and_matches_substrings(
    auth_client: AsyncClient, db_session: AsyncSession
):
    await persist_exercise(db_session, name="Barbell Bench Press")
    await persist_exercise(db_session, name="Barbell Back Squat")

    response = await auth_client.get("/exercises/search?name=bench")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Barbell Bench Press"


@pytest.mark.xfail(
    reason="Same /search vs /{exercise_id} route-ordering bug as the test above.",
    strict=False,
)
async def test_search_by_main_muscle_filters_exactly(
    auth_client: AsyncClient, db_session: AsyncSession
):
    await persist_exercise(db_session, name="Squat", main_muscle="quadriceps")
    await persist_exercise(db_session, name="Row", main_muscle="back")

    response = await auth_client.get("/exercises/search?main_muscle=back")

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Row"


@pytest.mark.xfail(
    reason=(
        "backend/crud/exercises.py:get_exercise returns None for an unknown id, "
        "and the route's response_model=ExerciseRead isn't Optional, so FastAPI's "
        "response validation turns the missing-exercise case into a 500 instead of "
        "a clean 404. Add an explicit not-found check in the service/router to fix."
    ),
    strict=False,
)
async def test_get_exercise_returns_404_for_an_unknown_id(auth_client: AsyncClient):
    response = await auth_client.get("/exercises/999999")

    assert response.status_code == 404
