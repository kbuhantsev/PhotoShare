# pydantic models
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from src.user.models import Role
from src.schemas import ResponseModel


class UserSchema(BaseModel):
    username: str = Field(min_length=2, max_length=25)
    email: EmailStr
    password: str = Field(min_length=8, max_length=12)


class UserBaseResponseSchema(UserSchema, ResponseModel):
    pass


class UserResponseSchema(UserBaseResponseSchema):
    password: str = Field(exclude=True)

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserCurrentResponseSchema(UserBaseResponseSchema):
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


class UserRequestEmailSchema(BaseModel):
    email: EmailStr


class UserRequestPasswordResetSchema(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str
