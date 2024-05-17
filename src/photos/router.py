from fastapi import APIRouter, status, Depends
from typing import Annotated

from fastapi import File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.photos.service import create_photo, update_photo, get_photo, delete_photo
from src.database import get_db
from src.photos.schemas import PhotoResponseSchema
from src.user.models import User

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)


@router.get("/", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK)
async def get_photos(
    skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)
):

    response = PhotoResponseSchema()

    try:
        photos = await get_photos(skip=skip, limit=limit, db=db)
        response.data = photos
        return response
    except Exception as e:
        response.status = "error"
        response.message = "An error occurred while getting the photos!"
        return response


@router.get(
    "/{photo_id}", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK
)
async def get_photo_by_id(photo_id: int, db: AsyncSession = Depends(get_db)):

    response = PhotoResponseSchema()

    try:
        photo = await get_photo(photo_id=photo_id, db=db)
    except Exception as e:
        response.status = "error"
        response.message = "An error occurred while getting the photo!"
        return response

    if not photo:
        response.status = "error"
        response.message = "An error occurred while getting the photo!"
        return response

    response = PhotoResponseSchema()
    response.data = photo
    return response


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PhotoResponseSchema
)
async def create_photo(
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    tags: Annotated[list[str], Form()],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    response = PhotoResponseSchema()

    try:
        photo = await create_photo(
            title=title,
            file=file.file,
            description=description,
            tags=tags,
            db=db,
            current_user=current_user,
        )
    except Exception as e:
        response.status = "error"
        response.message = "An error occurred while creating the photo!"
        return response

    if not photo:
        response.status = "error"
        response.message = "An error occurred while creating the photo!"
        return response

    response = PhotoResponseSchema()
    response.data = photo
    return response


@router.put(
    "/{photo_id}", status_code=status.HTTP_200_OK, response_model=PhotoResponseSchema
)
async def update_photo_by_id(
    photo_id: int,
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    tags: Annotated[list[str], Form()],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    response = PhotoResponseSchema()

    try:
        photo = await update_photo(
            photo_id=photo_id,
            title=title,
            file=file.file,
            description=description,
            tags=tags,
            db=db,
        )
    except Exception as e:
        response.status = "error"
        response.message = "An error occurred while updating the photo!"
        return response

    if not photo:
        response.status = "error"
        response.message = "An error occurred while updating the photo!"
        return response

    response = PhotoResponseSchema()
    response.data = photo
    return response


@router.delete(
    "/{photo_id}", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK
)
async def delete_photo_by_id(photo_id: int, db: AsyncSession = Depends(get_db)):

    response = PhotoResponseSchema()

    try:
        photo = await delete_photo(photo_id=photo_id, db=db)
    except Exception as e:
        response.status = "error"
        response.message = "An error occurred while deleting the photo!"
        return response

    if not photo:
        response.status = "error"
        response.message = "An error occurred while deleting the photo!"
        return response

    response = PhotoResponseSchema()
    return response
