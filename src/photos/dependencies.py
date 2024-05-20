from pprint import pprint

from fastapi import Depends, Request

from src.database import get_db
from src.dependencies import get_current_user
from src.photos.service import get_photo
from src.user.models import Role, User

from sqlalchemy.ext.asyncio import AsyncSession


async def allowed_delete_photo(
    request: Request,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):

    pprint(request)
    is_admin = user.role == Role.ADMIN
    if is_admin:
        return True

    photo_id = request.path_params.get("photo_id")
    photo = await get_photo(photo_id=photo_id, db=db)
    if user.id == photo.owner_id:
        return True

    return False
