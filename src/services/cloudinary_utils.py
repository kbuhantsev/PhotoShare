from typing import BinaryIO
import re

import cloudinary
import cloudinary.api
import cloudinary.uploader

from src.settings import settings

MAIN_FOLDER = settings.cloudinary_folder

cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)


def get_full_folder(folder: str) -> str:
    full_path = [MAIN_FOLDER, folder]
    return "/".join(p for p in full_path if p != "")


def upload_file(file: BinaryIO | str, folder: str, public_id: str = None):
    folder_upload = get_full_folder(folder)
    if not public_id:
        asset = cloudinary.uploader.upload(
            file,
            folder=folder_upload,
            overwrite=True,
            use_filename=True,
            use_unique_filename=False,
        )
    else:
        asset = cloudinary.uploader.upload(
            file,
            folder=folder_upload,
            public_id=public_id,
            overwrite=True,
        )

    return asset


def build_url(
    public_id: str, width: int = 300, height: int = 300, crop: str = "fill"
) -> str:
    return cloudinary.CloudinaryImage(public_id=public_id).build_url(
        width=width, height=height, crop=crop
    )


def delete_file(public_id: str) -> bool:
    r = cloudinary.uploader.destroy(public_id=public_id)
    if r.get("result") == "ok":
        return True
    return False


def transform_file(public_id: str, transformations: dict):

    result = cloudinary.CloudinaryImage(public_id=public_id).image(**transformations)
    if not result:
        return None

    img_url_pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"')

    match = img_url_pattern.search(result)
    if match:
        return match.group(1)
    else:
        return None
