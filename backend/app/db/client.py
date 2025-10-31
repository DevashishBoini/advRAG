"""
Database client for async PostgreSQL connection management.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool, QueuePool

from app.config import settings

logger = logging.getLogger(__name__)


class DatabaseClient:
    """
    Async database client for managing PostgreSQL connections.
    
    Features:
    - Connection pooling for efficient resource management
    - Async context managers for session handling
    - Graceful connection and disconnection
    """
    
    def __init__(self):
        """Initialize the database client."""
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None
        self._is_connected: bool = False
    
    async def connect(self) -> None:
        """
        Establish database connection with connection pooling.
        
        Raises:
            Exception: If connection fails
        """
        if self._is_connected:
            logger.warning("Database already connected")
            return
        
        try:
            logger.info("Connecting to database...")
            
            # Create async engine with connection pooling
            self._engine = create_async_engine(
                settings.database_url,
                echo=settings.database_echo,
                pool_size=settings.database_pool_size,
                max_overflow=settings.database_max_overflow,
                pool_timeout=settings.database_pool_timeout,
                pool_recycle=settings.database_pool_recycle,
                pool_pre_ping=True,  # Verify connections before using
                poolclass=QueuePool,
                future=True,
            )
            
            # Create session factory
            self._session_factory = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
            
            # Test connection
            async with self._engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            
            self._is_connected = True
            logger.info("Successfully connected to database")
            
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            self._is_connected = False
            raise
    
    async def disconnect(self) -> None:
        """
        Close database connection and dispose of engine.
        """
        if not self._is_connected:
            logger.warning("Database not connected")
            return
        
        try:
            logger.info("Disconnecting from database...")
            
            if self._engine:
                await self._engine.dispose()
                self._engine = None
            
            self._session_factory = None
            self._is_connected = False
            
            logger.info("Successfully disconnected from database")
            
        except Exception as e:
            logger.error(f"Error during database disconnect: {e}")
            raise
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get an async database session with automatic commit/rollback.
        
        Yields:
            AsyncSession: Database session
            
        Raises:
            RuntimeError: If database is not connected
        """
        if not self._is_connected or not self._session_factory:
            raise RuntimeError("Database not connected. Call connect() first.")
        
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Session error, rolling back: {e}")
                raise
            finally:
                await session.close()
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._is_connected
    
    @property
    def engine(self) -> AsyncEngine | None:
        """Get the database engine."""
        return self._engine


# Global database client instance
db_client = DatabaseClient()
