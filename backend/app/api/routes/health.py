"""
Health check API routes.
Defines endpoints for service health monitoring.
"""

import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.handlers.health_handlers import handle_health_check
from app.models.schemas import HealthCheckResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    response_model=HealthCheckResponse,
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"},
    },
    summary="Health check",
    description="Checks the health of the service and database connectivity",
)
async def health_check():
    """
    Health check endpoint to verify database connectivity.
    
    Returns:
        - **status**: Overall service status (healthy/unhealthy)
        - **database**: Database connection status (connected/disconnected/error)
        - **timestamp**: Time of the health check
    """
    response_data, status_code = await handle_health_check()
    
    if status_code == 200:
        return response_data
    else:
        return JSONResponse(
            status_code=status_code,
            content=response_data if isinstance(response_data, dict) else response_data.model_dump()
        )
