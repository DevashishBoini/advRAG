"""
Database initialization script.
Run this to verify database setup and create tables.
"""

import asyncio
import logging
import sys

# Add parent directory to path
sys.path.insert(0, "/Users/dboini/Public/proj/advRAG/advRAG/backend")

from app.config import settings
from app.db.manager import db_manager
from app.models.session import Base

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize database and create tables."""
    logger.info("=" * 60)
    logger.info("Database Initialization Script")
    logger.info("=" * 60)
    
    try:
        # Display configuration
        logger.info(f"Database URL: {settings.database_url.split('@')[1] if '@' in settings.database_url else 'N/A'}")
        logger.info(f"Pool Size: {settings.database_pool_size}")
        logger.info(f"Max Retries: {settings.db_max_retries}")
        logger.info("")
        
        # Initialize database
        logger.info("Initializing database...")
        success = await db_manager.initialize()
        
        if success:
            logger.info("✓ Database initialized successfully!")
            
            # Check health
            logger.info("\nChecking database health...")
            health = await db_manager.check_health()
            
            logger.info(f"Connected: {health['connected']}")
            logger.info(f"Tables Exist: {health['tables_exist']}")
            
            if health.get('error'):
                logger.warning(f"Health Check Warning: {health['error']}")
            
            logger.info("\n" + "=" * 60)
            logger.info("Database is ready!")
            logger.info("=" * 60)
            
        else:
            logger.error("✗ Database initialization failed!")
            logger.error("Please check your configuration and try again.")
            return False
        
        # Disconnect
        await db_manager.disconnect()
        logger.info("\nDisconnected from database.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during initialization: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
