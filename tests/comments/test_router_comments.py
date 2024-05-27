import pytest_asyncio
from starlette.datastructures import QueryParams


@pytest_asyncio.fixture()
async def token(client, user, monkeypatch):
    client.post("/api/auth/signup", json=user)

    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )

    data = response.json()
    return data.get("access_token")


def test_create_comment_success(client, token):
    comment = {"photo_id": 1, "comment": "Test comment"}
    response = client.post(
        "/api/comments",
        json=comment,
        headers={"Authorization": f"Bearer {token}"}
    )

    response_json = response.json()

    assert response.status_code == 201, response.text
    assert response_json.get("data").get("photo_id") == comment.get("photo_id"), response.text
    assert response_json.get("data").get("comment") == comment.get("comment"), response.text
    assert response_json.get("data").get("user_id") == 1, response.text


def test_get_comments_success(client):
    photo_id = 1
    response = client.get(f"/api/comments/{photo_id}")

    assert response.status_code == 200, response.text


def test_get_comments_fail(client):
    photo_id = 999
    response = client.get(f"/api/comments/{photo_id}")

    assert response.status_code == 500, response.text


def test_update_comment_success(client, token):
    comment = {"comment_id": 1, "comment": "Updated comment"}
    response = client.put(
        "/api/comments/1",
        params=QueryParams(comment=comment.get("comment")),
        headers={"Authorization": f"Bearer {token}"}
    )
    response_json = response.json()

    assert response.status_code == 200, response.text
    assert response_json.get("data").get("comment") == comment.get("comment"), response.text


def test_update_comment_fail(client, token):
    comment = {"comment_id": 999, "comment": "Updated comment"}
    response = client.put(
        "/api/comments/999",
        params=QueryParams(comment=comment.get("comment")),
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 500, response.text


def test_delete_comment_success(client, token):
    response = client.delete(
        "/api/comments/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text


def test_delete_comment_fail(client, token):
    response = client.delete(
        "/api/comments/999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 500, response.text
