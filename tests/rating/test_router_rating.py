import pytest_asyncio


@pytest_asyncio.fixture()
async def token(client, user, monkeypatch):
    client.post("/api/auth/signup", json=user)

    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )

    data = response.json()
    return data.get("access_token")


def test_set_rating_handler(client, user, token):
    photo_id = 1
    rating = {"rating": 5}
    response = client.post(
        f"/api/rating/{photo_id}",
        json=rating,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_json = response.json()

    assert response.status_code == 200, response.text
    assert response_json.get("data").get("rating") == rating.get("rating"), response.text


def test_update_rating_handler(client, user, token):
    photo_id = 1
    rating = {"rating": 4}
    response = client.post(
        f"/api/rating/{photo_id}",
        json=rating,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_json = response.json()

    assert response.status_code == 200, response.text
    assert response_json.get("data").get("rating") == rating.get("rating"), response.text


def test_get_average_rating_handler(client):
    photo_id = 1
    response = client.get(
        f"/api/rating/avg/{photo_id}",
    )
    response_json = response.json()

    assert response.status_code == 200, response.text
    assert response_json.get("data").get("rating") == 4, response.text


def test_delete_rating_handler(client, user, token):
    photo_id = 1
    response = client.delete(
        f"/api/rating/{photo_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    response_json = response.json()

    assert response.status_code == 200, response.text
    assert response_json.get("data").get("rating") == 4, response.text
