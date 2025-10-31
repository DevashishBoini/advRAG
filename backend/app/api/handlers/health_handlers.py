"""
Handler functions for health check operations.
"""

import logging
from datetime import datetime

from app.db.manager import db_manager
from app.models.schemas import HealthCheckResponse

logger = logging.getLogger(__name__)


async def handle_health_check() -> tuple[HealthCheckResponse | dict, int]:
    """
    Handle health check logic.
    
    Returns:
        tuple: (response_data, status_code)
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
                {
                    "status": "unhealthy",
                    "database": "disconnected",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": health_status.get("error")
                },
                503
            )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return (
            {
                "status": "unhealthy",
                "database": "error",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            },
            503
        )
