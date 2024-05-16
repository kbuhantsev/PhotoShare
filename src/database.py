from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.settings import settings


engine = create_async_engine(settings.get_db_uri(), echo=True)
SessionDB = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


async def get_db():
    async with SessionDB() as session:
        yield session
