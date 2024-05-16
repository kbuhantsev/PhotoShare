from fastapi import APIRouter, status, Depends
from typing import Annotated

from fastapi import File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.photos.service import create_photo
from src.database import get_db
from src.photos.schemas import PhotoResponseSchema
from src.user.models import User

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


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PhotoResponseSchema
)
async def create_photo(
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    tags: Annotated[list[str], Form()],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(),
):

    photo = await create_photo(
        title=title,
        file=file.file,
        description=description,
        tags=tags,
        db=db,
        current_user=current_user,
    )

    response = PhotoResponseSchema()

    if not photo:
        response.status = "error"
        response.message = "An error occurred while creating the photo!"
        return response

    response = PhotoResponseSchema()
    response.data = photo
    return response


@router.put("/{photo_id}")
async def update_photo(photo_id: int):
    return {"message": "Hello World"}


@router.delete("/{photo_id}")
async def delete_photo(photo_id: int):
    return {"message": "Hello World"}
