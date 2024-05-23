import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from src.schemas import ResponseModel
from src.user.models import Role


class UsersRolesResponseShema(ResponseModel):
    data: List = []


class UserSchema(BaseModel):
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr
    password: str = Field(min_length=8, max_length=12)


class UserUpdateSchema(BaseModel):
    # WTF not WORKING
    # password: str = Field(exclude=True)

    # model_config = ConfigDict(
    #     from_attributes=True,
    # )
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr


class UserEmailSchema(BaseModel):
    email: EmailStr


class UserAuthPasswordResetSchema(BaseModel):
    new_password: str = Field(min_length=8, max_length=12)
    confirm_password: str = Field(min_length=8, max_length=12)


class UserPasswordResetSchema(UserAuthPasswordResetSchema):
    reset_token: str

    model_config = ConfigDict(
        from_attributes=True,
    )


# RESPONSE
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
        blocked: Optional[bool]

        @field_serializer("role")
        def serialize_role(self, role: Role) -> str:
            if role is None:
                return None
            return role.name

    data: Data = None

    model_config = ConfigDict(
        from_attributes=True,
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


class UsersProfileResponseSchema(UserProfileResponseSchema):
    data: list[UserProfileResponseSchema.Data] = []
    total: int = 0

    model_config = ConfigDict(
        from_attributes=True,
    )
