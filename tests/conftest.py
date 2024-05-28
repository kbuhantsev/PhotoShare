import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.comments.models import Comment
from src.database import get_db
from src.main import app
from src.models import Base
from src.photos.models import Photo
from src.tags.models import Tag
from src.user.models import Role, User

DATABASE_TEST_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_TEST_URL)

TestingSession = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


@pytest.fixture(scope="module")
def session():
    async def get_session():
        async with TestingSession() as session:
            yield session

    asyncio.run(get_session())


@pytest.fixture(scope="module", autouse=True)
def create_test_database():
    async def init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init())


@pytest.fixture(scope="module")
def client():

    async def override_get_db():
        async with TestingSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {
        "username": "test",
        "email": "test@test.com",
        "password": "testtest",
        "avatar": None
    }
