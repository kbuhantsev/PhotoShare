from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel


class RatingSchema(BaseModel):
    rating: int

    model_config = ConfigDict(from_attributes=True)


class RatingResponseSchema(ResponseModel):

    class Data(RatingSchema):
        id: int
        user_id: int
        photo_id: int

    data: Data = None

    model_config = ConfigDict(from_attributes=True)
