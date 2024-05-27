from sqlalchemy import ForeignKey, SmallInteger, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


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
