from typing import BinaryIO
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User


async def create_photo(
    *,
    title: str,
    file: BinaryIO,
    description: str,
    tags: list[str],
    db: AsyncSession,
    current_user: User
):
    pass


async def update_photo(*, photo_id: int):
    pass


async def delete_photo(*, photo_id: int):
    pass


async def get_photos():
    pass


async def get_photo(*, photo_id: int):
    pass
