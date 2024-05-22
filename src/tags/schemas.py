from typing import List, Optional

from pydantic import BaseModel

from src.schemas import ResponseModel


class TagSchema(BaseModel):
    id: Optional[int] = None
    name: str


class TagResponseSchema(ResponseModel):
    data: TagSchema = None


class TagsResponseSchema(ResponseModel):
    data: List[TagSchema] = []
