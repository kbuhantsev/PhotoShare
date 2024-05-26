import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException, status
from passlib.context import CryptContext
from src.services.authentication import Auth
from src.user.schemas import UserResponseSchema
from src.user import service as users

class TestAuth(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.auth = Auth()
        self.test_email = "test@example.com"
        self.test_password = "test_password"
        self.test_hashed_password = self.auth.get_password_hash(self.test_password)

    def test_verify_password_match(self):
        self.auth.pwd_context = MagicMock(spec=CryptContext)
        self.auth.pwd_context.verify.return_value = True

        plain_password = "test_password"
        hashed_password = self.auth.pwd_context.hash(plain_password)
        self.assertTrue(self.auth.verify_password(plain_password, hashed_password))
        self.auth.pwd_context.verify.assert_called_once_with(plain_password, hashed_password)

    def test_verify_password_no_match(self):
        self.auth.pwd_context = MagicMock(spec=CryptContext)
        self.auth.pwd_context.verify.return_value = False

        plain_password = "test_password"
        hashed_password = self.auth.pwd_context.hash("different_password")

        self.assertFalse(self.auth.verify_password(plain_password, hashed_password))
        self.auth.pwd_context.verify.assert_called_once_with(plain_password, hashed_password)

    async def test_create_access_token(self):
        token = await self.auth.create_access_token({"sub": self.test_email})
        self.assertIsInstance(token, str)

    async def test_create_refresh_token(self):
        token = await self.auth.create_refresh_token({"sub": self.test_email})
        self.assertIsInstance(token, str)

    async def test_decode_refresh_token_success(self):
        refresh_token = await self.auth.create_refresh_token({"sub": self.test_email})
        email = await self.auth.decode_refresh_token(refresh_token)
        self.assertEqual(email, self.test_email)

    async def test_decode_refresh_token_invalid_scope(self):
        refresh_token = await self.auth.create_access_token({"sub": self.test_email})
        with self.assertRaises(HTTPException) as cm:
            await self.auth.decode_refresh_token(refresh_token)
        self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(cm.exception.detail, "Invalid scope for token")

    async def test_decode_refresh_token_invalid_token(self):
        with self.assertRaises(HTTPException) as cm:
            await self.auth.decode_refresh_token("invalid_token")
        self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(cm.exception.detail, "Could not validate credentials")

    async def test_get_current_user_success(self):
        token = await self.auth.create_access_token({"sub": self.test_email})
        db = AsyncMock()
        mock_user_resp = UserResponseSchema(username="Bob", email="test@example.com", password="password")
        with patch.object(users, "get_user_by_email", return_value=mock_user_resp):
            result = await self.auth.get_current_user(token, db, )
            self.assertEqual(result, mock_user_resp)

    async def test_get_current_user_invalid_token(self):
        db = AsyncMock()
        mock_user_resp = UserResponseSchema(username="Bob", email="test@example.com", password="password")

        with (patch.object(users, "get_user_by_email", return_value=mock_user_resp)):
            with patch.object(self.auth, 'create_access_token', return_value="invalid_token") as mock_create_token:
                token = mock_create_token.return_value
                with self.assertRaises(HTTPException) as cm:
                    await self.auth.get_current_user(token, db,)
                self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    async def test_get_current_user_user_not_found(self):
        token = await self.auth.create_access_token({"sub": self.test_email})
        db = AsyncMock()

        with (patch.object(users, "get_user_by_email", return_value=None)):
            with self.assertRaises(HTTPException) as cm:
                await self.auth.get_current_user(token, db,)

            self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    async def test_create_email_token(self):
        token = self.auth.create_email_token({"sub": self.test_email})
        self.assertIsInstance(token, str)

    async def test_get_email_from_token(self):
        email_token = self.auth.create_email_token({"sub": self.test_email})
        email = await self.auth.get_email_from_token(email_token)
        self.assertEqual(email, self.test_email)

    async def test_create_password_reset_token(self):
        token = await self.auth.create_password_reset_token({"sub": self.test_email})
        self.assertIsInstance(token, str)

    async def test_decode_password_reset_token(self):
        password_reset_token = await self.auth.create_password_reset_token({"sub": self.test_email})
        email = await self.auth.decode_password_reset_token(password_reset_token)
        self.assertEqual(email, self.test_email)


if __name__ == '__main__':
    unittest.main()
