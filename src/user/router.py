import os
from typing import Annotated, List, Literal
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user, allowed_all

from src.database import get_db
from src.user.models import User, Role
from src.user.schemas import (
    UserCurrentResponseSchema,
    UserProfileResponseSchema,
    UsersProfileResponseSchema,
    UsersRolesResponseShema,
)
from src.photos.schemas import PhotosResponseSchema
from src.comments.schemas import CommentResponseSchema
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
async def get_current_user_data(user: User = Depends(get_current_user)):
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
    dependencies=[Depends(allowed_all)],
)
async def get_all_users(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    """
    Get all users endpoint

    :param db: database session
    :type db: AsyncSession
    :param user: current user
    :type user: User

    :return: all users
    :rtype: UsersProfileResponseSchema
    """

    try:
        users_data = await users.get_all_users(db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": users_data, "total": len(users_data)}


@router.get("/photos", response_model=PhotosResponseSchema)
async def get_users_photos(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get users photos endpoint

    :param skip: skip
    :type skip: int
    :param limit: limit
    :type limit: int
    :param db: database session

    :return: users photos
    :rtype: ResponseModel
    """

    try:
        photos = await users.get_users_photos(skip, limit, user, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": photos, "total": len(photos)}


@router.get("/comments", response_model=CommentResponseSchema)
async def get_users_comments(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get users comments endpoint

    :param skip: skip
    :type skip: int
    :param limit: limit
    :type limit: int
    :param db: database session

    :return: users comments
    :rtype: ResponseModel
    """

    # TODO
    try:
        comments = await users.get_users_comments(skip, limit, user, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": comments}


@router.post(
    "/block",
    response_model=UserCurrentResponseSchema,
    dependencies=[Depends(allowed_all)],
)
async def block_user(
    user: Annotated[str, Form(description="email user to block")],
    block: Annotated[bool, Form()],
    db: AsyncSession = Depends(get_db),
):
    """
    Block user endpoint

    :param user: current user
    :type user: User
    :param db: database session

    """
    try:
        block_user = await users.block_user(user, block, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {
        "data": block_user,
        "message": f"user `{user.username}` {'blocked' if block else 'unblocked'}",
    }


@router.get(
    "/roles",
    response_model=UsersRolesResponseShema,
    dependencies=[Depends(allowed_all)],
)
async def get_users_roles(db: AsyncSession = Depends(get_db)):
    """
    Get users roles endpoint

    :param db: database session
    :type db: AsyncSession

    :return: users roles
    :rtype: List[Role]
    """
    return {"data": [role.name for role in Role]}


@router.post(
    "/change_role",
    response_model=UserCurrentResponseSchema,
    dependencies=[Depends(allowed_all)],
)
async def change_role(
    user: Annotated[str, Form(description="email user to change")],
    role: Annotated[
        str, Form(description="select new role", enum=[role.name for role in Role])
    ],
    db: AsyncSession = Depends(get_db),
):
    """
    Change user role endpoint

    :param user: email user to change
    :type user: str
    :param role: new role
    :type role: Role
    :param db: database session

    :return: updated user
    :rtype: UserCurrentResponseSchema

    """
    try:
        change_role = await users.update_role(user, Role[role], db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": change_role}
