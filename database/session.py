from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from database import SessionLocal
import logging

# Configure SQLAlchemy engine logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session context manager with transaction."""
    logger = logging.getLogger(__name__)
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            except Exception as e:
                logger.error(f"Session error occurred: {str(e)}")
                logger.error("Stack trace:", exc_info=True)
                raise
            finally:
                logger.info("Closing database session")
                await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session without transaction management."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
