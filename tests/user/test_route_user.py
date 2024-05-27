import pytest_asyncio

from unittest.mock import MagicMock, mock_open, patch

import cloudinary
import src.services.cloudinary_utils as cloudinary_utils

new_user = {
    "username": "test_user",
    "email": "test_user@test.com",
    "password": "testtest",
}


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

    # Update user object
    user["role"] = data_obj["role"]


def test_update_user(client, token, user):
    user_fields = {"username": "Admin", "email": "Admin@test.com"}
    response = client.put(
        "/api/user",
        json=user_fields,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["username"] == user_fields["username"]
    assert data_obj["email"] == user_fields["email"]

    # Update user object
    user["username"] = data_obj["username"]
    user["email"] = data_obj["email"]


def test_update_avatar(client, token, monkeypatch):

    monkeypatch.setattr(
        "src.user.router.upload_file", MagicMock(return_value={"public_id": "avatar"})
    )
    monkeypatch.setattr(
        "src.user.router.build_url", MagicMock(return_value="test_avatar_url")
    )

    response = client.patch(
        "/api/user/avatar",
        files={"file": "avatar.jpg"},
        # files={"file" : file},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["avatar"] =="test_avatar_url"


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


def test_get_profile_exsists_user(client, token, user):
    response = client.get(
        f"/api/user/profile/{user['username']}",
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["username"] == user["username"]
    assert data_obj["email"] == user["email"]
    assert data_obj["role"] == user["role"]


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
        data={"blocked_user": new_user["email"], "block": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["blocked"] == False


def test_get_all_users_success(client, token, user):
    response = client.get(
        "/api/user",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert isinstance(data_obj, list)
    assert len(data_obj) == 2
    assert data_obj[0]["username"] == user["username"]
    assert data_obj[1]["username"] == new_user["username"]


def test_get_all_users_fail(client):

    response = client.post(
        "/api/auth/login",
        data={"username": new_user["email"], "password": new_user["password"]},
    )

    token_user = response.json().get("access_token")
    response = client.get(
        "/api/user",
        headers={"Authorization": f"Bearer {token_user}"},
    )

    assert response.status_code == 403, response.text


def test_get_user_photo(client, token):

    response = client.get(
        "/api/user/photos",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()
    assert len(data_obj["data"]) == 0
    assert data_obj["total"] == 0


def test_get_user_comments(client, token):

    response = client.get(
        "/api/user/comments",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()
    assert len(data_obj["data"]) == 0
    assert data_obj["total"] == 0


def test_get_users_roles_success(client, token):

    response = client.get(
        "/api/user/roles",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj == ["USER", "ADMIN", "MODERATOR"]


def test_get_users_roles_fail(client):

    response = client.post(
        "/api/auth/login",
        data={"username": new_user["email"], "password": new_user["password"]},
    )

    token_user = response.json().get("access_token")

    response = client.get(
        "/api/user/roles",
        headers={"Authorization": f"Bearer {token_user}"},
    )

    assert response.status_code == 403, response.text


def test_change_role_fail(client, token):

    response = client.post(
        "/api/auth/login",
        data={"username": new_user["email"], "password": new_user["password"]},
    )

    token_user = response.json().get("access_token")

    response = client.post(
        "/api/user/change_role",
        data={"changeable_user": new_user["email"], "role": "ADMIN"},
        headers={"Authorization": f"Bearer {token_user}"},
    )

    assert response.status_code == 403, response.text


def test_change_role_success(client, token):

    response = client.post(
        "/api/user/change_role",
        data={"changeable_user": new_user["email"], "role": "ADMIN"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    data_obj = response.json()["data"]
    assert data_obj["role"] == "ADMIN"
