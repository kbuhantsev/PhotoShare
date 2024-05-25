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

    async def test_delete_tag(self):
        result = await delete_tag(tag_id=1, db=self.session)
        self.assertIsNone(None)

    async def test_get_tags(self):
        result = await get_tags(db=self.session)
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
