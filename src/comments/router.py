from fastapi import APIRouter, Depends
from src.database import get_db
from src.comments.schemas import CommentModel, CommentCreate, CommentUpdate
from typing import List
from src.auth.dependencies import get_current_user
from src.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import src.comments.service as comment_services

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)



#TODO Додати обмеження на кількіть запитів
@router.post("/", response_model=CommentModel, description="No more than 15 requests per minute")
async def create_comment(photo_id:int, comment: CommentCreate, db:AsyncSession= Depends(get_db),
                         current_user : User = Depends(get_current_user)):

    comment_create = await comment_services.create_comment(photo_id=photo_id, comment=comment, db=db, current_user=current_user)
    return comment_create

@router.get('/{photo_id}', response_model=List[CommentModel])
async def get_comments(photo_id: int, db: AsyncSession = Depends(get_db)):
    comment_get = await comment_services.get_comments(photo_id=photo_id, db= db)
    return comment_get


@router.put("/{comment_id}", response_model=CommentModel)
async def update_comment(comment_id: int, comment: CommentUpdate, db: AsyncSession = Depends(get_db),
                         current_user : User = Depends(get_current_user)):

    updated_comment = comment_services.update_comment(comment_id=comment_id, comment=comment,
                                                      db=db,current_user=current_user)
    return updated_comment


@router.delete('/{comment_id}', response_model=CommentModel)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db),
                         current_user : User = Depends(get_current_user)):

    deleted_comment = comment_services.delete_comment(comment_id=comment_id, db=db, current_user=current_user)
    return deleted_comment