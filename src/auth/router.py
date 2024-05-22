from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import ForgotPasswordTokenSchema, TokenSchema
from src.database import get_db
from src.schemas import ResponseModel
from src.services.authentication import auth_service
from src.user import service as users
from src.user.schemas import (
    UserRequestEmailSchema,
    UserRequestPasswordResetSchema,
    UserResponseSchema,
    UserSchema,
)

router = APIRouter(prefix="/auth", tags=["Auth"])
get_refresh_token = HTTPBearer()


@router.post(
    "/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED
)
async def signup(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes in a UserSchema object, which is validated by pydantic.
        If the email already exists, it raises an HTTPException with status code 409 (Conflict).
        Otherwise, it hashes the password and creates a new user using create_user from repositories/users.py.

    :param body: UserSchema: Validate the request body
    :param db: AsyncSession: Get the database session
    :return: A user object
    :doc-author: Trelent
    """
    exist_user = await users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="ACCOUNT EXIST"
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await users.create_user(body, db)

    return {"data": new_user}


@router.post("/login", response_model=TokenSchema)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Handle user login.

    This endpoint allows users to log in using their email and password. It verifies the credentials,
    generates access and refresh tokens, and updates the user's refresh token in the database.

    Args:
        body (OAuth2PasswordRequestForm): The login credentials.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the email is invalid, the email is not confirmed, or the password is invalid,
                       with appropriate status codes and error messages.

    Returns:
        dict: A dictionary containing the access token, refresh token, and token type.
    """
    user = await users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    # if not user.confirmed:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if user.blocked == True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is bloked")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    db: AsyncSession = Depends(get_db),
    user: UserSchema = Depends(auth_service.get_current_user),
):
    """
    Logout user endpoint

    :param db: database session
    :type db: AsyncSession
    :param user: user
    :type user: User

    :return: None

    """
    await users.update_token(user, None, db)
    return {}


@router.get("/refresh_token", response_model=TokenSchema)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh the access token.

    This endpoint allows users to refresh their access token using their refresh token. It verifies
    the refresh token, generates new access and refresh tokens, and updates the user's refresh token
    in the database.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials containing the refresh token.
        db (AsyncSession): The database session.

    Raises:
        HTTPException: If the refresh token is invalid, with a 401 status code and a message indicating
                       that the refresh token is invalid.

    Returns:
        dict: A dictionary containing the new access token, refresh token, and token type.
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/forget_password",
    response_model=ForgotPasswordTokenSchema,
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))]
)
async def forget_password(
    body: UserRequestEmailSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    Forget password endpoint

    :param body: email
    :type body: UserRequestEmailSchema
    :param db: database session
    :type db: AsyncSession

    :return: message
    :rtype: dict
    """
    exsisting_user = await users.get_user_by_email(body.email, db)
    if not exsisting_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Email address",
        )

    reset_token = await auth_service.create_password_reset_token(
        data={"sub": exsisting_user.email}
    )
    return {
        "message": "For reset password use this token in endpoint /reset_password",
        "reset_token": reset_token,
    }


@router.post(
    "/reset_password",
    response_model=ResponseModel,
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))]
)
async def reset_password(
    body: UserRequestPasswordResetSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    Reset password endpoint

    :param body: email
    :type body: UserRequestPasswordResetSchema
    :param db: database session
    :type db: AsyncSession

    :return: message
    :rtype: dict
    """
    try:
        email = await auth_service.decode_password_reset_token(body.reset_token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid reset token")
        if body.new_password != body.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords don't match")
        hashed_password = auth_service.get_password_hash(body.new_password)
        await users.update_password(email, hashed_password, db)
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Some thing unexpected happened!")
