from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from database import SessionLocal


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session context manager with transaction."""
    async with SessionLocal() as session:
        async with session.begin():
            try:
                yield session
            finally:
                await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session without transaction management."""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
