# Global models

from sqlalchemy import Integer, func, DateTime, MetaData

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

base_metadata = MetaData()


class Base(DeclarativeBase):
    metadata = base_metadata
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
