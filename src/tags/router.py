from fastapi import APIRouter
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import IntegrityError
from src.tags.schemas import TagCreate, TagResponse
from src.database import get_db
from src.tags.models import Tag

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/tags", response_model=List[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(Tag))
        tags = result.scalars().all()
    return tags
