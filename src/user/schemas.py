from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from src.schemas import ResponseModel
from src.user.models import Role


class UsersRolesResponseSchema(ResponseModel):
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

    class Data(UserResponseSchema.Data):
        role: Role
        avatar: Optional[str]
        blocked: Optional[bool]

        @field_serializer("role")
        def serialize_role(self, role: Role) -> str | None:
            if role is None:
                return None
            return role.name

    data: Data = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserProfileResponseSchema(UserCurrentResponseSchema):

    class Data(UserCurrentResponseSchema.Data):
        created_at: datetime
        updated_at: datetime
        count_photos: int = 0
        count_comments: int = 0

    data: Data = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserProfileInfoResponseSchema(UserProfileResponseSchema.Data):
    pass



class UsersProfileResponseSchema(UserProfileResponseSchema):
    data: list[UserProfileResponseSchema.Data] = []
    total: int = 0

    model_config = ConfigDict(
        from_attributes=True,
    )


# TESTS

class UserResponseRefreshToken(UserSchema):
    refresh_token: str


class UserRequestEmailSchema(BaseModel):
    email: EmailStr


class UserRequestPasswordResetSchema(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str
