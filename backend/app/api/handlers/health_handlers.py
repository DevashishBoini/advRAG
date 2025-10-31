"""
Handler functions for health check operations.
"""

import logging
from datetime import datetime

from app.db.manager import db_manager
from app.models.schemas import HealthCheckResponse

logger = logging.getLogger(__name__)


async def handle_health_check() -> tuple[HealthCheckResponse, int]:
    """
    Handle health check logic.
    
    Returns:
        tuple: (HealthCheckResponse, status_code)
    """
    try:
        health_status = await db_manager.check_health()
        
        if health_status["connected"]:
            return (
                HealthCheckResponse(
                    status="healthy",
                    database="connected",
                    timestamp=datetime.utcnow()
                ),
                200
            )
        else:
            return (
                HealthCheckResponse(
                    status="unhealthy",
                    database="disconnected",
                    timestamp=datetime.utcnow()
                ),
                503
            )
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return (
            HealthCheckResponse(
                status="unhealthy",
                database="error",
                timestamp=datetime.utcnow()
            ),
            503
        )
