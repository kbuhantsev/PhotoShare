from typing import List

from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel


class TagSchema(BaseModel):
    id: int | None = None
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagResponseSchema(ResponseModel):
    data: TagSchema = None


class TagsResponseSchema(ResponseModel):
    data: List[TagSchema] = []
