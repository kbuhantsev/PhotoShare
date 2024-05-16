from sqlalchemy import Integer, func, DateTime

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import settings

engine = create_async_engine(settings.get_db_uri())
async_session_factory = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# Dependency
async def get_db():
    async with async_session_factory() as session:
        yield session


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
