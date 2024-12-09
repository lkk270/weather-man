from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator
import logging
from core.settings import DATABASE_URL

logger = logging.getLogger(__name__)

# Initialize engine at module level for connection pooling across Lambda invocations
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connection before using from pool
    pool_size=5,         # Maintain small pool for Lambda
    max_overflow=10      # Allow temporary additional connections
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session with transaction management."""
    session = AsyncSession(engine, expire_on_commit=False)
    try:
        async with session.begin():  # Start transaction
            yield session
    except Exception as e:
        logger.error(f"Session error: {str(e)}")
        await session.rollback()
        raise
    finally:
        await session.close()
