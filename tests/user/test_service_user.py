import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base
from src.user.models import User, Role
from src.photos.models import Photo
from src.comments.models import Comment
from src.tags.models import Tag
from src.user.service import (
    create_user,
    get_count_users,
    get_user_by_email,
    update_user,
    update_avatar_url,
    update_password,
    update_role,
    update_token,
    block_user,
    get_all_users,
    get_user_profile,
    get_user_comments,
    get_user_photos,
)
from src.user.schemas import UserSchema, UserUpdateSchema


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

    @patch("src.user.service.get_count_users", new=AsyncMock(return_value=0))
    async def test_create_first_user(self):

        body = UserSchema(
            email="test@example.com", username="test", password="123456789"
        )

        result = await create_user(body=body, db=self.session)

        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.role, Role.ADMIN)

    @patch("src.user.service.get_count_users", new=AsyncMock(return_value=1))
    async def test_create_next_user(self):

        body = UserSchema(
            email="test@example.com", username="test", password="123456789"
        )

        result = await create_user(body=body, db=self.session)

        self.assertIsInstance(result, User)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.role, None)

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

    async def test_get_user_by_email_not_found(self):
        user = User(
            id=1,
            username="test",
            email="test@example.com",
            password="testtest",
            avatar=None,
            role="USER",
        )
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(email=user.email, db=self.session)
        self.assertIsNone(result)

    async def test_update_user(self):
        user = User()
        user_fields = UserUpdateSchema(username="test2", email="test2@example.com")
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_user(email=user.email, body=user_fields, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.email, user_fields.email)
        self.assertEqual(result.username, user_fields.username)

    async def test_update_avatar_url(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_avatar_url(
            email=user.email, url="test_url", db=self.session
        )
        self.assertIsInstance(result, User)
        self.assertEqual(result.avatar, "test_url")

    async def test_update_password(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_password(
            email=user.email, password="test_password", db=self.session
        )
        self.assertIsInstance(result, User)
        self.assertEqual(result.password, "test_password")

    async def test_update_role(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_role(user=user, role=Role.ADMIN, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.role, Role.ADMIN)

    async def test_update_token(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await update_token(user=user, token="test_token", db=self.session)
        self.assertEqual(result, None)
        self.assertEqual(user.refresh_token, "test_token")

    async def test_block_user(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await block_user(user=user, block=True, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.blocked, True)

    async def test_unblock_user(self):
        user = User()
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = user
        self.session.execute.return_value = mocked_user
        result = await block_user(user=user, block=False, db=self.session)
        self.assertIsInstance(result, User)
        self.assertEqual(result.blocked, False)

    async def test_get_all_users(self):
        users_data =[{"user": User()}, {"user": User()}]
        mocked_users = MagicMock()
        mocked_users.mappings.return_value.all.return_value = users_data
        self.session.execute.return_value = mocked_users
        result = await get_all_users(db=self.session)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [user_data["user"].to_dict() for user_data in users_data])

    async def test_get_user_profile(self):
        user = {"user": User()}
        mocked_user = MagicMock()
        mocked_user.mappings.return_value.first.return_value = user
        self.session.execute.return_value = mocked_user
        result = await get_user_profile(username=user["user"].username, db=self.session)
        self.assertIsInstance(result, dict)
        self.assertEqual(result, user["user"].to_dict())
    
    async def test_get_user_profile_not_found(self):
        mocked_user = MagicMock()
        mocked_user.mappings.return_value.first.return_value = None
        self.session.execute.return_value = mocked_user
        result = await get_user_profile(username="", db=self.session)
        self.assertEqual(result, None)

    async def test_get_user_photos(self):
        photos = [Photo(), Photo(), Photo()]
        mocked_photos = MagicMock()
        mocked_photos.scalars.return_value.all.return_value = photos
        self.session.execute.return_value = mocked_photos
        result = await get_user_photos(skip=0, limit=50, user= User(), db=self.session)
        self.assertEqual(result, photos)

    async def test_get_user_comments(self):
        comments = [Comment(), Comment(), Comment()]
        mocked_comments = MagicMock()
        mocked_comments.scalars.return_value.all.return_value = comments
        self.session.execute.return_value = mocked_comments
        result = await get_user_comments(skip=0, limit=50, user= User(), db=self.session)
        self.assertEqual(result, comments)
