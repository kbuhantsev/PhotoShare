from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.photos.models import Photo
from src.photos.utils.cloudinary_utils import transform_file


async def transform(photo_id: int, transformations: dict, db: AsyncSession) -> dict | None:

    query = select(Photo).where(Photo.id == photo_id)
    res = await db.execute(query)
    photo = res.scalars().one_or_none()
    if not photo:
        return None

    result = transform_file(public_id=photo.public_id, transformations=transformations)

    return result
