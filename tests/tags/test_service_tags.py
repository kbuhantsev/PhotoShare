import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.tags.models import Tag
from src.tags.service import create_tag, delete_tag, get_tags


class TestTagsService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)

    async def test_create_tag(self):
        name = "test"
        result = await create_tag(name="test", db=self.session)
        self.assertIsInstance(result, Tag)
        self.assertEqual(result.name, name)

    async def test_get_tags(self):
        result_list = []

        mocked_tags = MagicMock()
        mocked_tags.scalars.return_value.all.return_value = result_list
        self.session.execute.return_value = mocked_tags

        result = await get_tags(db=self.session)
        self.assertIsInstance(result, list)
        self.assertEqual(result, result_list)

    async def test_delete_tag(self):

        tag = Tag(id=1, name="test")

        mocked_tags = MagicMock()
        mocked_tags.scalar_one_or_none.return_value = tag
        self.session.execute.return_value = mocked_tags

        result = await delete_tag(tag_id=1, db=self.session)
        self.assertEqual(result, tag)

    async def test_delete_tag_not_found(self):

        mocked_tags = MagicMock()
        mocked_tags.scalar_one_or_none.return_value = None
        self.session.execute.return_value = mocked_tags

        result = await delete_tag(tag_id=1, db=self.session)
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
