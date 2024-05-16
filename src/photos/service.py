from typing import BinaryIO


async def create_photo(
    *,
    title: str,
    file: BinaryIO,
    folder: str,
    public_id: str,
    secure_url: str,
    tags: list[str],
):
    pass


async def update_photo(*, photo_id: int):
    pass


async def delete_photo(*, photo_id: int):
    pass


async def get_photos():
    pass


async def get_photo(*, photo_id: int):
    pass