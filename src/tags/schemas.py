# pydantic models
from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
