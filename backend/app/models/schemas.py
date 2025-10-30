"""
Pydantic v2 schema definitions for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    """Base schema with common fields."""

    class Config:
        from_attributes = True


class HealthResponse(BaseSchema):
    """Health check response schema."""

    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class ErrorResponse(BaseSchema):
    """Error response schema."""

    detail: str = Field(..., description="Error detail message")
    error_code: Optional[str] = Field(None, description="Error code")
