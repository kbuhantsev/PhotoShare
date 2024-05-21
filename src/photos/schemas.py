from typing import List, Optional

from pydantic import BaseModel

from src.schemas import ResponseModel


#  ---------------------------------------------------------
#  Photos

class PhotoSchema(BaseModel):
    id: Optional[int] = None
    title: str
    owner_id: int
    public_id: str
    secure_url: str
    folder: str = "photos"
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


#  ---------------------------------------------------------
#  Transformations

class TransformationSchema(BaseModel):
    id: Optional[int] = None
    photo_id: int
    title: str
    public_id: str
    secure_url: str
    folder: str = "transformations"


class TransformationResponseSchema(ResponseModel):
    data: Optional[TransformationSchema] = None


class TransformationsResponseSchema(ResponseModel):
    data: Optional[List[TransformationSchema]] = []


class TransformationsURLResponseSchema(ResponseModel):
    data: Optional[str] = None
