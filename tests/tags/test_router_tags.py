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


def test_get_empty_tags(client):
    response = client.get("/api/tags/")

    assert response.status_code == 500, response.text


def test_create_tag(client, token):
    tag_name = "test_tag"
    response = client.post(
        "/api/tags/",
        json={"name": tag_name},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201, response.text


def test_get_tags(client):
    response = client.get("/api/tags/")

    assert response.status_code == 200, response.text
    data_obj = response.json()
    assert len(data_obj.get("data")) == 1
    assert data_obj.get("data")[0].get("name") == "test_tag"


def test_delete_tag(client, token):
    response = client.delete(
        "/api/tags/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, response.text


def test_delete_nonexistent_tag(client, token):
    response = client.delete("/api/tags/999", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 500, response.text
