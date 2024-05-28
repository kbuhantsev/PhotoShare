from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tags.models import Tag


async def get_tags(db: AsyncSession) -> list[Tag]:
    """
    Retrieve all tags.

    :param db: Database session dependency.
    :param db: AsyncSession
    :return: list of tags
    """
    result = await db.execute(select(Tag))
    return list(result.scalars().all())


async def create_tag(name:str, db: AsyncSession) -> Tag:
    """
    Create a new tag.

    :param name: Name of the tag to be created.
    :type name: str
    :param db: Database session dependency.
    :type db: AsyncSession
    :return: A TagModel instance indicating the result of the create operation.
    """
    tag = Tag(name=name)

    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_tag(tag_id: int, db: AsyncSession) -> Tag | None:
    """
    Delete an existing tag.

    :param tag_id: ID of the tag to be deleted.
    :type tag_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :return: A TagModel instance indicating the result of the delete operation.
    :rtype: TagModel
    """
    result = await db.execute(select(Tag).filter(Tag.id == tag_id))
    tag = result.scalar_one_or_none()

    if not tag:
        return None

    await db.delete(tag)
    await db.commit()
    return tag
