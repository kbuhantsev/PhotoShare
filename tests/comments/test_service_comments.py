import unittest
from unittest.mock import AsyncMock, MagicMock,patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User
from src.comments.schemas import CommentSchema
from src.comments.service import create_comment, delete_comment, get_comments,update_comment
from src.tags.models import PhotoToTag
from src.user.models import Role


class TestCreateCommentHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)


    async def test_create_comment(self):
        mocked_user = MagicMock(spec=User)

        comment = CommentSchema(comment="Test comment", photo_id=1)
        result = await create_comment(comment, self.session, mocked_user)
        self.assertEqual(result.comment, comment.comment)

    async def test_comment_get(self):
        photo_id = 1
        result_list = []

        mocked_comments = MagicMock()
        mocked_comments.scalars.return_value.all.return_value = result_list
        self.session.execute.return_value = mocked_comments

        result = await get_comments(photo_id, self.session)
        self.assertEqual(result, result_list)

    async def test_update_comment(self):
        self.mocked_user = MagicMock(spec=User)
        self.mocked_user.id = 1
        result_comment=''
        comment_id=1
        new_comment_test = "Updated comment"
        mock_comment = MagicMock()
        mock_comment.id = comment_id
        mock_comment.user_id=self.mocked_user.id
        mock_comment.return_value.scalar_one_or_none = result_comment
        self.session.execute.return_value = mock_comment
        result = await update_comment(comment_id,new_comment_test,self.session,self.mocked_user)
        self.assertEqual(result.comment,new_comment_test)

    async def test_delete_comment(self):
        comment_id = 1
        mock_comment = MagicMock()
        result_comment=''
        mock_comment.return_value.scalar_one_or_none = result_comment
        self.session.execute.return_value = mock_comment
        result = await delete_comment(comment_id, self.session)

        self.session.delete.assert_called_once_with(result)

    # async def test_get_comments_success(self, mock_get_db, mock_get_comments):

    # async def test_update_comment_success(self, mock_get_db, mock_get_current_user, mock_update_comment):
    #     pass
    #
    # async def test_delete_comment_success(self, mock_allowed_delete_comments, mock_get_db, mock_delete_comment):
    #     pass
