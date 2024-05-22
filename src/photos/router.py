from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
    Body,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.dependencies import get_current_user
from src.photos.dependencies import allowed_delete_photo
from src.photos.schemas import (
    PhotoResponseSchema,
    PhotoSchema,
    PhotosResponseSchema,
    TransformationSchema,
    TransformationResponseSchema,
    TransformationsURLResponseSchema,
    TransformationsURLSchema,
)
from src.photos.services.photo_service import (
    create_photo,
    delete_photo,
    get_photo,
    get_photos,
    update_photo,
    get_photos_count,
)
from src.photos.services.transformation_service import (
    transform,
    save_transform,
    get_qr_code,
)
from src.user.models import User

from src.logger import get_logger

logger = get_logger("Photos")

router = APIRouter(
    prefix="/photos",
    tags=["Photos"],
)


@router.get("/", response_model=PhotosResponseSchema, status_code=status.HTTP_200_OK)
async def get_photos_handler(
    response: Response,
    skip: int = 0,
    limit: int = 50,
    q: str = "",
    db: AsyncSession = Depends(get_db),
):

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

        return {"total": total, "data": photos_data}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while getting the photos!",
        }


@router.get(
    "/{photo_id}", response_model=PhotoResponseSchema, status_code=status.HTTP_200_OK
)
async def get_photo_by_id(
    response: Response, photo_id: int, db: AsyncSession = Depends(get_db)
):

    try:
        photo = await get_photo(photo_id=photo_id, db=db)
        if not photo:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while getting the photo!",
            }

        tags_list = [tag.name for tag in photo.tags]

        photo_data = PhotoSchema(
            id=photo.id,
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )

        return {"data": photo_data}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while getting the photo!",
        }


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

    try:
        photo = await create_photo(
            title=title,
            file=file.file,
            description=description,
            tags=tags_list,
            db=db,
            current_user=current_user,
        )

        if not photo:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while creating the photo!",
            }

        photo_data = PhotoSchema(
            id=photo.id,
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )

        return {"data": photo_data}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while creating the photo!",
        }


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

    try:
        photo = await update_photo(
            photo_id=photo_id,
            title=title,
            file=file.file if file else None,
            description=description,
            tags=tags_list,
            db=db,
        )

        if not photo:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while updating the photo!",
            }

        photo_data = PhotoSchema(
            id=photo.id,
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )
        return {"data": photo_data}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while updating the photo!",
        }


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

    try:
        photo = await delete_photo(photo_id=photo_id, db=db)
        if not photo:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while deleting the photo!",
            }

        tags_list = [tag.name for tag in photo.tags]

        photo_data = PhotoSchema(
            id=photo.id,
            title=photo.title,
            owner_id=photo.owner_id,
            public_id=photo.public_id,
            secure_url=photo.secure_url,
            folder=photo.folder,
            tags=tags_list if tags_list else [],
        )
        return {"data": photo_data}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while deleting the photo!",
        }


#  ---------------------------------------------------------
#  Transformations


@router.post(
    "/trans/{photo_id}",
    response_model=TransformationsURLResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def create_transformation(
    photo_id: int,
    transformations: Annotated[dict[str, Any], Body(embed=True)],
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    try:
        url = await transform(photo_id=photo_id, transformations=transformations, db=db)

        if not url:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while creating the transformation!",
            }

        return {"data": url}
    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while creating the transformation!",
        }


@router.post(
    "/trans/save/{photo_id}",
    response_model=TransformationResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def save_transformation(
    photo_id: int,
    body: TransformationsURLSchema,
    response: Response,
    db: AsyncSession = Depends(get_db),
):

    try:

        transformation = await save_transform(photo_id=photo_id, url=body.url, db=db)

        if not transformation:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while saving the photo!",
            }

        qr_code = await get_qr_code(
            transformation_id=transformation.id, url=transformation.secure_url, db=db
        )

        if not qr_code:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {
                "status": "error",
                "message": "An error occurred while saving qr code!",
            }

        transformation_data = TransformationSchema(
            id=transformation.id,
            photo_id=transformation.photo_id,
            title=transformation.title,
            public_id=transformation.public_id,
            secure_url=transformation.secure_url,
            folder=transformation.folder,
            qr_code=qr_code.secure_url,
        )

        return {"data": transformation_data}

    except Exception as e:
        logger.error(e)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status": "error",
            "message": "An error occurred while saving the transformation!",
        }
