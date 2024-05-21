from fastapi import Depends, Request

from src.database import get_db
from src.dependencies import get_current_user
from src.photos.services.photo_service import get_photo
from src.user.models import Role, User

from sqlalchemy.ext.asyncio import AsyncSession


async def allowed_edit_photo(
    request: Request,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    has_permission = (user.role == Role.ADMIN or user.role == Role.MODERATOR)
    if has_permission:
        return True

    photo_id = request.path_params.get("photo_id")
    if not photo_id:
        return False

    photo = await get_photo(photo_id=int(photo_id), db=db)
    if user.id == photo.owner_id:
        return True

    return False


async def allowed_delete_photo(
    request: Request,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    is_admin = user.role == Role.ADMIN
    if is_admin:
        return True

    photo_id = request.path_params.get("photo_id")
    if not photo_id:
        return False

    photo = await get_photo(photo_id=int(photo_id), db=db)
    if user.id == photo.owner_id:
        return True

    return False
