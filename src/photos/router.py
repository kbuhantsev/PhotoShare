from fastapi import APIRouter, status
from typing import Annotated

from fastapi import File, Form, UploadFile

from service import create_photo

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)


@router.get("/")
async def get_photos():
    return {"message": "Hello World"}


@router.get("/{photo_id}")
async def get_photo(photo_id: int):
    return {"message": "Hello World"}


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=None)
async def create_photo(
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    folder: Annotated[str, Form()],
    public_id: Annotated[str, Form()],
    secure_url: Annotated[str, Form()],
    tags: Annotated[list[str], Form()],
):

    photo = await create_photo(
        title=title,
        file=file.file,
        folder=folder,
        public_id=public_id,
        secure_url=secure_url,
        tags=tags,
    )



    return {"message": "Hello World"}


@router.put("/{photo_id}")
async def update_photo(photo_id: int):
    return {"message": "Hello World"}


@router.delete("/{photo_id}")
async def delete_photo(photo_id: int):
    return {"message": "Hello World"}
