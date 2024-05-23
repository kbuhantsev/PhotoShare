from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.comments.service as comment_services
from src.comments.schemas import (
    CommentSchema,
    CommentResponseSchema,
    CommentsResponseSchema,
)

from src.database import get_db
from src.dependencies import allowed_delete_comments, get_current_user
from src.logger import get_logger
from src.user.models import User

logger = get_logger("Comments")

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponseSchema,
    description="No more than 15 requests per minute",
)
async def create_comment_handler(
    response: Response,
    comment: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new comment.

    :param response: The response object.
    :type response: Response
    :param comment: The comment to be created.
    :type comment: CommentSchema
    :param db: The database session.
    :type db: AsyncSession
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The created comment.
    :rtype: CommentResponseSchema
    """
    try:
        comment_create = await comment_services.create_comment(
            comment=comment, db=db, current_user=current_user
        )
        if not comment_create:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while posting the comment!",
            }
        return {"data": comment_create}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while posting the comment!",
        }


@router.get(
    "/{photo_id}", status_code=status.HTTP_200_OK, response_model=CommentsResponseSchema
)
async def get_comments_handler(
    photo_id: int, response: Response, db: AsyncSession = Depends(get_db)
):
    """
    Get comments for a photo.

    :param photo_id: The ID of the photo.
    :type photo_id: int
    :param response: The response object.
    :type response: Response
    :param db: The database session.
    :type db: AsyncSession
    :return: The comments for the photo.
    :rtype: CommentResponseSchema
    """
    try:
        comments = await comment_services.get_comments(photo_id=photo_id, db=db)
        if not comments:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while getting comments!",
            }
        return {"data": comments}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while getting comments!",
        }


@router.put(
    "/{comment_id}",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_comment_handler(
    response: Response,
    comment_id: int,
    comment: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a comment.

    :param response: The response object.
    :type response: Response
    :param comment_id: The ID of the comment to be updated.
    :type comment_id: int
    :param comment: The updated comment text.
    :type comment: str
    :param db: The database session.
    :type db: AsyncSession
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The updated comment.
    :rtype: CommentResponseSchema
    """
    try:
        updated_comment = await comment_services.update_comment(
            comment_id=comment_id, comment=comment, db=db, current_user=current_user
        )
        if not updated_comment:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while updating comment",
            }
        return {"data": updated_comment}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while updating comment",
        }


@router.delete(
    "/{comment_id}",
    response_model=CommentResponseSchema,
    dependencies=[Depends(allowed_delete_comments)],
)
async def delete_comment_handler(
    response: Response, comment_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Delete a comment.

    :param response: The response object.
    :type response: Response
    :param comment_id: The ID of the comment to be deleted.
    :type comment_id: int
    :param db: The database session.
    :type db: AsyncSession
    :return: The deleted comment.
    :rtype: CommentResponseSchema
    """
    try:
        deleted_comment = await comment_services.delete_comment(
            comment_id=comment_id, db=db
        )
        if not deleted_comment:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while deleting comment",
            }
        return {"data": deleted_comment}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while deleting comment",
        }
