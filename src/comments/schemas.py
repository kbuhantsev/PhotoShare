from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel


class CommentSchema(BaseModel):
    photo_id: int
    comment: str

    model_config = ConfigDict(from_attributes=True)


class CommentResponseSchema(ResponseModel):

    class Data(CommentSchema):
        id: int
        user_id: int
        created_at: datetime
        updated_at: datetime


class CommentsResponseSchema(ResponseModel):

    data: List[CommentResponseSchema.Data] = []
