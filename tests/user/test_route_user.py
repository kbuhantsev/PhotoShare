from unittest.mock import MagicMock
import pytest_asyncio
from starlette.datastructures import QueryParams

from fastapi import File


@pytest_asyncio.fixture()
async def token(client, user, monkeypatch):
    client.post("/api/auth/signup", json=user)

    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )

    data = response.json()
    return data.get("access_token")


def test_get_current_user(client, token, user):
    response = client.get(
        "/api/user/current", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["username"] == user["username"]
    assert data_obj["email"] == user["email"]
    assert data_obj["role"] == "ADMIN"


def test_update_user(client, token, user):
    user_fields = {"username": user["username"], "email": user["email"]}
    response = client.put(
        "/api/user",
        json=user_fields,
        headers={"Authorization": f"Bearer {token}"},
        
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["username"] == user_fields["username"]
    assert data_obj["email"] == user_fields["email"]

    # update user again
    # response = client.put(
    #     "/api/user",
    #     json={"username": user["username"], "email": user["email"]},
    #     headers={"Authorization": f"Bearer {token}"},
    # )


def test_update_avatar(client, token, monkeypatch):
    pass
    # monkeypatch.setattr("fastapi.File", MagicMock(spec=File))
    # response = client.patch(
    #     "/api/user/avatar",
    #     data={"file": (File(), "avatar.png")},
    #     headers={"Authorization": f"Bearer {token}"},
    # )

    # assert response.status_code == 200, response.text
    # data_obj = response.json()["data"]
    # assert data_obj["avatar_url"]


def test_reset_password_success(client, token, user):
    response = client.patch(
        "/api/user/reset_password",
        json={"new_password": user["password"], "confirm_password": user["password"]},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()
    assert data_obj["message"] == "Password updated successfully"


def test_reset_password_fail_confirm_password(client, token):
    response = client.patch(
        "/api/user/reset_password",
        json={"new_password": "new_password", "confirm_password": "new_passwor2"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()
    assert data_obj["status"] == "error"
    assert data_obj["message"] == "400: Passwords don't match"


def test_get_profile_exsists_user(client, token):
    response = client.get(
        "/api/user/profile/test",
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["username"] == "test"
    assert data_obj["email"] == "test@test.com"
    assert data_obj["role"] == "ADMIN"


def test_get_profile_non_exsists_user(client, token):
    response = client.get(
        "/api/user/profile/test2",
    )

    assert response.status_code == 404, response.text
    data_obj = response.json()
    # assert data_obj["status"] == "error"
    # assert data_obj["message"] == "User not found"
    assert data_obj["detail"] == "User not found"


def test_block_user_success(client, token):

    new_user = {
        "username": "test_user",
        "email": "test_user@test.com",
        "password": "testtest",
    }

    client.post("/api/auth/signup", json=new_user)

    data = {
        "blocked_user": new_user["email"],
        "block": True,
    }
    response = client.post(
        "/api/user/block/",
        data=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["blocked"] == True


def test_unblock_user_success(client, token):

    response = client.post(
        "/api/user/block/",
        data={"blocked_user": "test_user@test.com", "block": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["blocked"] == False
