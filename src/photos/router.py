from typing import Annotated, Union

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
    Body
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user
from src.photos.dependencies import allowed_delete_photo
from src.photos.schemas import PhotoResponseSchema, PhotoSchema, PhotosResponseSchema, TransformationSchema, \
    TransformationResponseSchema
from src.photos.services.photo_service import (
    create_photo,
    delete_photo,
    get_photo,
    get_photos,
    update_photo,
    get_photos_count,
)
from src.photos.services.transformation_service import transform
from src.user.models import User

router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)


@router.get("/", response_model=PhotosResponseSchema, status_code=status.HTTP_200_OK)
async def get_photos_handler(
    skip: int = 0, limit: int = 50, q: str = "", db: AsyncSession = Depends(get_db)
):
    response_model = PhotosResponseSchema()

    try:
        total = await get_photos_count(query=q, db=db)
        photos = await get_photos(skip=skip, limit=limit, query=q, db=db)
        photos_data = []
        for photo in photos:
            tags_list = [tag.name for tag in photo.tags]
            photos_data.append(
                PhotoSchema(
                    id=photo.id,
                    title=photo.title,
                    owner_id=photo.owner_id,
                    public_id=photo.public_id,
                    secure_url=photo.secure_url,
                    folder=photo.folder,
                    tags=tags_list if tags_list else [],
                )
            )
        response_model.total = total
        response_model.data = photos_data

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
        response_model.data = photo_data
    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while getting the photo!"
        return response_model

    if not photo:
        response_model.status = "error"
        response_model.message = "An error occurred while getting the photo!"
        return response_model

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

        photo_data = PhotoSchema(
            id=photo.id,
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )
        response_model.data = photo_data

    except Exception as e:
        print(e)
        response_model.status = "error"
        response_model.message = "An error occurred while creating the photo!"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model

    if not photo:
        response_model.status = "error"
        response_model.message = "An error occurred while creating the photo!"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response_model

    return response_model


@router.put(
    "/{photo_id}", status_code=status.HTTP_200_OK, response_model=PhotoResponseSchema
)
async def update_photo_by_id(
    response: Response,
    photo_id: int,
    title: Annotated[str, Form()] = None,
    file: Annotated[UploadFile, File()] = None,
    description: Annotated[str, Form()] = None,
    tags: Annotated[str, Form()] = None,
    db: AsyncSession = Depends(get_db),
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
            file=file.file if file else None,
            description=description,
            tags=tags_list,
            db=db,
        )

        photo_data = PhotoSchema(
            id=photo.id,
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )
        response_model.data = photo_data

    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_model.status = "error"
        response_model.message = "An error occurred while updating the photo!"
        return response_model

    if not photo:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_model.status = "error"
        response_model.message = "An error occurred while updating the photo!"
        return response_model

    return response_model


@router.delete(
    "/{photo_id}", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK
)
async def delete_photo_by_id(
    response: Response,
    photo_id: int,
    allowed: bool = Depends(allowed_delete_photo),
    db: AsyncSession = Depends(get_db),
):

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

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
        response_model.data = photo_data
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

    return response_model


#  ---------------------------------------------------------
#  Transformations

@router.post("/trans/{photo_id}", response_model=TransformationResponseSchema, status_code=status.HTTP_200_OK)
async def create_transformation(
     response: Response,
     photo_id: int,
     transformations: Annotated[dict[str, Union[str | int | float | None]], Body(embed=True)],
     db: AsyncSession = Depends(get_db),
):

    response_model = TransformationResponseSchema()

    try:
        result = await transform(
            photo_id=photo_id,
            transformations=transformations,
            db=db
        )

        if not result:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_model.status = "error"
            response_model.message = "An error occurred while creating the transformation!"
            return response_model

        transformation_data = TransformationSchema(
            photo_id=photo_id,
            title=result.get("title"),
            public_id=result.get("public_id"),
            secure_url=result.get("secure_url"),
            folder="transformations",
        )
        response_model.data = transformation_data
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_model.status = "error"
        response_model.message = "An error occurred while creating the transformation!"
        return response_model

    return result
