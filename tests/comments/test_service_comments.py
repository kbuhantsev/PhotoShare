import unittest
from unittest.mock import AsyncMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.router import router
from src.comments.schemas import CommentSchema, CommentResponseSchema
from src.user.models import User


class TestCreateCommentHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_comment = CommentSchema(comment="Test comment", photo_id=1)
        self.mock_user = User(id=1, username="testuser", email="test@example.com")

    @patch("src.comments.service.create_comment")
    @patch("src.dependencies.get_current_user")
    @patch("src.database.get_db")
    async def test_create_comment_success(self, mock_get_db, mock_get_current_user, mock_create_comment):
        mock_get_db.return_value = self.mock_db
        mock_get_current_user.return_value = self.mock_user
        mock_create_comment.return_value = self.mock_comment

        response = client.post("/", json=self.mock_comment.dict(), headers={"Authorization": "Bearer token"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"data": self.mock_comment.dict()})
        mock_create_comment.assert_called_once_with(comment=self.mock_comment, db=self.mock_db,
                                                    current_user=self.mock_user)


class TestGetCommentsHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_comments = [CommentResponseSchema(id=1, content="Test comment")]

    @patch("src.comments.service.get_comments")
    @patch("src.database.get_db")
    async def test_get_comments_success(self, mock_get_db, mock_get_comments):
        mock_get_db.return_value = self.mock_db
        mock_get_comments.return_value = self.mock_comments

        response = client.get("/1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"data": [comment.dict() for comment in self.mock_comments]})
        mock_get_comments.assert_called_once_with(photo_id=1, db=self.mock_db)

    @patch("src.comments.service.update_comment")
    @patch("src.dependencies.get_current_user")
    @patch("src.database.get_db")
    async def test_update_comment_success(self, mock_get_db, mock_get_current_user, mock_update_comment):
        mock_get_db.return_value = self.mock_db
        mock_get_current_user.return_value = self.mock_user
        mock_update_comment.return_value = self.mock_comment

        response = client.put("/1", json={"comment": "Updated comment"}, headers={"Authorization": "Bearer token"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"data": self.mock_comment.dict()})
        mock_update_comment.assert_called_once_with(comment_id=1, comment="Updated comment", db=self.mock_db,
                                                    current_user=self.mock_user)

    @patch("src.comments.service.delete_comment")
    @patch("src.database.get_db")
    @patch("src.dependencies.allowed_delete_comments")
    async def test_delete_comment_success(self, mock_allowed_delete_comments, mock_get_db, mock_delete_comment):
        mock_get_db.return_value = self.mock_db
        mock_delete_comment.return_value = self.mock_comment
        mock_allowed_delete_comments.return_value = None

        response = client.delete("/1", headers={"Authorization": "Bearer token"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"data": self.mock_comment.dict()})
        mock_delete_comment.assert_called_once_with(comment_id=1, db=self.mock_db)


if __name__ == '__main__':
    unittest.main()
