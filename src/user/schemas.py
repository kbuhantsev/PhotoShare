import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from src.schemas import ResponseModel
from src.user.models import Role


class UserSchema(BaseModel):
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr
    password: str = Field(min_length=8, max_length=12)


class UserBaseResponseSchema(ResponseModel):

    data: UserSchema = None


class UserResponseSchema(UserBaseResponseSchema):

    class Data(UserSchema):
        password: str = Field(exclude=True)

    data: Data = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCurrentResponseSchema(UserBaseResponseSchema):

    class Data(UserSchema):
        password: str = Field(exclude=True)
        role: Role
        avatar: Optional[str]

        @field_serializer("role")
        def serialize_role(self, role: Role) -> str:
            if role is None:
                return None
            return role.name

    data: Data = None

    model_config = ConfigDict(
        from_attributes=True,
        unsettabl=True,
    )


class UserProfileResponseSchema(UserCurrentResponseSchema):

    class Data(UserCurrentResponseSchema.Data):
        created_at: datetime.datetime = None
        updated_at: datetime.datetime = None
        count_photos: int = 0
        count_comments: int = 0

    data: Data = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserRequestEmailSchema(BaseModel):
    email: EmailStr


class UserRequestPasswordResetSchema(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str
