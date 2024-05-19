from typing import List

from pydantic import BaseModel
from src.schemas import ResponseModel


class PhotoSchema(BaseModel):
    title: str
    owner_id: int
    public_id: str
    secure_url: str
    folder: str
    tags: list[str] = []


class PhotoResponseSchema(ResponseModel):
    data: PhotoSchema = None


class PhotosResponseSchema(ResponseModel):
    data: List[PhotoSchema] = []



