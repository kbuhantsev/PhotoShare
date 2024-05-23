from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.tags.schemas import TagsResponseSchema
from src.tags.service import get_tags

from src.logger import get_logger

logger = get_logger("Comments")

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/", response_model=TagsResponseSchema, status_code=status.HTTP_200_OK)
async def get_tags_handler(response: Response, db: AsyncSession = Depends(get_db)):

    try:
        tags = await get_tags(db)
        if not tags:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while getting tags!",
            }

        return {"data": tags}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while getting tags!",
        }
