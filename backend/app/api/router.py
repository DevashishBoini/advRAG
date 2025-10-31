"""
Main API router.
This file aggregates all routes and provides the main router for the application.
"""

from fastapi import APIRouter

# Import from the routes package
from app.api.routes.health import router as health_router
from app.api.routes.sessions import router as sessions_router

# Main router that includes all API routes
router = APIRouter()

# Include all route modules
router.include_router(health_router)
router.include_router(sessions_router)


@router.get("/")
async def read_root():
    """
    Root API endpoint.
    
    Returns basic API information.
    """
    return {
        "message": "API is running",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


__all__ = ["router"]
