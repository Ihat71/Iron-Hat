"""
End-to-end tests for /auth/*, driven entirely through HTTP via the `client`
fixture (see conftest.py). This is the layer to test when you care about
status codes, response shapes, and how routes are wired together -- for
pure business-logic edge cases prefer a crud/ or unit/ test, which is
faster and easier to pinpoint.
"""

from httpx import AsyncClient

from tests.conftest import make_user_payload


async def test_register_returns_201_and_the_created_user(client: AsyncClient):
    response = await client.post("/auth/register", json=make_user_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "test_lifter"
    assert body["email"] == "test.lifter@example.com"
    # the password must never come back in a response
    assert "password" not in body
    assert "hashed_password" not in body


async def test_register_rejects_a_duplicate_username(client: AsyncClient):
    await client.post("/auth/register", json=make_user_payload())

    response = await client.post(
        "/auth/register",
        json=make_user_payload(email="someone.else@example.com"),
    )

    assert response.status_code == 409


async def test_register_rejects_a_duplicate_email(client: AsyncClient):
    await client.post("/auth/register", json=make_user_payload())

    response = await client.post(
        "/auth/register",
        json=make_user_payload(username="a_different_username"),
    )

    assert response.status_code == 409


async def test_register_rejects_an_invalid_email(client: AsyncClient):
    response = await client.post(
        "/auth/register", json=make_user_payload(email="not-an-email")
    )

    assert response.status_code == 422


async def test_login_returns_a_bearer_token_for_correct_credentials(client: AsyncClient):
    payload = make_user_payload()
    await client.post("/auth/register", json=payload)

    response = await client.post(
        "/auth/login",
        json={"username": payload["username"], "password": payload["password"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


async def test_login_rejects_a_wrong_password(client: AsyncClient):
    payload = make_user_payload()
    await client.post("/auth/register", json=payload)

    response = await client.post(
        "/auth/login",
        json={"username": payload["username"], "password": "wrong-password"},
    )

    assert response.status_code == 401


async def test_login_rejects_an_unknown_username(client: AsyncClient):
    response = await client.post(
        "/auth/login", json={"username": "ghost", "password": "whatever"}
    )

    assert response.status_code == 401


async def test_token_endpoint_supports_oauth2_form_login_for_swagger(client: AsyncClient):
    payload = make_user_payload()
    await client.post("/auth/register", json=payload)

    response = await client.post(
        "/auth/token",
        data={"username": payload["username"], "password": payload["password"]},
    )

    assert response.status_code == 200
    assert response.json()["access_token"]


async def test_me_returns_the_authenticated_users_profile(client: AsyncClient):
    payload = make_user_payload()
    await client.post("/auth/register", json=payload)
    login = await client.post(
        "/auth/token",
        data={"username": payload["username"], "password": payload["password"]},
    )
    token = login.json()["access_token"]

    response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == payload["username"]


async def test_me_requires_authentication(client: AsyncClient):
    response = await client.get("/auth/me")

    assert response.status_code == 401


async def test_me_rejects_a_garbage_token(client: AsyncClient):
    response = await client.get(
        "/auth/me", headers={"Authorization": "Bearer not-a-real-token"}
    )

    assert response.status_code == 401
