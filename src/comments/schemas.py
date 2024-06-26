from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel
from src.user.schemas import UserProfileInfoResponseSchema


class CommentSchema(BaseModel):
    photo_id: int
    comment: str

    model_config = ConfigDict(from_attributes=True)


class CommentResponseInstanceSchema(CommentSchema):
    id: int
    user: UserProfileInfoResponseSchema
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentResponseSchema(ResponseModel):

    class Data(CommentSchema):
        id: int
        user: UserProfileInfoResponseSchema
        created_at: datetime
        updated_at: datetime

    data: Data = None


class CommentsResponseSchema(ResponseModel):

    data: List[CommentResponseSchema.Data] = []
    total: int = 0
