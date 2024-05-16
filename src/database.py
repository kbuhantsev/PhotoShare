from sqlalchemy import Integer, func, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from src.settings import settings


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


engine = create_async_engine(settings.get_db_uri(), echo=True)
SessionDB = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


async def get_db():
    async with SessionDB() as session:
        yield session
