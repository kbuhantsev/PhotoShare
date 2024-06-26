from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.models import Comment
from src.comments.schemas import CommentSchema
from src.user.models import User


async def create_comment(
    comment: CommentSchema,
    db: AsyncSession,
    current_user: User,
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

    return db_comment


async def get_comments(photo_id: int, db: AsyncSession) -> list[Comment]:
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
    db: AsyncSession,
    current_user: User,
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
    db_comment.comment = comment
    await db.commit()
    await db.refresh(db_comment)

    return db_comment


async def delete_comment(comment_id: int, db: AsyncSession) -> Comment | None:
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
    result = await db.execute(select(Comment).filter(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()

    await db.delete(db_comment)
    await db.commit()
    return db_comment
