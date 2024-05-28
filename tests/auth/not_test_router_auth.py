import unittest
from unittest.mock import AsyncMock, patch

from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.router import (
    forget_password,
    login,
    logout,
    refresh_token,
    reset_password,
    signup,
)
from src.services.authentication import auth_service
from src.user import service as users
from src.user.schemas import (
    UserRequestEmailSchema,
    UserRequestPasswordResetSchema,
    UserResponseRefreshToken,
    UserResponseSchema,
    UserSchema,
)


class TestRefreshTokenFunction(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user_ref_token = UserResponseRefreshToken(username='Bob', email="test@example.com",
                                                            password='123456789', refresh_token="valid_refresh_token")
        self.mock_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_refresh_token")

    async def test_refresh_token_success(self):
        # Mock the dependencies
        mock_access_token = "new_access_token"
        mock_refresh_token = "new_refresh_token"

        # Mock the token decoding, token creation, and user update
        with patch.object(auth_service, 'decode_refresh_token', return_value=self.mock_user_ref_token.email):
            with patch.object(users, 'get_user_by_email', return_value=self.mock_user_ref_token):
                with patch.object(auth_service, 'create_access_token', return_value=mock_access_token):
                    with patch.object(auth_service, 'create_refresh_token', return_value=mock_refresh_token):
                        with patch.object(users, 'update_token', return_value=None):
                            # Call the function
                            result = await refresh_token(credentials=self.mock_credentials, db=self.mock_db)

                            # Assert the result
                            self.assertEqual(result, {
                                "access_token": mock_access_token,
                                "refresh_token": mock_refresh_token,
                                "token_type": "bearer",
                            })

                            # Assert that the user's token was updated
                            users.update_token.assert_called_once_with(self.mock_user_ref_token, mock_refresh_token,
                                                                       self.mock_db)

    async def test_refresh_token_invalid(self):
        # Mock the dependencies
        mock_credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_refresh_token")

        # Mock the token decoding and user update
        with patch.object(auth_service, 'decode_refresh_token', return_value=self.mock_user_ref_token.email):
            with patch.object(users, 'get_user_by_email', return_value=self.mock_user_ref_token):
                with patch.object(users, 'update_token', return_value=None):
                    # Call the function and expect an HTTPException
                    with self.assertRaises(HTTPException) as cm:
                        await refresh_token(credentials=mock_credentials, db=self.mock_db)

                    # Assert the exception
                    self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
                    self.assertEqual(cm.exception.detail, "Invalid refresh token")

                    # Assert that the user's token was updated to None
                    users.update_token.assert_called_once_with(self.mock_user_ref_token, None, self.mock_db)


class TestLogoutFunction(unittest.IsolatedAsyncioTestCase):
    async def test_logout_success(self):
        pass
        # Mock the dependencies
        mock_db = AsyncMock(spec=AsyncSession)
        mock_user = UserSchema(username='Bob', email="test@example.com", password='123456789')

        # Mock the user token update
        with patch.object(users, 'update_token', return_value=None):
            # Call the function
            result = await logout(db=mock_db, user=mock_user)

            # Assert the result
            self.assertEqual(result, {})

            # Assert that the user's token was updated to None
            users.update_token.assert_called_once_with(mock_user, None, mock_db)


class TestSignupFunction(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user_body = UserSchema(username="Bob", email="test@example.com", password="password")
        self.mock_user_resp = UserResponseSchema(username="Bob", email="test@example.com", password="password")

    async def test_signup_success(self):
        # Mock the user retrieval and creation
        with patch.object(users, 'get_user_by_email', return_value=None):
            with patch.object(auth_service, 'get_password_hash', return_value="hashed_password"):
                with patch.object(users, 'create_user', return_value=self.mock_user_resp):
                    # Call the function
                    result = await signup(body=self.mock_user_body, db=self.mock_db)

                    # Assert the result
                    self.assertEqual(result, self.mock_user_resp)

                    # Assert that the user was created with the hashed password
                    self.mock_user_body.password = "hashed"
                    users.create_user.assert_called_once_with(self.mock_user_body, self.mock_db)

    async def test_signup_email_exists(self):
        # Mock the user retrieval
        with patch.object(users, 'get_user_by_email', return_value=self.mock_user_resp):
            # Call the function and expect an HTTPException
            with self.assertRaises(HTTPException) as cm:
                await signup(body=self.mock_user_body, db=self.mock_db)

            # Assert the exception
            self.assertEqual(cm.exception.status_code, status.HTTP_409_CONFLICT)
            self.assertEqual(cm.exception.detail, "ACCOUNT EXIST")


class TestLoginFunction(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user = AsyncMock(email="test@example.com", password="hashed_password")
        self.mock_body = OAuth2PasswordRequestForm(username="test@example.com", password="test_password")

    async def test_login_success(self):
        # Mock the dependencies
        mock_access_token = "mock_access_token"
        mock_refresh_token = "mock_refresh_token"

        # Mock the user retrieval and token update
        with patch.object(users, 'get_user_by_email', return_value=self.mock_user):
            with patch.object(auth_service, 'verify_password', return_value=True):
                with patch.object(auth_service, 'create_access_token', return_value=mock_access_token):
                    with patch.object(auth_service, 'create_refresh_token', return_value=mock_refresh_token):
                        with patch.object(users, 'update_token', return_value=None) as mock_update_token:
                            # Call the function
                            result = await login(body=self.mock_body, db=self.mock_db)

                            # Assert the result
                            self.assertEqual(result, {
                                "access_token": mock_access_token,
                                "refresh_token": mock_refresh_token,
                                "token_type": "bearer",
                            })

                            # Assert that the user was updated with the refresh token

                            mock_update_token.assert_called_once_with(self.mock_user, mock_refresh_token, self.mock_db)

    async def test_login_invalid_email(self):
        # Mock the dependencies
        mock_user = None

        # Mock the user retrieval
        with patch.object(users, 'get_user_by_email', return_value=mock_user):
            # Call the function and expect an HTTPException
            with self.assertRaises(HTTPException) as cm:
                await login(body=self.mock_body, db=self.mock_db)

            # Assert the exception
            self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(cm.exception.detail, "Invalid email")

    async def test_login_invalid_password(self):
        # Mock the user retrieval and password verification
        with patch.object(users, 'get_user_by_email', return_value=self.mock_user):
            with patch.object(auth_service, 'verify_password', return_value=False):
                # Call the function and expect an HTTPException
                with self.assertRaises(HTTPException) as cm:
                    await login(body=self.mock_body, db=self.mock_db)

                # Assert the exception
                self.assertEqual(cm.exception.status_code, status.HTTP_401_UNAUTHORIZED)
                self.assertEqual(cm.exception.detail, "Invalid password")


class TestResetPasswordFunction(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)

    async def test_reset_password_success(self):
        # Mock the dependencies
        mock_body = UserRequestPasswordResetSchema(
            reset_token="valid_reset_token",
            new_password="new_password",
            confirm_password="new_password"
        )

        mock_email = "test@example.com"

        # Mock the token decoding and password update
        with patch.object(auth_service, 'decode_password_reset_token', return_value=mock_email):
            with patch.object(auth_service, 'get_password_hash', return_value="hashed_password"):
                with patch.object(users, 'update_password', return_value=None):
                    # Call the function
                    result = await reset_password(body=mock_body, db=self.mock_db)

                    # Assert the result
                    self.assertEqual(result, {
                        "message": "Password updated successfully"
                    })

                    # Assert that the token was decoded and the password was updated
                    auth_service.decode_password_reset_token.assert_called_once_with(mock_body.reset_token)
                    auth_service.get_password_hash.assert_called_once_with(mock_body.new_password)
                    users.update_password.assert_called_once_with(mock_email, "hashed_password", self.mock_db)

    async def test_reset_password_invalid_token(self):
        # Mock the dependencies
        mock_body = UserRequestPasswordResetSchema(
            reset_token="invalid_reset_token",
            new_password="new_password",
            confirm_password="new_password"
        )

        # Mock the token decoding
        with patch.object(auth_service, 'decode_password_reset_token', return_value=None):
            # Call the function and expect an HTTPException
            with self.assertRaises(HTTPException) as cm:
                await reset_password(body=mock_body, db=self.mock_db)

            # Assert the exception
            self.assertEqual(cm.exception.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(cm.exception.detail, 'Some thing unexpected happened!')

            # Assert that the token was decoded
            auth_service.decode_password_reset_token.assert_called_once_with(mock_body.reset_token)

    async def test_reset_password_passwords_dont_match(self):
        # Mock the dependencies
        mock_body = UserRequestPasswordResetSchema(
            reset_token="valid_reset_token",
            new_password="new_password",
            confirm_password="different_password"
        )

        # Call the function and expect an HTTPException
        with self.assertRaises(HTTPException) as cm:
            await reset_password(body=mock_body, db=self.mock_db)

        # Assert the exception
        self.assertEqual(cm.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(cm.exception.detail, 'Some thing unexpected happened!')


class TestForgetPasswordFunction(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.mock_user = UserRequestEmailSchema(email="test@example.com")

    async def test_forget_password_success(self):
        # Mock the dependencies
        mock_reset_token = "reset_token"

        # Mock the user retrieval and token creation
        with patch.object(users, 'get_user_by_email', return_value=self.mock_user):
            with patch.object(auth_service, 'create_password_reset_token', return_value=mock_reset_token):
                # Call the function
                result = await forget_password(body=self.mock_user, db=self.mock_db)

                # Assert the result
                self.assertEqual(result, {
                    "message": "For reset password use this token in endpoint /reset_password",
                    "reset_token": mock_reset_token,
                })

                # Assert that the user was retrieved and the token was created
                users.get_user_by_email.assert_called_once_with(self.mock_user.email, self.mock_db)
                auth_service.create_password_reset_token.assert_called_once_with(data={"sub": self.mock_user.email})

    async def test_forget_password_user_not_found(self):
        # Mock the user retrieval
        with patch.object(users, 'get_user_by_email', return_value=None):
            # Call the function and expect an HTTPException
            with self.assertRaises(HTTPException) as cm:
                await forget_password(body=self.mock_user, db=self.mock_db)

            # Assert the exception
            self.assertEqual(cm.exception.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(cm.exception.detail, "Invalid Email address")

            # Assert that the user was retrieved
            users.get_user_by_email.assert_called_once_with(self.mock_user.email, self.mock_db)


if __name__ == '__main__':
    unittest.main()
