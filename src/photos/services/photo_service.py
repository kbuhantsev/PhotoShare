from typing import BinaryIO

from sqlalchemy import select, func, or_, RowMapping, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.photos.models import Photo
from src.photos.utils.cloudinary_utils import delete_file, upload_file
from src.tags.models import Tag, PhotoToTag
from src.user.models import User


async def create_photo(
    *,
    title: str,
    file: BinaryIO,
    description: str,
    tags: list[str],
    db: AsyncSession,
    current_user: User,
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
) -> RowMapping | None:
    query = select(Photo).where(Photo.id == photo_id).options(selectinload(Photo.tags))
    res = await db.execute(query)
    photo = res.scalars().first()
    if not photo:
        return None

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

    if len(tags_arr) > 0:
        photo.tags = tags_arr

    if title:
        photo.title = title
    if description:
        photo.description = description
    if file:
        asset = upload_file(file, folder="photos")
        photo.public_id = asset.get("public_id")
        photo.secure_url = asset.get("secure_url")
        photo.folder = "photos"

    await db.commit()
    await db.refresh(photo)
    return photo


async def delete_photo(*, photo_id: int, db: AsyncSession) -> RowMapping | None:
    query = select(Photo).where(Photo.id == photo_id).options(selectinload(Photo.tags))
    res = await db.execute(query)
    photo = res.scalars().one_or_none()
    if not photo:
        return None

    deleted = delete_file(public_id=photo.public_id)
    if not deleted:
        return None

    await db.delete(photo)
    await db.commit()

    return photo


async def get_photos(
    skip: int, limit: int, query: str, db: AsyncSession
) -> list[Photo]:

    if query:
        statement = get_search_statement(query, skip, limit)
        res = await db.execute(statement)

        return list(res.scalars().all())
    else:
        statement = select(Photo).offset(skip).limit(limit).options(selectinload(Photo.tags))
        res = await db.execute(statement)
        return list(res.scalars().all())


async def get_photos_count(query: str, db: AsyncSession) -> int:
    if query:
        statement = get_search_statement(query)
        res = await db.execute(statement)
        total = len(res.scalars().all())
    else:
        query = select(func.count(Photo.id))
        res = await db.execute(query)
        total = res.scalar()

    return total


async def get_photo(*, photo_id: int, db: AsyncSession) -> RowMapping | None:
    query = (select(Photo).
             where(Photo.id == photo_id).
             options(selectinload(Photo.tags))
    )
    res = await db.execute(query)
    return res.scalars().one_or_none()


def get_search_statement(query: str, skip: int = 0, limit: int = 50) -> Select:
    statement = (
        select(Photo)
        .join(PhotoToTag, Photo.id == PhotoToTag.photo_id)
        .join(Tag, Tag.id == PhotoToTag.tag_id)
        .where(or_(Tag.name.ilike(f"%{query}%"), Photo.title.ilike(f"%{query}%")))
        .offset(skip)
        .limit(limit)
        .options(selectinload(Photo.tags))
    )
    return statement
