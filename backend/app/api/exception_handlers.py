"""
Global exception handlers for FastAPI application.
Provides consistent error responses across all endpoints.
"""

import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from app.utils.exceptions import (
    AppException,
    ValidationError,
    ResourceNotFoundError,
    DatabaseError,
    ConnectionError as AppConnectionError,
    AuthenticationError,
    AuthorizationError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle custom application exceptions.
    
    Args:
        request: The FastAPI request
        exc: Application exception
        
    Returns:
        JSONResponse with error details
    """
    # Determine status code based on exception type
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if isinstance(exc, ValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, ResourceNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, AuthenticationError):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(exc, AuthorizationError):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(exc, RateLimitError):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
    elif isinstance(exc, AppConnectionError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    elif isinstance(exc, DatabaseError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    # Use appropriate symbol based on severity
    if status_code >= 500:
        log_symbol = "🔥"
        log_level = logger.critical
    elif status_code >= 400:
        log_symbol = "⚠️"
        log_level = logger.warning
    else:
        log_symbol = "❌"
        log_level = logger.error
    
    log_level(
        f"{log_symbol} Application error: {exc.message} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Status: {status_code}"
    )
    
    return JSONResponse(
        status_code=status_code,
        content=exc.to_dict()
    )


async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors from request body/query params.
    
    Args:
        request: The FastAPI request
        exc: Validation error
        
    Returns:
        JSONResponse with validation error details
    """
    logger.warning(
        f"⚠️  Validation error: {exc.errors()} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method}"
    )
    
    # Format validation errors
    errors = []
    for error in exc.errors():
        loc = " -> ".join(str(x) for x in error["loc"])
        errors.append({
            "field": loc,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Request validation failed",
            "detail": "One or more fields contain invalid data",
            "errors": errors
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions.
    
    Args:
        request: The FastAPI request
        exc: Any unhandled exception
        
    Returns:
        JSONResponse with generic error message
    """
    logger.critical(
        f"🔥 UNEXPECTED ERROR: {str(exc)} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method}",
        exc_info=True
    )
    
    # Don't expose internal error details in production
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


def register_exception_handlers(app: Any) -> None:
    """
    Register all exception handlers with the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    # Custom application exceptions
    app.add_exception_handler(AppException, app_exception_handler)
    
    # Pydantic validation errors
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    
    # Catch-all for unexpected exceptions
    app.add_exception_handler(Exception, generic_exception_handler)
    
    logger.info("✅ Registered global exception handlers")
