from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ForgotPasswordTokenSchema(BaseModel):
    message: str
    reset_token: str
