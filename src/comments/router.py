from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database import get_db
from src.comments.models import Comment
from datetime import datetime
from src.comments.schemas import CommentModel, CommentCreate, CommentUpdate
from typing import List, Union
from src.auth.dependencies import get_current_user
from src.user.models import User
router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)



#TODO Додати обмеження на кількіть запитів
@router.post("/", response_model=CommentModel, description="No more than 15 requests per minute")
async def create_comment(photo_id:int, comment: CommentCreate, db: Session = Depends(get_db),
                         current_user : User = Depends(get_current_user)):
    try:
        db_comment = Comment(comment=comment, photo_id=photo_id, user_id=current_user.id)
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return {"status": 'ok', "message":" ", "data": comment}

    except Exception as e:
        return {"status": 'error', "message":e, "data": comment}

@router.get('/{photo_id}', response_model=List[CommentModel])
async def get_comments(photo_id: int, db:Session = Depends(get_db),
                       current_user : User = Depends(get_current_user)):
    try:
        comments = await db.query(Comment).filter(Comment.photo_id == photo_id).all()
        return {"status": 'ok', "message":" ", "data": [comment for comment in comments]}
    except Exception as e:
        return {"status": 'error', "message":e, "data": " "}

@router.put("/{comment_id}", response_model=CommentModel)
async def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db),
                         current_user : User = Depends(get_current_user)):
    try:
        db_comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == current_user.id))
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db_comment.comment = comment.comment
        db_comment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_comment)
        return {"status": 'ok', "message":" ", "data": comment}

    except Exception as e:
        return {"status": 'error', "message":e, "data": comment}

@router.delete('/{comment_id}', response_model=CommentModel)
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         current_user : User = Depends(get_current_user)):
    try:
        if current_user.role != 1 and current_user.role != 2:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Only administrators and moderators can delete comments")
        db_comment = db.query(Comment).filter(Comment.id == comment_id)
        if not db_comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db.delete(db_comment)
        db.commit()
        return {"status": 'ok', "message":" ", "data": None}
    except Exception as e:
        return {"status": 'error', "message": e, "data": None}
