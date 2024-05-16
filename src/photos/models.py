from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, MetaData, ForeignKey

from src.models import Base
from src.tags.models import Tag

photo_metadata = MetaData()


class Photo(Base):
    __tablename__ = "photos"
    metadata = photo_metadata
    title: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    public_id: Mapped[str] = mapped_column(String(255))
    secure_url: Mapped[str] = mapped_column(String(255))
    folder: Mapped[str] = mapped_column(String(255))
    tags: Mapped[list[Tag]] = relationship(
        secondary="photo_m2m_tag", back_populates="photos"
    )

    def __repr__(self):
        return f"Photo(title={self.title})"
