import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy import event, text
from app.models import BaseModel
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create async engine with connection pooling
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO_LOG,  # SQL logging
    future=True,
    pool_pre_ping=True,  # Enable connection health checks
    poolclass=AsyncAdaptedQueuePool,
    pool_size=settings.DB_POOL_SIZE,  # Maximum number of connections in the pool
    max_overflow=settings.DB_MAX_OVERFLOW,  # Maximum number of connections that can be created beyond pool_size
    pool_timeout=settings.DB_POOL_TIMEOUT,  # Seconds to wait before giving up on getting a connection from the pool
    pool_recycle=settings.DB_POOL_RECYCLE,  # Seconds after which a connection is automatically recycled
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception as e:
        logger.error(f"Session error: {str(e)}")
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions"""
    async with get_db_session() as session:
        yield session


# Database initialization
async def init_db() -> None:
    try:
        # Try to connect to the database
        async with async_engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
            logger.info("Database tables created successfully")

        # Test the connection pool
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            logger.info("Database connection pool initialized successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise


# Database cleanup
async def close_db_connection() -> None:
    try:
        await async_engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connections: {str(e)}")
        raise


# Optional: Add event listeners for monitoring
@event.listens_for(async_engine.sync_engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    logger.info("New database connection established")


@event.listens_for(async_engine.sync_engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    logger.info("Database connection checked out from pool")


@event.listens_for(async_engine.sync_engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    logger.info("Database connection returned to pool")
