from pydantic import BaseModel
from src.schemas import ResponseModel
from typing import List, Optional


class CommentSchema(BaseModel):
    user_id: Optional[int]
    photo_id: Optional[int]
    comment: Optional[str]


class CommentResponseSchema(ResponseModel):
    data: List[CommentSchema] = None
