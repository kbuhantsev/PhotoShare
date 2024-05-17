# pydantic models
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from src.user.models import Role
from src.schemas import ResponseModel


class UserSchema(ResponseModel):
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr
    password: str = Field(min_length=8, max_length=12)


class UserResponseSchema(UserSchema):
    password: str = Field(exclude=True)

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCurrentResponseSchema(UserSchema):
    password: str = Field(exclude=True)
    role: Role
    avatar: Optional[str]
    confirmed: bool

    @field_serializer("role")
    def serialize_role(self, role: Role) -> str:
        return role.name

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserRequestEmailSchema(ResponseModel):
    email: EmailStr


class UserRequestPasswordResetSchema(ResponseModel):
    reset_token: str
    new_password: str
    confirm_password: str
