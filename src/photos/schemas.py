from src.schemas import ResponseModel


class PhotoSchema(ResponseModel):
    title: str
    owner_id: int
    public_id: str
    secure_url: str
    folder: str
    tags: list