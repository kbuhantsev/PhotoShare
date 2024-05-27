from pydantic import BaseModel, ConfigDict

from src.schemas import ResponseModel


class RatingSchema(BaseModel):
    rating: float | int

    model_config = ConfigDict(from_attributes=True)


class RatingResponseSchema(ResponseModel):

    class Data(RatingSchema):
        id: int
        user_id: int
        photo_id: int

    data: Data = None

    model_config = ConfigDict(from_attributes=True)


class RatingAverageResponseSchema(ResponseModel):

    class Data(RatingSchema):
        photo_id: int

    data: Data = None
