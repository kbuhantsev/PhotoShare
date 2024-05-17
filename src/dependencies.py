from typing import Annotated
from fastapi import Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.services.authentication import auth_service
from src.services.roles import RolesAccess
from src.user.models import Role, User


async def get_current_user(
    token: Annotated[str, Depends(auth_service.oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await auth_service.get_current_user(token=token, db=db)


async def allowed_delite_comments(
    request: Request, user: User = Depends(get_current_user)
):
    return await RolesAccess(allowed_roles=[Role.ADMIN])(request, user=user)
