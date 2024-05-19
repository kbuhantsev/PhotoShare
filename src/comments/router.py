from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.comments.service as comment_services
from src.comments.schemas import CommentResponseSchema, CommentSchema
from src.database import get_db
from src.dependencies import allowed_delite_comments, get_current_user
from src.user.models import User

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


# TODO Додати обмеження на кількіть запитів
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CommentResponseSchema,
    description="No more than 15 requests per minute"
)
async def create_comment_handler(
        response: Response,
        photo_id: int,
        comment: CommentSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    response_model = CommentResponseSchema()
    try:
        comment_create = await comment_services.create_comment(
            photo_id=photo_id, comment=comment, db=db, current_user=current_user
        )

    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while posting the comment"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model

    response = CommentResponseSchema()
    response.data = comment_create
    return response


@router.get("/{photo_id}", status_code=status.HTTP_200_OK, response_model=CommentResponseSchema)
async def get_comments_handler(photo_id: int, response: Response, db: AsyncSession = Depends(get_db)):
    response_model_instance = CommentResponseSchema()
    try:
        comment_get = await comment_services.get_comments(photo_id=photo_id, db=db)
    except Exception as e:
        print(e)
        response_model_instance.status = "error"
        response_model_instance.message = "An error occurred while getting comments from this photo"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model_instance

    response = CommentResponseSchema()
    response.data = comment_get
    return response


@router.put("/{comment_id}", response_model=CommentResponseSchema, status_code=status.HTTP_200_OK)
async def update_comment_handler(
        response: Response,
        comment_id: int,
        comment: str,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    response_model = CommentResponseSchema()
    try:
        updated_comment = await comment_services.update_comment(
            comment_id=comment_id, comment=comment, db=db, current_user=current_user
        )
    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while updating this comment"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model.dict()

    if not updated_comment:
        response_model.status = "error"
        response_model.message = "An error occurred while updating this comment"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model.dict()

    response = CommentResponseSchema()
    response.data = [updated_comment] if updated_comment is not None else []

    return response.dict()


@router.delete("/{comment_id}", response_model=CommentResponseSchema, dependencies=[Depends(allowed_delite_comments)])
async def delete_comment_handler(
        response: Response,
        comment_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),

):
    response_model = CommentResponseSchema()
    try:
        deleted_comment = await comment_services.delete_comment(
            comment_id=comment_id, db=db, current_user=current_user
        )
    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while deleting this comment"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model

    if not deleted_comment:
        response_model.status = "error"
        response_model.message = "An error occurred while deleting this comment"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model

    response = CommentResponseSchema()
    response.data = [deleted_comment] if deleted_comment is not None else []

    return response
