"""
API routes and endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    """Root API endpoint."""
    return {"message": "API is running"}


@router.get("/status")
async def get_status():
    """Get API status."""
    return {"status": "operational"}
