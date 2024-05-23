from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.logger import get_logger
from src.tags.dependencies import allowed_create_tag, allowed_delete_tag
from src.tags.schemas import TagResponseSchema, TagSchema, TagsResponseSchema
from src.tags.service import create_tag, delete_tag, get_tags

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


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TagResponseSchema,
)
async def create_tag_handler(
    response: Response,
    tag: TagSchema,
    db: AsyncSession = Depends(get_db),
    allowed: bool = Depends(allowed_create_tag),
):

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    try:
        tag_create = await create_tag(
            name=tag.name, db=db
        )
        if not tag_create:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while posting tag!",
            }
        return {"data": tag_create}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while posting tag!",
        }


@router.delete(
    "/{tag_id}",
    response_model=TagResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def delete_tag_handler(
        response: Response,
        tag_id: int,
        db: AsyncSession = Depends(get_db),
        allowed: bool = Depends(allowed_delete_tag),
):

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    try:
        tag = await delete_tag(tag_id=tag_id, db=db)
        if not tag:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while deleting tag!",
            }
        return {"data": tag}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while deleting tag!",
        }
