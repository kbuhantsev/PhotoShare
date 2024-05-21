from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


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
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="photos_to_tags",
        back_populates="photos",
    )

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
    qr_code: Mapped["QrCode"] = relationship(back_populates="transformation", single_parent=True)

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
    transformation: Mapped["Transformation"] = relationship(back_populates="qr_code", single_parent=True)

    def __repr__(self):
        return f"QrCode(name={self.title})"
