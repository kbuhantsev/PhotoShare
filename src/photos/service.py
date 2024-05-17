from typing import BinaryIO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.photos.models import Photo
from src.photos.utils import upload_file, delete_file
from src.tags.models import Tag
from src.user.models import User


async def create_photo(
    *,
    title: str,
    file: BinaryIO,
    description: str,
    tags: list[str],
    db: AsyncSession,
    current_user: User
) -> Photo | None:

    asset = upload_file(file, folder="photos")

    photo = Photo(
        title=title,
        description=description,
        owner_id=current_user.id,
        public_id=asset.get("public_id"),
        secure_url=asset.get("secure_url"),
        folder="photos",
    )

    tags_arr = []

    if tags:
        for tag in tags:
            query = select(Tag).where(Tag.name == tag)
            res = await db.execute(query)
            tag_obj = res.scalars().one_or_none()
            if tag_obj:
                tags_arr.append(tag_obj)
            else:
                new_tag = Tag(name=tag)
                tags_arr.append(new_tag)

        await db.commit()
        await db.flush()

        photo.tags = tags_arr

    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


async def update_photo(
    *,
    photo_id: int,
    title: str,
    file: BinaryIO,
    description: str,
    tags: list[str],
    db: AsyncSession,
    current_user: User
) -> Photo | None:

    query = select(Photo).where(Photo.id == photo_id)
    res = await db.execute(query)
    photo = res.scalars().first()
    if not photo:
        return None

    asset = await upload_file(file, folder="photos")
    photo.title = title
    photo.description = description
    photo.public_id = asset.get("public_id")
    photo.secure_url = asset.get("secure_url")
    photo.folder = "photos"
    photo.tags = [Tag(name=tag) for tag in tags]
    await db.commit()
    await db.refresh(photo)
    return photo


async def delete_photo(*, photo_id: int, db: AsyncSession) -> Photo | None:
    query = select(Photo).where(Photo.id == photo_id)
    res = await db.execute(query)
    photo = res.scalars().one_or_none()
    if not photo:
        return None

    deleted = await delete_file(public_id=photo.public_id)
    if not deleted:
        return None

    await db.delete(photo)
    await db.commit()

    return photo


async def get_photos(skip: int, limit: int, db: AsyncSession) -> list[Photo]:
    query = select(Photo).offset(skip).limit(limit)
    res = await db.execute(query)
    return list(res.scalars().all())


async def get_photo(*, photo_id: int, db: AsyncSession) -> Photo | None:
    query = select(Photo).where(Photo.id == photo_id)
    res = await db.execute(query)
    return res.scalars().one_or_none()
