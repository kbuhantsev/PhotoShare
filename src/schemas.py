from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: str = "ok"
    message: str = ""
