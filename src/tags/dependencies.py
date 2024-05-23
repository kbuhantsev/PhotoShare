from fastapi import Depends

from src.dependencies import get_current_user
from src.user.models import Role, User


async def allowed_create_tag(
    user: User = Depends(get_current_user),
):

    allowed = (
        user.role == Role.ADMIN or user.role == Role.MODERATOR or user.role == Role.USER
    )
    if allowed:
        return True

    return False


async def allowed_delete_tag(
    user: User = Depends(get_current_user),
):

    is_admin = user.role == Role.ADMIN
    if is_admin:
        return True

    return False
