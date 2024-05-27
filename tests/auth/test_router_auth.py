access_token = ""
refresh_token = ""
reset_token = ""
new_password = "testpass"


def test_signup(client, user):
    response = client.post("/api/auth/signup", json=user)

    assert response.status_code == 201, response.text
    data = response.json()["data"]
    assert data["username"] == user["username"]
    assert data["email"] == user["email"]


def test_signup_already_exist(client, user):
    response = client.post("/api/auth/signup", json=user)

    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "ACCOUNT EXIST"


def test_login(client, user):
    global access_token, refresh_token
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"

    # Update
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]


def test_login_fail(client):
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "test_password"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid email"


def test_login_invalid_password(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": "wrong_password"},
    )

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid password"


def test_refresh_token(client):
    global access_token, refresh_token
    response = client.get(
        "/api/auth/refresh_token",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"

    access_token = data["access_token"]
    refresh_token = data["refresh_token"]


def test_refresh_token_fail(client):
    response = client.get(
        "/api/auth/refresh_token",
        headers={"Authorization": f"Bearer "},
    )

    assert response.status_code == 403
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_logout(client):
    response = client.get(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204


def test_logout_fail(client):
    response = client.get(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer "},
    )

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Could not validate credentials"


def test_forget_password(client, user):
    global reset_token
    response = client.post(
        "/api/auth/forget_password",
        json={"email": user["email"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reset_token"]

    reset_token = data["reset_token"]


def test_forget_password_invalid_email(client):
    global reset_token
    response = client.post(
        "/api/auth/forget_password",
        json={"email": "test@example.com"},
    )

    assert response.status_code == 404
    data = response.json()
    assert data["detail"]
    assert data["detail"] == "Invalid Email address"


def test_change_password_confirm_not_match(client):
    response = client.post(
        "/api/auth/reset_password",
        json={
            "reset_token": reset_token,
            "new_password": new_password,
            "confirm_password": "other_pass",
        },
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"]
    assert data["detail"] == "Some thing unexpected happened!"


def test_change_password(client):
    response = client.post(
        "/api/auth/reset_password",
        json={
            "reset_token": reset_token,
            "new_password": new_password,
            "confirm_password": new_password,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"]
    assert data["message"] == "Password updated successfully"


def test_login_with_new_password(client, user):
    global access_token, refresh_token
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": new_password},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"

    # Update
    access_token = data["access_token"]
    refresh_token = data["refresh_token"]


def test_logout_with_new_password(client):
    response = client.get(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204
