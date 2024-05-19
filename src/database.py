from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.settings import settings

engine = create_async_engine(settings.get_db_uri())
async_session_factory = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


# Dependency
async def get_db():
    async with async_session_factory() as session:
        yield session
