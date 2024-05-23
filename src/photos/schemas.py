from typing import List, Optional

from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)


class TransformationResponseSchema(ResponseModel):
    data: Optional[TransformationSchema] = None


class TransformationsResponseSchema(ResponseModel):
    data: Optional[List[TransformationSchema]] = []


class TransformationsURLSchema(BaseModel):
    url: str


class TransformationsURLResponseSchema(ResponseModel):
    data: str | None = None


#  ---------------------------------------------------------
#  Photos


class PhotoSchema(BaseModel):
    id: int | None = None
    title: str
    description: str
    owner_id: int
    public_id: str
    secure_url: str
    folder: str = "photos"
    tags: list[TagSchema] | None = []
    transformations: list[TransformationSchema] | None = []
    comments: list[CommentSchema] | None = []

    model_config = ConfigDict(from_attributes=True)


class UpdatePhotoSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[TagSchema] | None = None


class PhotoResponseSchema(ResponseModel):
    data: PhotoSchema = None


class PhotosResponseSchema(ResponseModel):
    data: List[PhotoSchema] | None = []
    total: int | None = 0
