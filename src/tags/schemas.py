# pydantic models
from pydantic import BaseModel, Field


class TagResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
