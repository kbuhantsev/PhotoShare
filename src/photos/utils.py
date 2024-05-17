from typing import BinaryIO

import cloudinary
import cloudinary.uploader
import cloudinary.api

from src.settings import settings


cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)


def upload_file(file: BinaryIO, folder: str):
    asset = cloudinary.uploader.upload(
        file,
        folder=folder,
        overwrite=True,
        use_filename=True,
        use_unique_filename=False,
    )

    return asset


def delete_file(public_id: str):
    r = cloudinary.uploader.destroy(public_id=public_id)
    if r.get("result") == "ok":
        return True
    return False


def transform_file(public_id:str, transformations: dict):

    result = cloudinary.CloudinaryImage(public_id=public_id) \
        .image(**transformations)

    return result

