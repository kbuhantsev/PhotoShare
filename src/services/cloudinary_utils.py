from typing import BinaryIO
import re

import cloudinary
import cloudinary.api
import cloudinary.uploader

from src.settings import settings

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)


def upload_file(file: BinaryIO | str, folder: str):
    asset = cloudinary.uploader.upload(
        file,
        folder=folder,
        overwrite=True,
        use_filename=True,
        use_unique_filename=False,
    )

    return asset


def delete_file(public_id: str) -> bool:
    r = cloudinary.uploader.destroy(public_id=public_id)
    if r.get("result") == "ok":
        return True
    return False


def transform_file(public_id:str, transformations: dict):

    result = cloudinary.CloudinaryImage(public_id=public_id) \
        .image(**transformations)
    if not result:
        return None

    img_url_pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"')

    match = img_url_pattern.search(result)
    if match:
        return match.group(1)
    else:
        return None