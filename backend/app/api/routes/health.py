"""
Health check API routes.
Defines endpoints for service health monitoring.
"""

import logging

from fastapi import APIRouter, Response
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
async def health_check(response: Response) -> HealthCheckResponse:
    """
    Health check endpoint to verify database connectivity.
    
    Returns:
        HealthCheckResponse: Health status with database connectivity info
        - **status**: Overall service status (healthy/unhealthy)
        - **database**: Database connection status (connected/disconnected/error)
        - **timestamp**: Time of the health check
    """
    response_data, status_code = await handle_health_check()
    
    # Set custom status code while still using response model validation
    response.status_code = status_code
    
    # FastAPI will automatically validate response_data against HealthCheckResponse
    return response_data
