from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlalchemy import and_, select
from src.database import get_db
from src.comments.models import Comment
from datetime import datetime
from src.comments.schemas import CommentModel, CommentCreate, CommentUpdate
from typing import List
from src.dependencies import get_current_user
from src.user.models import User


async def create_comment(
    photo_id: int,
    comment: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CommentModel:
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
    try:
        db_comment = Comment(
            comment=comment, photo_id=photo_id, user_id=current_user.id
        )
        db.add(db_comment)
        await db.commit()
        await db.refresh(db_comment)
        return CommentModel(status="ok", message=" ", data=[db_comment])

    except Exception as e:
        return CommentModel(status="error", message=e, data=[])


async def get_comments(
    photo_id: int, db: AsyncSession = Depends(get_db)
) -> List[CommentModel]:
    """
    Retrieve all comments for a specific photo.

    :param photo_id: ID of the photo whose comments are to be retrieved.
    :type photo_id: int
    :param db: Database session dependency.
    :type db: AsyncSession
    :return: A CommentModel instance containing a list of comments for the specified photo.
    :rtype: CommentModel
    """
    try:
        result = await db.execute(select(Comment).filter(Comment.photo_id == photo_id))
        comments = result.scalars().all()
        return CommentModel(
            status="ok", message=" ", data=[comment for comment in comments]
        )
    except Exception as e:
        return CommentModel(status="error", message=str(e), data=[])


async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CommentModel:
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
    try:
        result = await db.execute(
            select(Comment).filter(
                and_(Comment.id == comment_id, Comment.user_id == current_user.id)
            )
        )
        db_comment = result.scalar_one_or_none()
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db_comment.comment = comment.comment
        db_comment.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_comment)
        return CommentModel(status="ok", message=" ", data=[db_comment])

    except Exception as e:
        return CommentModel(status="error", message=str(e), data=[])


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
    try:
        if current_user.role != 1 and current_user.role != 2:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators and moderators can delete comments",
            )
        result = await db.execute(select(Comment).filter(Comment.id == comment_id))
        db_comment = result.scalar_one_or_none()
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await db.delete(db_comment)
        await db.commit()
        return CommentModel(status="ok", message=" ", data=[])
    except Exception as e:
        return CommentModel(status="error", message=str(e), data=[])
