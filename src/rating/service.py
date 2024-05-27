from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.rating.models import Rating


async def create_update_rating(db: AsyncSession, photo_id: int, user_id: int, rating: int):

    result = await db.execute(select(Rating).where(
        and_(Rating.user_id == user_id, Rating.photo_id == photo_id)
    ))
    db_rating = result.scalars().first()

    if db_rating:
        db_rating.rating = rating
        await db.commit()
        await db.refresh(db_rating)
        return db_rating
    else:
        db_rating = Rating(
            photo_id=photo_id,
            user_id=user_id,
            rating=rating
        )

    db.add(db_rating)
    await db.commit()
    await db.refresh(db_rating)
    return db_rating


async def delete_rating(db: AsyncSession, photo_id: int, user_id: int):

    result = await db.execute(select(Rating).where(
        and_(Rating.user_id == user_id, Rating.photo_id == photo_id)
    ))
    db_rating = result.scalars().first()

    await db.delete(db_rating)
    await db.commit()

    return db_rating


async def get_average_rating(db: AsyncSession, photo_id: int):
    result = await db.execute(select(Rating).where(Rating.photo_id == photo_id))
    ratings = result.scalars().all()
    if not ratings:
        return 0
    return sum([rating.rating for rating in ratings]) / len(ratings)
