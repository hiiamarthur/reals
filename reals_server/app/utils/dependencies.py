
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import async_session

# Dependency for getting the database session
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session