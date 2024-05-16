from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, String, ForeignKey, SmallInteger

from src.models import Base


class Photo(Base):
    __tablename__ = "photos"
    title: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    public_id: Mapped[str] = mapped_column(String(255))
    secure_url: Mapped[str] = mapped_column(String(255))
    folder: Mapped[str] = mapped_column(String(255))
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary="photos_to_tags", back_populates="photos"
    )

    def __repr__(self):
        return f"Photo(title={self.title})"


class Rating(Base):
    __tablename__ = "ratings"
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    rating: Mapped[int] = mapped_column(
        SmallInteger(), CheckConstraint("rating >= 1 and rating <= 5")
    )

    def __repr__(self):
        return f"Rating(photo_id={self.photo_id}, user_id={self.user_id}, rating={self.rating})"
