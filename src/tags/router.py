from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from src.tags.schemas import TagResponse
from src.database import get_db
from src.tags.models import Tag

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/tags_all", response_model=List[TagResponse])
async def get_tags_all(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Tag))
        tags = result.scalars().all()
    return tags
