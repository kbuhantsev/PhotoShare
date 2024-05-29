import unittest
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.rating.models import Rating
from src.rating.service import (
    create_update_rating,
    delete_rating,
    get_average_rating,
    get_rating,
)


class TestRatingService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)

    async def test_create_rating(self):
        rating = Rating()

        mocked_rating = MagicMock()
        mocked_rating.scalars.return_value.first.return_value = rating
        self.session.execute.return_value = mocked_rating

        result = await create_update_rating(
            db=self.session, photo_id=1, user_id=1, rating=5
        )
        self.assertIsInstance(result, Rating)
        self.assertEqual(result.rating, 5)

    async def test_update_rating(self):
        rating = Rating()

        mocked_rating = MagicMock()
        mocked_rating.scalars.return_value.first.return_value = rating
        self.session.execute.return_value = mocked_rating

        result = await create_update_rating(
            db=self.session, photo_id=1, user_id=1, rating=4
        )
        self.assertIsInstance(result, Rating)
        self.assertEqual(result.rating, 4)

    async def test_rating_get(self):
        rating = Rating()

        mocked_rating = MagicMock()
        mocked_rating.scalar_one_or_none.return_value = rating
        self.session.execute.return_value = mocked_rating

        result = await get_rating(db=self.session, photo_id=1, user_id=1)
        self.assertIsInstance(result, Rating)

    async def test_delete_rating(self):
        rating = Rating()

        mocked_rating = MagicMock()
        mocked_rating.scalars.return_value.first.return_value = rating
        self.session.execute.return_value = mocked_rating

        result = await delete_rating(db=self.session, photo_id=1, user_id=1)
        self.assertIsInstance(result, Rating)

    async def test_get_average_rating(self):
        mocked_rating = MagicMock()
        mocked_rating.scalars.return_value.all.return_value = []
        self.session.execute.return_value = mocked_rating

        result = await get_average_rating(db=self.session, photo_id=1)
        self.assertEqual(result, 0)
