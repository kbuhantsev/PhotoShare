from typing import Annotated, List

from fastapi import (
    APIRouter,
    Body,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.schemas import CommentsResponseSchema
from src.database import get_db
from src.dependencies import allowed_all, get_current_user
from src.photos.schemas import PhotosResponseSchema
from src.schemas import ResponseModel
from src.services.authentication import auth_service
from src.services.cloudinary_utils import build_url, upload_file
from src.user import service as users
from src.user.models import Role, User
from src.user.schemas import (
    UserAuthPasswordResetSchema,
    UserCurrentResponseSchema,
    UserProfileResponseSchema,
    UsersProfileResponseSchema,
    UsersRolesResponseSchema,
    UserUpdateSchema,
)

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
    Return current user

    :param user: current user
    :type user: User

    :return: current user
    :rtype: User
    """
    return {"data": user}


@router.put("/", response_model=UserCurrentResponseSchema)
async def update_user(
    body: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update user

    :param body: user data
    :type body: str
    :param db: database session
    :type db: AsyncSession
    :param user: current user
    :type user: User

    :return: updated user
    :rtype: User
    """
    # TODO
    updated_user = await users.update_user(user.email, body, db)
    return {"data": updated_user}


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
    Update user avatar

    :param file: user avatar
    :type file: UploadFile
    :param db: database session
    :type db: AsyncSession
    :param user: current user
    :type user: User

    :return: updated user
    :rtype: User
    """

    try:
        avatar = upload_file(file.file, "user_avatar", user.email)
        avatar_url = build_url(avatar.get("public_id"))
        result = await users.update_avatar_url(user.email, avatar_url, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": result}


@router.patch(
    "/reset_password",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
)
async def reset_password(
    body: UserAuthPasswordResetSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Reset user password

    :param body: email
    :type body: str
    :param db: database session
    :type db: AsyncSession
    :param user: current user
    :type user: User

    :return: message
    :rtype: dict
    """
    try:
        if body.new_password != body.confirm_password:
            raise HTTPException(status_code=400, detail="Passwords don't match")
        hashed_password = auth_service.get_password_hash(body.new_password)
        await users.update_password(user.email, hashed_password, db)
        return {"message": "Password updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/profile/{username}", response_model=UserProfileResponseSchema)
async def get_profile(
    response: Response, username: str, db: AsyncSession = Depends(get_db)
):
    """
    Get user profile

    :param response: response object
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
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
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
    response: Response,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get all users

    :param response: response object
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
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"status": "error", "message": str(e)}

    return {"data": users_data, "total": len(users_data)}


@router.get("/photos", response_model=PhotosResponseSchema)
async def get_user_photos(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get user photos

    :param user: user
    :type user: User
    :param skip: skip
    :type skip: int
    :param limit: limit
    :type limit: int
    :param db: database session

    :return: users photos
    :rtype: ResponseModel
    """

    try:
        photos = await users.get_user_photos(skip, limit, user, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": photos, "total": len(photos)}


@router.get("/comments", response_model=CommentsResponseSchema)
async def get_user_comments(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get user comments

    :param user: user
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
        comments = await users.get_user_comments(skip, limit, user, db)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": comments}


@router.get(
    "/roles",
    response_model=UsersRolesResponseSchema,
    dependencies=[Depends(allowed_all)],
)
async def get_users_roles(db: AsyncSession = Depends(get_db)):
    """
    Get users roles

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
    response: Response,
    changeable_user: Annotated[str, Form(description="email user to change")],
    role: Annotated[
        str, Form(description="select new role", enum=[curr_role.name for curr_role in Role])
    ],
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Change user role

    :param changeable_user: changeable user
    :param response: response object
    :param user: email user to change
    :type user: str
    :param role: new role
    :type role: Role
    :param db: database session

    :return: updated user
    :rtype: UserCurrentResponseSchema

    """
    try:
        changeable_user = await users.get_user_by_email(changeable_user, db)
        if changeable_user != user:
            change_user = await users.update_role(changeable_user, Role[role], db)
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"status": "error", "message": "You can't change your role"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"data": change_user}


@router.post(
    "/block",
    response_model=UserCurrentResponseSchema,
    dependencies=[Depends(allowed_all)],
)
async def block_user_handler(
    response: Response,
    blocked_user: Annotated[str, Form(description="email user to block")],
    block: Annotated[bool, Form(description="Flag to block or unblock user")],
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Block user

    :param response: response object
    :param blocked_user: user to block
    :type user: str
    :param block: flag to block or unblock user
    :type block: bool
    :param db: database session

    """
    try:
        blocked_user = await users.get_user_by_email(blocked_user, db)
        if blocked_user != user:
            block_user = await users.block_user(user, block, db)
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return {"status": "error", "message": "You can't block yourself"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {
        "data": block_user,
        "message": f"user `{block_user.username}` {'blocked' if block else 'unblocked'}",
    }
