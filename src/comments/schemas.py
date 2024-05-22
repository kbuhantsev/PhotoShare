from typing import List, Optional

from pydantic import BaseModel

from src.schemas import ResponseModel

from datetime import datetime


class CommentSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    photo_id: int
    comment: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CommentResponseSchema(ResponseModel):
    data: CommentSchema = None


class CommentsResponseSchema(ResponseModel):
    data: List[CommentSchema] = []
