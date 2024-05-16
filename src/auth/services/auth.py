from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.database import get_db
from src.settings import settings

class Auth:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm

    def verify_password(self, plain_password, hashed_password):
        """
        Verify plain password with hashed password

        :param plain_password: plain password
        :type plain_password: str
        :param hashed_password: hashed password
        :type hashed_password: str

        :return: password verification
        :rtype: bool
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Get password hash

        :param password: password
        :type password: str

        :return: password hash
        :rtype: str
        """
        return self.pwd_context.hash(password)

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Create access token

        :param data: data
        :type data: dict
        :param expires_delta: expires delta
        :type expires_delta: Optional[float]

        :return: access token
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(UTC), "exp": expire, "scope": "access_token"}
        )
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ):
        """
        Create refresh token

        :param data: data
        :type data: dict
        :param expires_delta: expires delta
        :type expires_delta: Optional[float]

        :return: refresh token
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + +timedelta(seconds=expires_delta)
        else:
            expire = datetime.now(UTC) + timedelta(days=7)
        to_encode.update(
            {"iat": datetime.now(UTC), "exp": expire, "scope": "refresh_token"}
        )
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def decode_refresh_token(self, token: str):
        """
        Decode refresh token

        :param token: refresh token
        :type token: str

        :return: email
        :rtype: str | HTTPException
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "refresh_token":
                email = payload["sub"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ):
        """
        Get current user

        :param token: access token
        :type token: str
        :param db: database session
        :type db: AsyncSession

        :return: user
        :rtype: User | HTTPException
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user_db = await users.get_user_by_email(email, db)
        if user_db is None:
            raise credentials_exception
        return user_db

    async def create_email_token(self, data: dict):
        """
        Create email token for email verification

        :param data: data
        :type data: dict

        :return: email token
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=1)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def decode_email_token(self, token: str):
        """
        Decode email token for email verification

        :param token: email token
        :type token: str

        :return: email
        :rtype: str | HTTPException
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not validate credentials for email verification",
            )

    async def create_password_reset_token(self, data: dict):
        """
        Create password reset token

        :param data: data
        :type data: dict

        :return: password reset token
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(hours=3)
        to_encode.update({"iat": datetime.now(UTC), "exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def decode_password_reset_token(self, token: str):
        """
        Decode password reset token

        :param token: password reset token
        :type token: str

        :return: email
        :rtype: str | HTTPException
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not validate credentials for password reset",
            )


auth_service = Auth()