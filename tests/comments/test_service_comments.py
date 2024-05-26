import unittest
from unittest.mock import AsyncMock, patch, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.models import Comment
from src.user.models import User
from src.comments.schemas import CommentSchema
from src.comments.service import create_comment, delete_comment, get_comments


class TestCreateCommentHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)

    async def test_create_comment(self):
        mocked_user = MagicMock(spec=User)

        comment = CommentSchema(comment="Test comment", photo_id=1)
        result = await create_comment(comment, self.session, mocked_user)
        self.assertEqual(result.comment, comment.comment)

    # async def test_get_comments_success(self, mock_get_db, mock_get_comments):
    #     pass
    #
    # async def test_update_comment_success(self, mock_get_db, mock_get_current_user, mock_update_comment):
    #     pass
    #
    # async def test_delete_comment_success(self, mock_allowed_delete_comments, mock_get_db, mock_delete_comment):
    #     pass
