from pydantic import BaseModel
from src.schemas import ResponseModel
from typing import List


class CommentSchema(BaseModel):
    user_id: int
    photo_id: int
    comment: str


class CommentResponseSchema(ResponseModel):
    data: CommentSchema = None
