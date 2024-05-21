from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.photos.models import Photo, Transformation, QrCode
from src.photos.utils.qrcode_utils import create_qr_code
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
    await db.flush()
    await db.refresh(transformation)

    return transformation


async def get_qr_code(transformation_id: int, url: str, db: AsyncSession) -> QrCode | None:

    qr_asset = create_qr_code(url=url)
    if qr_asset:
        qr = QrCode(
            transformation_id=transformation_id,
            title=qr_asset.get("original_filename"),
            public_id=qr_asset.get("public_id"),
            secure_url=qr_asset.get("secure_url"),
            folder=qr_asset.get("folder"),
        )

        db.add(qr)
        await db.commit()
        await db.refresh(qr)

        return qr

    return None
