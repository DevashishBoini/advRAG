"""
FastAPI application entry point with database lifecycle management.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import register_exception_handlers
from app.api.router import router
from app.config import settings
from app.db.manager import db_manager
from app.middleware.logging import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    
    Handles:
    - Database connection initialization with retry logic
    - Table creation
    - Graceful shutdown and cleanup
    """
    # Startup
    logger.info("🚀 Starting application...")
    
    try:
        # Initialize database with retry logic
        initialized = await db_manager.initialize()
        
        if not initialized:
            logger.error("❌ Failed to initialize database. Application may not function correctly.")
            # Continue anyway to allow health checks to report the issue
        else:
            logger.info("✅ Database initialized successfully")
    
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}", exc_info=True)
        # Continue anyway to allow health checks to report the issue
    
    logger.info("✅ Application started successfully")
    
    # Yield control to the application
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    
    try:
        await db_manager.disconnect()
        logger.info("✅ Database disconnected successfully")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}", exc_info=True)
    
    logger.info("✅ Application shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance with lifecycle management
    """
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        openapi_tags=[
            {
                "name": "health",
                "description": "Health check endpoints for monitoring application and database status"
            },
            {
                "name": "sessions",
                "description": "Chat session management - Create, read, update, and delete chat sessions"
            },
            {
                "name": "root",
                "description": "Root endpoints with API information"
            }
        ],
        contact={
            "name": "AdvRAG API Support",
            "url": "https://github.com/DevashishBoini/advRAG",
        },
        license_info={
            "name": "MIT",
        },
    )

    # Register exception handlers
    register_exception_handlers(app)
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: Configure based on your needs in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(router, prefix="/api/v1", tags=["api"])

    # Root health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        """
        Simple health check endpoint.
        For detailed health status, use /api/v1/health
        """
        return {"status": "healthy", "app": settings.app_name}

    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        """Root endpoint with API information."""
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.version,
            "docs": "/docs",
            "health": "/health",
            "api": "/api/v1"
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
