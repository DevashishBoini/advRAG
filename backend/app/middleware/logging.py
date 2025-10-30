"""
Logging middleware for request/response tracking.
"""

import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from time import time

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next):
        """Process the request and log timing information."""
        start_time = time()
        
        response = await call_next(request)
        
        process_time = time() - start_time
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Process time: {process_time:.3f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
