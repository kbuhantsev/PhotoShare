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



