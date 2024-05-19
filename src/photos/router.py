from fastapi import APIRouter, status, Depends
from typing import Annotated

from fastapi import File, Form, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_current_user
from src.photos.service import (
    create_photo,
    update_photo,
    get_photo,
    delete_photo,
    get_photos,
)
from src.database import get_db
from src.photos.schemas import PhotoResponseSchema, PhotoSchema, PhotosResponseSchema
from src.user.models import User

router = APIRouter(
    prefix="/photos",
    tags=["photos"],
)


@router.get("/", response_model=PhotosResponseSchema, status_code=status.HTTP_200_OK)
async def get_photos_handler(
    skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)
):

    response_model = PhotoResponseSchema()

    try:
        photos = await get_photos(skip=skip, limit=limit, db=db)
        photos_data = []
        for photo in photos:
            tags_list = [tag.name for tag in photo.tags]
            photos_data.append(
                PhotoSchema(
                    title=photo.title,
                    owner_id=photo.owner_id,
                    public_id=photo.public_id,
                    secure_url=photo.secure_url,
                    folder=photo.folder,
                    tags=tags_list if tags_list else [],
                )
            )
        response_model.data = photos_data
        return response_model
    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while getting the photos!"
        return response_model


@router.get(
    "/{photo_id}", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK
)
async def get_photo_by_id(photo_id: int, db: AsyncSession = Depends(get_db)):

    response_model = PhotoResponseSchema()

    try:
        photo = await get_photo(photo_id=photo_id, db=db)
        tags_list = [tag.name for tag in photo.tags]

        photo_data = PhotoSchema(
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )

    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while getting the photo!"
        return response_model

    if not photo:
        response_model.status = "error"
        response_model.message = "An error occurred while getting the photo!"
        return response_model

    response_model = PhotoResponseSchema()
    response_model.data = photo_data
    return response_model


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PhotoResponseSchema,
)
async def create_photo_handler(
    response: Response,
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    tags: Annotated[str, Form()] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]
    else:
        tags_list = []

    response_model = PhotoResponseSchema()

    try:
        photo = await create_photo(
            title=title,
            file=file.file,
            description=description,
            tags=tags_list,
            db=db,
            current_user=current_user,
        )
    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while creating the photo!"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response

    if not photo:
        response_model.status = "error"
        response_model.message = "An error occurred while creating the photo!"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response

    response = PhotoResponseSchema()
    response.data = photo
    return response


@router.put(
    "/{photo_id}", status_code=status.HTTP_200_OK, response_model=PhotoResponseSchema
)
async def update_photo_by_id(
    response: Response,
    photo_id: int,
    title: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    tags: Annotated[str, Form()] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if tags:
        tags_list = [tag.strip() for tag in tags.split(",")]
    else:
        tags_list = []

    response_model = PhotoResponseSchema()

    try:
        photo = await update_photo(
            photo_id=photo_id,
            title=title,
            file=file.file,
            description=description,
            tags=tags_list,
            db=db,
        )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_model.status = "error"
        response_model.message = "An error occurred while updating the photo!"
        return response_model

    if not photo:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_model.status = "error"
        response_model.message = "An error occurred while updating the photo!"
        return response_model

    response_model = PhotoResponseSchema()
    response_model.data = photo
    return response_model


@router.delete(
    "/{photo_id}", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK
)
async def delete_photo_by_id(
    response: Response, photo_id: int, db: AsyncSession = Depends(get_db)
):

    response_model = PhotoResponseSchema()

    try:
        photo = await delete_photo(photo_id=photo_id, db=db)
        tags_list = [tag.name for tag in photo.tags]

        photo_data = PhotoSchema(
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_model.status = "error"
        response_model.message = "An error occurred while deleting the photo!"
        return response_model

    if not photo:
        response.status_code = status.HTTP_403_FORBIDDEN
        response_model.status = "error"
        response_model.message = "An error occurred while deleting the photo!"
        return response_model

    response_model = PhotoResponseSchema()
    response_model.data = photo_data
    return response_model
