from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.photos.models import Photo, Transformation
from src.services.cloudinary_utils import transform_file, upload_file


async def transform(
    photo_id: int, transformations: dict, db: AsyncSession
) -> dict | None:

    query = select(Photo).where(Photo.id == photo_id)
    res = await db.execute(query)
    photo = res.scalars().one_or_none()
    if not photo:
        return None

    result = transform_file(public_id=photo.public_id, transformations=transformations)

    return result


async def save_transform(
    photo_id: int, url: str, db: AsyncSession
) -> Transformation | None:

    asset = upload_file(file=url, folder="transformations")

    transformation = Transformation(
        photo_id=photo_id,
        title=asset.get("original_filename"),
        public_id=asset.get("public_id"),
        secure_url=asset.get("secure_url"),
        folder=asset.get("folder"),
    )

    db.add(transformation)
    await db.commit()
    await db.refresh(transformation)
    return transformation
