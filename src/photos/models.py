from typing import List

from sqlalchemy import ForeignKey, String, select, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.models import Base
from src.rating.models import Rating


class Photo(Base):
    __tablename__ = "photos"
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    public_id: Mapped[str] = mapped_column(String(255))
    secure_url: Mapped[str] = mapped_column(String(255))
    folder: Mapped[str] = mapped_column(String(255))
    # Alchemy
    owner: Mapped["User"] = relationship("User", backref="photos", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="photos_to_tags",
        back_populates="photos",
        lazy="selectin",
    )
    transformations: Mapped[List["Transformation"]] = relationship(
        "Transformation",
        back_populates="photo",
        lazy="selectin",
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        primaryjoin="Comment.photo_id == Photo.id",
        back_populates="photo",
        lazy="selectin",
    )
    ratings: Mapped[List["Rating"]] = relationship(
        'Rating',
        primaryjoin='Photo.id==Rating.photo_id',
        foreign_keys='Rating.photo_id',
        backref='photo',
        lazy="selectin",
    )

    @hybrid_property
    def average_rating(self):
        if not self.ratings:
            return 0
        return sum([rating.rating for rating in self.ratings]) / len(self.ratings)

    def __repr__(self):
        return f"Photo(title={self.title})"


class Transformation(Base):
    __tablename__ = "transformations"
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(255))
    public_id: Mapped[str] = mapped_column(String(255))
    secure_url: Mapped[str] = mapped_column(String(255))
    folder: Mapped[str] = mapped_column(String(255))
    # Alchemy
    qr_code: Mapped["QrCode"] = relationship(
        "QrCode",
        back_populates="transformation",
        single_parent=True,
        primaryjoin="QrCode.transformation_id == Transformation.id",
        lazy="selectin",
    )
    photo: Mapped["Photo"] = relationship(
        "Photo",
        back_populates="transformations",
    )

    def __repr__(self):
        return f"Transformation(name={self.title})"


class QrCode(Base):
    __tablename__ = "qr_codes"
    transformation_id: Mapped[int] = mapped_column(
        ForeignKey("transformations.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    title: Mapped[str] = mapped_column(String(255))
    public_id: Mapped[str] = mapped_column(String(255))
    secure_url: Mapped[str] = mapped_column(String(255))
    folder: Mapped[str] = mapped_column(String(255))
    # Alchemy
    transformation: Mapped["Transformation"] = relationship(
        back_populates="qr_code",
        primaryjoin="QrCode.transformation_id == Transformation.id",
        single_parent=True,
    )

    def __repr__(self):
        return f"QrCode(name={self.title})"
