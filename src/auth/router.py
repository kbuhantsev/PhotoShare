from fastapi import APIRouter, Depends, HTTPException, status, Request

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db

from src.user.schemas import (
    UserRequestEmailSchema,
    UserRequestPasswordResetSchema,
    UserSchema,
    UserResponseSchema,
)
from src.auth.schemas import TokenSchema

from src.user import service as users
from src.auth.services.auth import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/signup",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def register(
    body: UserSchema,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Register new user endpoint
    Create new user and send confirmation email

    :param body: user data
    :type body: UserSchema
    :param bt: background tasks
    :type bt: BackgroundTasks
    :param request: request
    :type request: Request
    :param db: database session
    :type db: AsyncSession

    :return: created user
    :rtype: User
    """
    exsisting_user = await users.get_user_by_email(body.email, db)
    if exsisting_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await users.create_user(body, db)
    return new_user


@router.post(
    "/login",
    response_model=TokenSchema,
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    Login user endpoint

    :param body: email and password
    :type body: OAuth2PasswordRequestForm
    :param db: database session
    :type db: AsyncSession

    :return: access and refresh tokens, token type
    :rtype: Token
    """
    user = await users.get_user_by_email(body.username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
        )
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )
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


@router.get(
    "/refresh_token",
    response_model=TokenSchema,
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: AsyncSession = Depends(get_db),
):
    """
    Refresh tokens endpoint

    :param credentials: Get current credentials use refresh token
    :type credentials: HTTPAuthorizationCredentials
    :param db: database session
    :type db: AsyncSession

    :return: access and refresh tokens, token type
    :rtype: Token
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user_db = await users.get_user_by_email(email, db)
    if user_db.refresh_token != token:
        await users.update_token(user_db, None, db)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    access_token = await auth_service.create_access_token(data={"sub": user_db.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user_db.email})
    await users.update_token(user_db, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/forget_password",
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))]
)
async def forget_password(
    body: UserRequestEmailSchema,
    # bt: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Forget password endpoint

    :param body: email
    :type body: UserRequestEmailSchema
    :param bt: background tasks
    :type bt: BackgroundTasks
    :param request: request
    :type request: Request
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
    # bt.add_task(
    #     send_password_reset_email,
    #     exsisting_user.email,
    #     exsisting_user.username,
    #     str(request.base_url),
    # )
    # return {"message": "Check your email for confirmation link"}
    reset_token = await auth_service.create_password_reset_token(exsisting_user.email)
    return {
        "message": "For reset password use this token in endpoint /reset_password",
        "token": reset_token,
    }


@router.post(
    "/reset_password",
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
