"""
Pydantic schemas for API request and response models.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.utils.validators import InputValidator


class SessionCreateRequest(BaseModel):
    """Request model for creating a new chat session."""
    
    user_id: Optional[str] = Field(None, description="Optional user identifier", max_length=255)
    title: Optional[str] = Field("New Chat Session", description="Session title", max_length=500)
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    @field_validator('title')
    @classmethod
    def validate_title_security(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate title using InputValidator.
        
        Delegates to InputValidator.validate_title() for:
        - Minimum length validation
        - Printable characters check
        - SQL injection pattern detection
        
        Note: max_length=500 is handled by Pydantic Field automatically
        """
        if v is None:
            return v
        
        try:
            return InputValidator.validate_title(v, field_name="title")
        except Exception as e:
            # Convert ValidationError to ValueError for Pydantic
            raise ValueError(str(e))
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id_format(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate user_id using InputValidator.
        
        Delegates to InputValidator.validate_user_id() for:
        - Length validation
        - Character validation (alphanumeric + special chars)
        - Whitespace stripping
        
        Note: max_length=255 is handled by Pydantic Field automatically
        """
        try:
            return InputValidator.validate_user_id(v, required=False)
        except Exception as e:
            raise ValueError(str(e))
    
    @field_validator('metadata')
    @classmethod
    def validate_metadata_content(cls, v: Optional[dict]) -> Optional[dict]:
        """
        Validate metadata using InputValidator.
        
        Delegates to InputValidator.validate_metadata() for:
        - Total size limit (10KB)
        - Key type and length validation
        - Value type validation
        """
        try:
            return InputValidator.validate_metadata(v)
        except Exception as e:
            raise ValueError(str(e))
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_id": "user_123",
                    "title": "Document Q&A Session",
                    "metadata": {"source": "web", "purpose": "research"}
                },
                {
                    "user_id": "alice@example.com",
                    "title": "My Research Notes",
                    "metadata": {"project": "thesis", "year": 2025}
                }
            ]
        }
    )


class SessionResponse(BaseModel):
    """Response model for chat session."""
    
    id: UUID = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    title: str = Field(..., description="Session title")
    status: str = Field(..., description="Session status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    metadata: Optional[str] = Field(None, description="Additional metadata")
    is_active: bool = Field(..., description="Whether session is active")
    message_count: int = Field(..., description="Number of messages")
    message: str = Field(..., description="Welcome message")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "user_123",
                "title": "Document Q&A Session",
                "status": "active",
                "created_at": "2025-10-31T12:00:00Z",
                "updated_at": "2025-10-31T12:00:00Z",
                "metadata": None,
                "is_active": True,
                "message_count": 0,
                "message": "hello! upload docs for me to Index"
            }
        }
    )


class SessionUpdateRequest(BaseModel):
    """Request model for updating a chat session."""
    
    title: Optional[str] = Field(None, description="Updated session title", max_length=500)
    status: Optional[str] = Field(None, description="Updated status")
    is_active: Optional[bool] = Field(None, description="Active status")
    metadata: Optional[dict] = Field(None, description="Updated metadata")
    
    @field_validator('title')
    @classmethod
    def validate_title_security(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate title using InputValidator.
        
        Delegates to InputValidator.validate_title() for all validation logic.
        """
        if v is None:
            return v
        
        try:
            return InputValidator.validate_title(v, field_name="title")
        except Exception as e:
            raise ValueError(str(e))
    
    @field_validator('status')
    @classmethod
    def validate_status_values(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate status using InputValidator.
        
        Delegates to InputValidator.validate_status() for whitelist validation.
        """
        try:
            return InputValidator.validate_status(v)
        except Exception as e:
            raise ValueError(str(e))
    
    @field_validator('metadata')
    @classmethod
    def validate_metadata_content(cls, v: Optional[dict]) -> Optional[dict]:
        """
        Validate metadata using InputValidator.
        
        Delegates to InputValidator.validate_metadata() for all validation logic.
        """
        try:
            return InputValidator.validate_metadata(v)
        except Exception as e:
            raise ValueError(str(e))
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Updated Session Title",
                    "status": "completed"
                },
                {
                    "status": "archived",
                    "is_active": False
                },
                {
                    "metadata": {"updated": True, "completion_date": "2025-11-01"}
                }
            ]
        }
    )


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Failed to create session",
                "detail": "Connection to database failed after 3 retries"
            }
        }
    )


class HealthCheckResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(..., description="Service status")
    database: str = Field(..., description="Database connection status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "database": "connected",
                "timestamp": "2025-10-31T12:00:00Z"
            }
        }
    )
