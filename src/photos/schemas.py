from typing import List, Optional

from pydantic import BaseModel

from src.schemas import ResponseModel


class PhotoSchema(BaseModel):
    id: Optional[int] = None
    title: str
    owner_id: int
    public_id: str
    secure_url: str
    folder: str
    tags: list[str] = []


class UpdatePhotoSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None


class PhotoResponseSchema(ResponseModel):
    data: PhotoSchema = None


class PhotosResponseSchema(ResponseModel):
    data: Optional[List[PhotoSchema]] = []
    total: Optional[int] = 0
