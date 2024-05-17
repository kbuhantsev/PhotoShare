from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.services.authentication import auth_service


async def get_current_user(token: Annotated[str, Depends(auth_service.oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]):
    return await auth_service.get_current_user(token=token, db=db)
