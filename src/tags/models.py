from sqlalchemy import mapped_column, Integer, String, MetaData, ForeignKey, Mapped
from sqlalchemy.orm import relationship

from src.models import Base
from src.photos.models import Photo

tag_metadata = MetaData()
photo_m2m_tag_metadata = MetaData()


class photo_m2m_tag(Base):
    __tablename__ = "photo_m2m_tag"
    metadata = photo_m2m_tag_metadata
    note: Mapped[int] = (
        mapped_column(Integer, ForeignKey("photos.id", ondelete="CASCADE")),
    )
    tag: Mapped[int] = (
        mapped_column(Integer, ForeignKey("tags.id", ondelete="CASCADE")),
    )


class Tag(Base):
    __tablename__ = "tags"
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    photos: Mapped[list[Photo]] = relationship(
        secondary="photo_m2m_tag", back_populates="tags"
    )

    def __repr__(self):
        return f"Tag(name={self.name})"
