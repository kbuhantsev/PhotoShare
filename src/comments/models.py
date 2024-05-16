from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, MetaData, ForeignKey

from src.models import Base

comment_metadata = MetaData()


class Comment(Base):
    __tablename__ = "comments"
    metadata = comment_metadata
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    comment: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"Comment(user_id={self.user_id}, photo_id={self.photo_id}, comment={self.comment})"
