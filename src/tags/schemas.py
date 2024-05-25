from typing import List

from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel


class TagSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TagResponseInstanceSchema(TagSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TagResponseSchema(ResponseModel):
    class Data(TagSchema):
        id: int

    data: Data = None


class TagsResponseSchema(ResponseModel):
    data: List[TagResponseSchema.Data] = []
