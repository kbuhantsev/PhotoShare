# pydantic models


from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Pydantic model for returning access and refresh tokens.

    Attributes:
        access_token (str): The access token for authentication.
        refresh_token (str): The refresh token for token refresh.
        token_type (str): The type of the token, which is typically "bearer".
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
