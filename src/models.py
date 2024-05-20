from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    SmallInteger,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

base_metadata = MetaData()


class Base(DeclarativeBase):
    metadata = base_metadata
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


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
