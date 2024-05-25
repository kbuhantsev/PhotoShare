from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.photos.models import Photo


class PhotoToTag(Base):
    __tablename__ = "photos_to_tags"
    photo_id: Mapped[int] = mapped_column(ForeignKey("photos.id", ondelete="CASCADE"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"))


class Tag(Base):
    __tablename__ = "tags"
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    photos: Mapped[List["Photo"]] = relationship(secondary="photos_to_tags", back_populates="tags")

    def __repr__(self):
        return f"Tag(name={self.name})"
