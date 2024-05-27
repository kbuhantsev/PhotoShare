from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user
from src.logger import get_logger
from src.rating.schemas import RatingResponseSchema, RatingSchema, RatingAverageResponseSchema
from src.user.models import User
from src.rating.service import create_update_rating, delete_rating, get_average_rating

logger = get_logger("Rating")

router = APIRouter(
    prefix="/rating",
    tags=["Rating"],
)


@router.get(
    "/{photo_id}", status_code=status.HTTP_200_OK, response_model=RatingAverageResponseSchema
)
async def get_rating_handler(
    response: Response,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
):
    try:
        average_rating = await get_average_rating(db=db, photo_id=photo_id)
        return {"data": {"rating": average_rating, "photo_id": photo_id}}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while getting rating!",
        }


@router.post(
    "/{photo_id}", status_code=status.HTTP_200_OK, response_model=RatingResponseSchema
)
async def set_rating_handler(
    response: Response,
    photo_id: int,
    rating: RatingSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        rating_create = await create_update_rating(
            db=db, user_id=current_user.id, photo_id=photo_id, rating=rating.rating
        )
        if not rating_create:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while creating rating!",
            }
        return {"data": rating_create}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while creating rating!",
        }


@router.delete("/{photo_id}", status_code=status.HTTP_200_OK)
async def delete_rating_handler(
    response: Response,
    photo_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        rating_delete = await delete_rating(
            db=db, user_id=current_user.id, photo_id=photo_id
        )
        if not rating_delete:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status": "error",
                "message": "An error occurred while deleting rating!",
            }
        return {"data": rating_delete}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while deleting rating!",
        }
