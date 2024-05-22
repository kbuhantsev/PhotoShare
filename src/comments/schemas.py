from typing import List

from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel

from datetime import datetime


class CommentSchema(BaseModel):
    id: int | None = None
    user_id: int
    photo_id: int
    comment: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class CommentResponseSchema(ResponseModel):
    data: CommentSchema = None


class CommentsResponseSchema(ResponseModel):
    data: List[CommentSchema] = []
