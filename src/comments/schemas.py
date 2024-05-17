from pydantic import BaseModel
from src.schemas import ResponseModel
from typing import List


class CommentModel(ResponseModel):
    data: List = []


class CommentCreate(BaseModel):
    comment: str


class CommentUpdate(BaseModel):
    comment: str
