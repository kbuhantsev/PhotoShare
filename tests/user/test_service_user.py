import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base
from src.user.models import User, Role
from src.photos.models import Photo
from src.comments.models import Comment
from src.tags.models import Tag
from src.user.service import create_user, get_count_users, get_user_by_email
from src.user.schemas import UserSchema


class TestUserService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_count_users(self):
        mocked_users = MagicMock()
        mocked_users.scalar.return_value = 0
        self.session.execute.return_value = mocked_users
        result = await get_count_users(db=self.session)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)

    # @patch("src.user.service.get_count_users")
    async def test_create_user(self):
        body = UserSchema(
            email="test@example.com", username="test", password="123456789"
        )

        get_count_users =MagicMock(return_value=0)
        
        result = await create_user(
            body=body,
            db=self.session,
        )

        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)

    async def test_get_user_by_email(self):
        user = User(
            id=1,
            username="test",
            email="test@example.com",
            password="testtest",
            avatar=None,
            role="USER",
        )
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(email=user.email, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, user.email)

    # async def test_get_user_by_id(self):
    #     user_id = 1
    #     result = await users.get_user_by_id(user_id=user_id, db=self.session)
    #     self.assertIsInstance(result, User)

    # async def test_get_current_user(self):
