import os
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import ResponseModel
from src.dependencies import get_current_user

from src.database import get_db
from src.user.models import User
from src.user.schemas import UserCurrentResponseSchema, UserProfileResponseSchema, UsersProfileResponseSchema
from src.user import service as users
from src.services.cloudinary_utils import upload_file

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get(
    "/current",
    response_model=UserCurrentResponseSchema,
    # dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
async def get_current_user(user: User = Depends(get_current_user)):
    """
    Return current user endpoint

    :param user: current user
    :type user: User

    :return: current user
    :rtype: User
    """
    return {"data": user}


@router.patch(
    "/avatar",
    response_model=UserCurrentResponseSchema,
    # dependencies=[Depends(RateLimiter(times=1, seconds=10))],
)
async def update_avatar(
    file: UploadFile = File(),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update user avatar endpoint

    :param file: user avatar
    :type file: UploadFile
    :param db: database session
    :type db: AsyncSession
    :param user: current user
    :type user: User

    :return: updated user
    :rtype: User
    """

    n = os.path.splitext(file.filename)
    # public_id = f"Contacts API/{user.email}"
    avatar_url = upload_file(file, "user_avatar")
    return await users.update_avatar_url(user.email, avatar_url, db)


@router.get("/profile/{username}", response_model=UserProfileResponseSchema)
async def get_profile(username: str, db: AsyncSession = Depends(get_db)):
    """
    Get user profile endpoint

    :param username: user username
    :type username: str
    :param db: database session
    :type db: AsyncSession

    :return: user profile
    :rtype: UserProfileResponseSchema
    """

    try:
        user_data = await users.get_user_profile(username, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return {"data": user_data}


@router.get(
    "/",
    response_model=UsersProfileResponseSchema,
    # dependencies=[Depends(allow_read_all_users)],
)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """
    """

    try:
        users_data = await users.get_all_users(db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": users_data, "total": len(users_data)}
