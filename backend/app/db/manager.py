"""
Database manager with retry logic and table creation.
"""

import asyncio
import logging
from typing import Any

from sqlalchemy import inspect, text
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings
from app.db.client import db_client
from app.models.session import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database manager with retry logic and graceful error handling.
    
    Features:
    - Automatic retry with exponential backoff
    - Table creation and migration support
    - Health check functionality
    - Graceful fallback mechanisms
    """
    
    def __init__(self):
        """Initialize the database manager."""
        self.client = db_client
    
    @retry(
        stop=stop_after_attempt(settings.db_max_retries),
        wait=wait_exponential(
            multiplier=settings.db_retry_delay,
            max=30
        ),
        retry=retry_if_exception_type((Exception,)),
        reraise=True,
    )
    async def connect_with_retry(self) -> bool:
        """
        Connect to database with automatic retry logic.
        
        Returns:
            bool: True if connection successful
            
        Raises:
            Exception: If all retry attempts fail
        """
        try:
            await self.client.connect()
            logger.info("🔌 Database connection established successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection attempt failed: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from database gracefully."""
        try:
            await self.client.disconnect()
            logger.info("✅ Database disconnected successfully")
        except Exception as e:
            logger.error(f"❌ Error during disconnect: {e}")
    
    async def create_tables(self) -> None:
        """
        Create all database tables if they don't exist.
        
        Raises:
            RuntimeError: If database is not connected
        """
        if not self.client.is_connected:
            raise RuntimeError("Database not connected")
        
        try:
            logger.info("🗄️  Creating database tables...")
            
            if not self.client.engine:
                raise RuntimeError("Database engine not available")
            
            async with self.client.engine.begin() as conn:
                # Create all tables defined in Base metadata
                await conn.run_sync(Base.metadata.create_all)
            
            logger.info("✅ Database tables created successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            raise
    
    async def check_health(self) -> dict[str, Any]:
        """
        Check database health and connection status.
        
        Returns:
            dict: Health status information
        """
        health_status = {
            "connected": False,
            "tables_exist": False,
            "error": None
        }
        
        try:
            if not self.client.is_connected:
                health_status["error"] = "Not connected"
                return health_status
            
            # Check connection
            async with self.client.get_session() as session:
                result = await session.execute(text("SELECT 1"))
                health_status["connected"] = True
            
            # Check if tables exist
            if not self.client.engine:
                raise RuntimeError("Database engine not available")
            
            async with self.client.engine.connect() as conn:
                def check_tables(connection):
                    inspector = inspect(connection)
                    return "chat_sessions" in inspector.get_table_names()
                
                tables_exist = await conn.run_sync(check_tables)
                health_status["tables_exist"] = tables_exist
            
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            health_status["error"] = str(e)
        
        return health_status
    
    async def initialize(self) -> bool:
        """
        Initialize database with retry logic and table creation.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Connect with retry
            await self.connect_with_retry()
            
            # Create tables if they don't exist
            await self.create_tables()
            
            # Verify health
            health = await self.check_health()
            if not health["connected"] or not health["tables_exist"]:
                logger.error(f"❌ Database initialization incomplete: {health}")
                return False
            
            logger.info("✅ Database initialized successfully")
            return True
            
        except Exception as e:
            logger.critical(f"🔥 DATABASE INITIALIZATION FAILED: {e}")
            return False
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute a database operation with retry logic.
        
        Uses tenacity retry decorator on the function execution.
        
        Args:
            func: Async function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function execution
        """
        @retry(
            stop=stop_after_attempt(settings.db_max_retries),
            wait=wait_exponential(
                multiplier=settings.db_retry_delay,
                max=10
            ),
            retry=retry_if_exception_type((Exception,)),
            reraise=True,
        )
        async def _execute():
            return await func(*args, **kwargs)
        
        try:
            return await _execute()
        except Exception as e:
            logger.critical(f"🔥 Operation failed after {settings.db_max_retries} retries: {e}")
            raise


# Global database manager instance
db_manager = DatabaseManager()
