from typing import List, Optional

from pydantic import BaseModel

from src.comments.schemas import CommentSchema
from src.schemas import ResponseModel
from src.tags.schemas import TagSchema


class QrCodeSchema(BaseModel):
    id: Optional[int] = None
    transformation_id: int
    title: str
    public_id: str
    secure_url: str
    folder: str = "qrcodes"


#  ---------------------------------------------------------
#  Transformations


class TransformationSchema(BaseModel):
    id: Optional[int] = None
    photo_id: int
    title: str
    public_id: str
    secure_url: str
    folder: str = "transformations"
    qr_code: Optional[QrCodeSchema] = None


class TransformationResponseSchema(ResponseModel):
    data: Optional[TransformationSchema] = None


class TransformationsResponseSchema(ResponseModel):
    data: Optional[List[TransformationSchema]] = []


class TransformationsURLSchema(BaseModel):
    url: str


class TransformationsURLResponseSchema(ResponseModel):
    data: Optional[str] = None


#  ---------------------------------------------------------
#  Photos


class PhotoSchema(BaseModel):
    id: Optional[int] = None
    title: str
    owner_id: int
    public_id: str
    secure_url: str
    folder: str = "photos"
    tags: Optional[list[TagSchema]] = None
    transformations: Optional[list[TransformationSchema]] = None
    comments: Optional[list[CommentSchema]] = None


class UpdatePhotoSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[TagSchema]] = None


class PhotoResponseSchema(ResponseModel):
    data: PhotoSchema = None


class PhotosResponseSchema(ResponseModel):
    data: Optional[List[PhotoSchema]] = []
    total: Optional[int] = 0
