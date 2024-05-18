from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_, select
from src.database import get_db
from src.comments.models import Comment
from datetime import datetime
from src.comments.schemas import CommentSchema, CommentResponseSchema
from typing import List
from src.dependencies import get_current_user
from src.user.models import User
from src.user.models import Role

async def create_comment(
    photo_id: int,
    comment: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Comment | None:
    """
    Create a new comment for a photo.

    :param photo_id: ID of the photo to which the comment is associated.
    :type photo_id: int
    :param comment: Data required to create a new comment.
    :type comment: CommentCreate
    :param db: Database session dependency.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: A CommentModel instance with the created comment data.
    :rtype: CommentModel
    """
    db_comment = Comment(
        comment=comment.comment, photo_id=comment.photo_id, user_id=current_user.id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)

    return comment


async def get_comments(
    photo_id: int, db: AsyncSession = Depends(get_db)
) -> list[Comment]:
    """
    Retrieve all comments for a specific photo.

    :param photo_id: ID of the photo whose comments are to be retrieved.
    :type photo_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :return: A CommentModel instance containing a list of comments for the specified photo.
    :rtype: Comment
    """
    result = await db.execute(select(Comment).filter(Comment.photo_id == photo_id))
    return list(result.scalars().all())

async def update_comment(
    comment_id: int,
    comment: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Comment | None:
    """
    Update an existing comment.

    :param comment_id: ID of the comment to be updated.
    :type comment_id: int
    :param comment: Data required to update the comment.
    :type comment: CommentUpdate
    :param db: Database session dependency.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: A CommentModel instance with the updated comment data.
    :rtype: CommentModel
    """

    result = await db.execute(
        select(Comment).filter(
            and_(Comment.id == comment_id, Comment.user_id == current_user.id)
        )
    )
    db_comment = result.scalar_one_or_none()
    # if not db_comment:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_comment.comment = comment
    db_comment.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_comment)

    return db_comment


async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete an existing comment.

    :param comment_id: ID of the comment to be deleted.
    :type comment_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :param current_user: Current authenticated user.
    :type current_user: User
    :return: A CommentModel instance indicating the result of the delete operation.
    :rtype: CommentModel
    """
    if current_user.role != Role.ADMIN and current_user.role != Role.MODERATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators and moderators can delete comments",
        )
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    # if not db_comment:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await db.delete(db_comment)
    await db.commit()
    return db_comment
