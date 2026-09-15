"""
End-to-end tests for /biometrics/*.

Uses the `auth_client` fixture from conftest.py, which is a `client` that
has already registered + logged in a user and carries its bearer token --
grab that fixture whenever a route requires `get_current_user`.
"""

from httpx import AsyncClient


async def test_create_biometrics_entry_returns_201(auth_client: AsyncClient):
    response = await auth_client.post("/biometrics", json={"weight": 82.5})

    assert response.status_code == 201
    body = response.json()
    assert body["weight"] == 82.5
    assert body["id"] is not None


async def test_create_biometrics_entry_requires_authentication(client: AsyncClient):
    response = await client.post("/biometrics", json={"weight": 82.5})

    assert response.status_code == 401


async def test_history_lists_every_entry_for_the_current_user(auth_client: AsyncClient):
    await auth_client.post("/biometrics", json={"weight": 82.5})
    await auth_client.post("/biometrics", json={"weight": 81.0})

    response = await auth_client.get("/biometrics/history")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_history_is_empty_for_a_brand_new_user(auth_client: AsyncClient):
    response = await auth_client.get("/biometrics/history")

    assert response.status_code == 200
    assert response.json() == []


async def test_recent_returns_the_most_recently_recorded_entry(auth_client: AsyncClient):
    await auth_client.post(
        "/biometrics", json={"weight": 85.0, "recorded_at": "2024-01-01T00:00:00Z"}
    )
    await auth_client.post(
        "/biometrics", json={"weight": 80.0, "recorded_at": "2024-06-01T00:00:00Z"}
    )

    response = await auth_client.get("/biometrics/recent")

    assert response.status_code == 200
    assert response.json()["weight"] == 80.0


async def test_update_changes_only_the_given_fields(auth_client: AsyncClient):
    created = await auth_client.post(
        "/biometrics", json={"weight": 82.5, "notes": "before cut"}
    )
    bio_id = created.json()["id"]

    response = await auth_client.patch(f"/biometrics/{bio_id}", json={"weight": 80.0})

    assert response.status_code == 200
    body = response.json()
    assert body["weight"] == 80.0
    assert body["notes"] == "before cut"


async def test_delete_removes_the_entry(auth_client: AsyncClient):
    created = await auth_client.post("/biometrics", json={"weight": 82.5})
    bio_id = created.json()["id"]

    response = await auth_client.delete(f"/biometrics/{bio_id}")

    assert response.status_code == 200
    assert response.json() is True

    history = await auth_client.get("/biometrics/history")
    assert history.json() == []
